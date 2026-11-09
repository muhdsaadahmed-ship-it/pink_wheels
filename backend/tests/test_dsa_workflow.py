import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import init_db
from services.matchmaking import request_ride, accept_ride, reject_ride, complete_ride, driver_list

def test_workflow():
    init_db()
    print("Testing Matchmaking Workflow...")
    
    # Request a ride near Saddar (24.8615, 67.0099)
    res = request_ride(
        passenger_id=1,
        pickup_location="Saddar Karachi",
        destination="Clifton Beach",
        pickup_lat=24.8615,
        pickup_lon=67.0099,
        dest_lat=24.8138,
        dest_lon=67.0300,
        vehicle_type="Bike"
    )

    print("Ride Requested. ID:", res["ride_id"])
    best = res["assigned_driver"]
    assert best is not None, "A driver should have been assigned"
    print(f"Top Selected Driver: {best['driver_name']} (ETA: {best['eta_minutes']} min, {best['distance_km']} km)")

    # Test rejection
    ride_id = res["ride_id"]
    rej_res = reject_ride(ride_id, best["driver_id"])
    next_driver = rej_res.get("assigned_driver")
    assert next_driver is not None, "Next driver should be selected after rejection"
    print(f"After rejection, next driver: {next_driver['driver_name']} (ETA: {next_driver['eta_minutes']} min)")

    # Test acceptance of the second driver
    next_id = next_driver["driver_id"]
    accept_ride(ride_id, next_id)
    d_node = driver_list.search(next_id)
    assert d_node.is_available is False, "Driver should be marked unavailable after acceptance"
    print(f"Driver {d_node.driver_name} availability status: {d_node.is_available}")

    # Test completion
    complete_ride(ride_id)
    assert d_node.is_available is True, "Driver should be marked available after completion"
    print(f"After completion, Driver {d_node.driver_name} availability status: {d_node.is_available}")
    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_workflow()
