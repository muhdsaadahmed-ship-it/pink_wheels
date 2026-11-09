from app.models import (
    AvailabilityStatus,
    DriverProfile,
    PassengerProfile,
    User,
    UserRole,
    VerificationStatus,
)
from app.core.security import hash_password
from app.services import driver_matching_service, fare_service
from tests.conftest import auth_headers


def make_driver(db, phone, lat, lng, availability=AvailabilityStatus.online,
                verified=True):
    user = User(
        full_name=f"Driver {phone}", phone_number=phone,
        password_hash=hash_password("Password1"),
        role=UserRole.driver,
        verification_status=(VerificationStatus.verified if verified
                             else VerificationStatus.pending),
        phone_verified=True,
    )
    db.add(user)
    db.flush()
    db.add(DriverProfile(
        user_id=user.id, current_latitude=lat, current_longitude=lng,
        availability_status=availability,
    ))
    db.commit()
    return user


def test_fare_formula(db_session):
    settings = fare_service.get_settings(db_session)
    result = fare_service.estimate_fare(db_session, distance_km=5.0, duration_min=15.0)
    expected = (settings.base_fare + 5 * settings.per_km_rate
                + 15 * settings.per_minute_rate) * settings.peak_multiplier
    assert result["estimated_fare"] == round(max(expected, settings.minimum_fare), 2)


def test_minimum_fare_floor(db_session):
    settings = fare_service.get_settings(db_session)
    result = fare_service.estimate_fare(db_session, distance_km=0.1, duration_min=0.5)
    assert result["estimated_fare"] == settings.minimum_fare
    assert result["minimum_fare_applied"] is True


def test_admin_fare_configuration(client, admin_headers):
    response = client.patch("/api/admin/fare-settings", headers=admin_headers,
                            json={"per_km_rate": 55.0, "peak_multiplier": 1.25})
    assert response.status_code == 200
    assert response.json()["per_km_rate"] == 55.0

    public = client.get("/api/drivers/fare-settings")
    assert public.status_code == 200
    assert public.json()["per_km_rate"] == 55.0


def test_nearby_driver_search(client, db_session):
    make_driver(db_session, "+923111000101", 24.8607, 67.0011)
    passenger = User(
        full_name="P", phone_number="+923111000102",
        password_hash=hash_password("Password1"), role=UserRole.passenger,
        verification_status=VerificationStatus.verified, phone_verified=True,
    )
    db_session.add(passenger)
    db_session.flush()
    db_session.add(PassengerProfile(user_id=passenger.id))
    db_session.commit()
    headers = auth_headers(client, passenger.phone_number)

    response = client.get("/api/drivers/nearby?lat=24.8609&lng=67.0012",
                          headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["distance_km"] < 1


def test_matching_excludes_unavailable_and_unverified(db_session):
    make_driver(db_session, "+923111000103", 24.8607, 67.0011)  # online, verified
    make_driver(db_session, "+923111000104", 24.8608, 67.0012,
                availability=AvailabilityStatus.offline)
    make_driver(db_session, "+923111000105", 24.8609, 67.0013, verified=False)
    far = make_driver(db_session, "+923111000106", 24.99, 67.30)  # >5km away

    candidates = driver_matching_service.find_eligible_drivers(
        db_session, 24.8607, 67.0011)
    ids = {c["driver_id"] for c in candidates}
    online = db_session.query(User).filter_by(phone_number="+923111000103").one()
    assert ids == {online.id}


def test_priority_queue_ranks_lowest_eta_first(db_session):
    near = make_driver(db_session, "+923111000107", 24.86075, 67.00115)
    far = make_driver(db_session, "+923111000108", 24.8640, 67.0050)
    candidates = driver_matching_service.find_eligible_drivers(
        db_session, 24.8607, 67.0011)
    queue = driver_matching_service.build_allocation_queue(candidates, "req-test")
    first = queue.pop()
    assert first.driver_id == near.id
    assert queue.pop().driver_id == far.id
