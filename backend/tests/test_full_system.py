"""Comprehensive End-to-End Test for Pink Wheels DSA System."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_dsa_full_suite():
    print("\n==============================")
    print("STARTING FULL DSA SYSTEM TESTS")
    print("==============================")

    # 1. Test Root Endpoint
    r = client.get("/")
    assert r.status_code == 200, f"Root failed: {r.status_code}"
    print("[PASS] [API] Root endpoint responding")

    # 2. Test Linked List Initial Seeding & Driver Registration
    r = client.get("/api/dsa/linked-list")
    assert r.status_code == 200
    ll_data = r.json()
    initial_count = ll_data["size"]
    assert initial_count >= 10, f"Expected at least 10 sample drivers, got {initial_count}"
    print(f"[PASS] [Linked List] Initial drivers verified ({initial_count} loaded into Singly Linked List)")

    # 3. Test Appending New Driver Node
    new_driver_payload = {
        "driver_id": 999,
        "driver_name": "Farzana Kausar",
        "phone_number": "+92 345 9999999",
        "vehicle_number": "KHI-TEST-99",
        "current_latitude": 24.8700,
        "current_longitude": 67.0500,
        "is_available": True,
    }
    r = client.post("/api/drivers/register", json=new_driver_payload)
    assert r.status_code == 200
    assert r.json()["total_registered"] == initial_count + 1
    print(f"[PASS] [Linked List] Appended driver #999 (size: {r.json()['total_registered']})")

    # 4. Test Search Driver Node
    r = client.get("/api/drivers/999")
    assert r.status_code == 200
    assert r.json()["driver_name"] == "Farzana Kausar"
    print("[PASS] [Linked List] Search node #999 successful")

    # 5. Test Delete Driver Node
    r = client.delete("/api/drivers/999")
    assert r.status_code == 200
    r_check = client.get("/api/drivers/999")
    assert r_check.status_code == 404
    print("[PASS] [Linked List] Deleted node #999; verified search returns 404")

    # 6. Test Fare Estimation Formula (Rs. 15/km for Bike, no waiting fees)
    fare_payload = {
        "pickup_latitude": 24.8615,
        "pickup_longitude": 67.0099,
        "destination_latitude": 24.8138,
        "destination_longitude": 67.0300,
        "vehicle_type": "Bike",
    }
    r = client.post("/api/rides/estimate-fare", json=fare_payload)
    assert r.status_code == 200
    fare_res = r.json()
    assert fare_res["rate_per_km"] == 15.0
    expected_fare = round(50.0 + fare_res["distance_km"] * 15.0, 2)
    assert fare_res["total_fare"] == expected_fare
    print(f"[PASS] [Fare Formula] Bike fare verified: PKR {fare_res['total_fare']} ({fare_res['distance_km']} km @ Rs. 15/km)")

    # 7. Test Priority Queue (Binary Min-Heap)
    r = client.get("/api/dsa/priority-queue?lat=24.8615&lon=67.0099")
    assert r.status_code == 200
    pq_data = r.json()
    sorted_order = pq_data["sorted_priority_order"]
    assert len(sorted_order) > 0
    # Verify min-heap property (each driver has <= ETA than next)
    for i in range(len(sorted_order) - 1):
        assert sorted_order[i]["eta_minutes"] <= sorted_order[i + 1]["eta_minutes"], "Min-heap ordering violated!"
    print(f"[PASS] [Priority Queue] Min-heap verified: {len(sorted_order)} drivers ranked by lowest ETA")

    # 8. Test Ride Request, Queue Enqueue & Matchmaking Workflow
    ride_payload = {
        "passenger_id": 1,
        "pickup_location": "Saddar Empress Market",
        "destination": "Clifton Beach",
        "pickup_latitude": 24.8615,
        "pickup_longitude": 67.0099,
        "destination_latitude": 24.8138,
        "destination_longitude": 67.0300,
        "vehicle_type": "Bike",
    }
    r = client.post("/api/rides/request", json=ride_payload)
    assert r.status_code == 200
    req_res = r.json()
    ride_id = req_res["ride_id"]
    assigned_driver = req_res["assigned_driver"]
    assert assigned_driver is not None, "Matchmaking failed to select a driver"
    print(f"[PASS] [Matchmaking] Ride #{ride_id} created; top driver offered: {assigned_driver['driver_name']} (ETA: {assigned_driver['eta_minutes']} min)")

    # 9. Test Driver Rejection -> Priority Queue Cascading to Next Driver
    r = client.post(f"/api/rides/{ride_id}/reject", json={"driver_id": assigned_driver["driver_id"]})
    assert r.status_code == 200
    rej_res = r.json()
    second_driver = rej_res.get("assigned_driver")
    assert second_driver is not None, "Expected next priority driver on rejection"
    assert second_driver["driver_id"] != assigned_driver["driver_id"]
    print(f"[PASS] [Matchmaking] Rejection cascaded in Min-Heap to next driver: {second_driver['driver_name']}")

    # 10. Test Driver Acceptance -> Linked List Availability Update
    r = client.post(f"/api/rides/{ride_id}/accept", json={"driver_id": second_driver["driver_id"]})
    assert r.status_code == 200
    # Check driver in Linked List
    r_driver = client.get(f"/api/drivers/{second_driver['driver_id']}")
    assert r_driver.json()["is_available"] is False, "Accepted driver should be unavailable in Linked List"
    print(f"[PASS] [Linked List Integration] Driver {second_driver['driver_name']} availability marked False in Linked List")

    # 11. Test Complete Ride -> Linked List Availability Restoration
    r = client.post(f"/api/rides/{ride_id}/complete")
    assert r.status_code == 200
    r_driver_after = client.get(f"/api/drivers/{second_driver['driver_id']}")
    assert r_driver_after.json()["is_available"] is True, "Completed driver should be available again in Linked List"
    print(f"[PASS] [Linked List Integration] Driver {second_driver['driver_name']} availability restored to True in Linked List")

    # 12. Test LIFO Stack Activity History
    r = client.get("/api/dsa/stack")
    assert r.status_code == 200
    stack_data = r.json()
    assert stack_data["size"] > 0
    top_event = stack_data["top"]
    assert top_event["event"] == "RIDE_COMPLETED", f"Expected top event RIDE_COMPLETED, got {top_event['event']}"
    print(f"[PASS] [Activity Stack] LIFO verified: Top of stack is '{top_event['event']}'")

    # 13. Test PostgreSQL / Database Ride History Persistence
    r = client.get("/api/rides")
    assert r.status_code == 200
    rides_list = r.json()["rides"]
    assert any(ride["id"] == ride_id for ride in rides_list)
    print(f"[PASS] [Database] Ride #{ride_id} verified in persistent ride records (Total: {len(rides_list)})")

    print("\n===========================================")
    print("ALL 13 END-TO-END DSA TESTS PASSED 100%!")
    print("===========================================")


if __name__ == "__main__":
    test_dsa_full_suite()
