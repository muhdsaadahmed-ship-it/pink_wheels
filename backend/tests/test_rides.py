import pytest

from app.models import (
    AvailabilityStatus,
    DriverProfile,
    PassengerProfile,
    User,
    UserRole,
    VerificationStatus,
)
from app.core.security import hash_password
from tests.conftest import auth_headers

PASSWORD = "Password1"


def make_user(db, phone, role, name=None, verified=True, lat=None, lng=None,
              availability=None):
    user = User(
        full_name=name or f"User {phone}",
        phone_number=phone,
        password_hash=hash_password(PASSWORD),
        role=role,
        verification_status=(VerificationStatus.verified if verified
                             else VerificationStatus.pending),
        phone_verified=True,
    )
    db.add(user)
    db.flush()
    if role == UserRole.passenger:
        db.add(PassengerProfile(user_id=user.id))
    else:
        db.add(DriverProfile(
            user_id=user.id,
            current_latitude=lat,
            current_longitude=lng,
            availability_status=availability or AvailabilityStatus.offline,
        ))
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def passenger(db_session):
    return make_user(db_session, "+923111000001", UserRole.passenger)


@pytest.fixture
def driver(db_session):
    return make_user(db_session, "+923111000002", UserRole.driver,
                     lat=24.8610, lng=67.0015,
                     availability=AvailabilityStatus.online)


RIDE_PAYLOAD = {
    "pickup_lat": 24.8607, "pickup_lng": 67.0011,
    "destination_lat": 24.9067, "destination_lng": 67.1608,
    "pickup_label": "Saddar", "destination_label": "Airport",
}


def request_ride(client, headers):
    return client.post("/api/rides/request", headers=headers, json=RIDE_PAYLOAD)


def test_estimate_returns_route_and_fare(client):
    response = client.post("/api/rides/estimate", json=RIDE_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert body["total_distance_km"] > 0
    fare = body["fare"]
    assert fare["estimated_fare"] > 0
    assert fare["currency"] == "PKR"


def test_full_ride_workflow(client, passenger, driver):
    p_headers = auth_headers(client, passenger.phone_number)
    d_headers = auth_headers(client, driver.phone_number)

    ride = request_ride(client, p_headers).json()
    assert ride["status"] in ("offered", "searching", "expired")

    # Driver sees the incoming request.
    requests = client.get("/api/drivers/requests", headers=d_headers).json()
    assert len(requests) == 1
    assert requests[0]["ride_id"] == ride["id"]

    accepted = client.post(f"/api/rides/{ride['id']}/accept", headers=d_headers)
    assert accepted.status_code == 200
    assert accepted.json()["status"] == "accepted"

    started = client.post(f"/api/rides/{ride['id']}/start", headers=d_headers)
    assert started.status_code == 200

    located = client.post(f"/api/rides/{ride['id']}/location", headers=d_headers,
                          json={"latitude": 24.87, "longitude": 67.02})
    assert located.status_code == 201

    completed = client.post(f"/api/rides/{ride['id']}/complete", headers=d_headers)
    assert completed.status_code == 200
    assert completed.json()["status"] == "completed"

    # Payment record exists and driver can confirm cash collection.
    payment = client.get(f"/api/payments/ride/{ride['id']}", headers=d_headers).json()
    assert payment["payment_status"] == "pending"
    confirmed = client.post(f"/api/payments/{payment['id']}/confirm", headers=d_headers)
    assert confirmed.status_code == 200

    # Both sides rate each other.
    rating = client.post(f"/api/rides/{ride['id']}/rate", headers=p_headers,
                         json={"score": 5, "review": "Great ride"})
    assert rating.status_code == 201
    rating2 = client.post(f"/api/rides/{ride['id']}/rate", headers=d_headers,
                          json={"score": 4})
    assert rating2.status_code == 201


def test_duplicate_active_ride_rejected(client, passenger, driver):
    p_headers = auth_headers(client, passenger.phone_number)
    assert request_ride(client, p_headers).status_code == 201
    assert request_ride(client, p_headers).status_code == 409


def test_invalid_state_transition_rejected(client, passenger, driver):
    p_headers = auth_headers(client, passenger.phone_number)
    d_headers = auth_headers(client, driver.phone_number)
    ride = request_ride(client, p_headers).json()
    client.post(f"/api/rides/{ride['id']}/accept", headers=d_headers)
    # Cannot complete before starting.
    completed = client.post(f"/api/rides/{ride['id']}/complete", headers=d_headers)
    assert completed.status_code == 409


def test_cancel_before_accept_no_fee(client, passenger, driver):
    p_headers = auth_headers(client, passenger.phone_number)
    ride = request_ride(client, p_headers).json()
    cancelled = client.post(f"/api/rides/{ride['id']}/cancel", headers=p_headers,
                            json={"reason": "changed my mind"})
    assert cancelled.status_code == 200
    assert cancelled.json()["cancellation_fee"] == 0


def test_cancel_after_accept_applies_fee(client, passenger, driver):
    p_headers = auth_headers(client, passenger.phone_number)
    d_headers = auth_headers(client, driver.phone_number)
    ride = request_ride(client, p_headers).json()
    client.post(f"/api/rides/{ride['id']}/accept", headers=d_headers)
    cancelled = client.post(f"/api/rides/{ride['id']}/cancel", headers=p_headers,
                            json={"reason": "emergency"})
    assert cancelled.status_code == 200
    assert cancelled.json()["cancellation_fee"] > 0


def test_unrelated_user_cannot_access_ride(client, passenger, db_session):
    p_headers = auth_headers(client, passenger.phone_number)
    ride = request_ride(client, p_headers).json()
    stranger = make_user(db_session, "+923111000003", UserRole.passenger)
    s_headers = auth_headers(client, stranger.phone_number)
    response = client.get(f"/api/rides/{ride['id']}", headers=s_headers)
    assert response.status_code == 403


def test_unverified_passenger_cannot_book(client, db_session):
    unverified = make_user(db_session, "+923111000004", UserRole.passenger, verified=False)
    headers = auth_headers(client, unverified.phone_number)
    assert request_ride(client, headers).status_code == 403


def test_ride_expires_without_drivers(client, db_session):
    passenger = make_user(db_session, "+923111000005", UserRole.passenger)
    p_headers = auth_headers(client, passenger.phone_number)
    # No online drivers at all -> ride expires.
    ride = request_ride(client, p_headers).json()
    assert ride["status"] == "expired"


def test_driver_reject_offers_next(client, passenger, driver, db_session):
    second = make_user(db_session, "+923111000006", UserRole.driver,
                       lat=24.8612, lng=67.0018,
                       availability=AvailabilityStatus.online)
    p_headers = auth_headers(client, passenger.phone_number)
    d1_headers = auth_headers(client, driver.phone_number)
    d2_headers = auth_headers(client, second.phone_number)

    ride = request_ride(client, p_headers).json()
    rejected = client.post(f"/api/rides/{ride['id']}/reject", headers=d1_headers)
    assert rejected.status_code == 200

    # Second driver now sees the offer and can accept.
    requests = client.get("/api/drivers/requests", headers=d2_headers).json()
    assert any(r["ride_id"] == ride["id"] for r in requests)
    accepted = client.post(f"/api/rides/{ride['id']}/accept", headers=d2_headers)
    assert accepted.status_code == 200
