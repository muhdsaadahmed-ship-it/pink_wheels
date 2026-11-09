"""Matchmaking and Ride Management Service.

Coordinates the 4 core DSA components:
1. Singly Linked List (Driver Registration & Availability)
2. FIFO Queue (Incoming Ride Requests)
3. Binary Min-Heap Priority Queue (Driver Matchmaking by ETA & Distance)
4. LIFO Stack (Ride Activity History)

Includes Haversine distance and configurable fare estimation.
"""

import math
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from dsa.linked_list import DriverLinkedList
from dsa.priority_queue import DriverPriorityQueue
from dsa.queue import RideQueue
from dsa.sample_drivers import INITIAL_SAMPLE_DRIVERS
from dsa.stack import ActivityStack
from database import execute_commit, execute_query


# ==========================================
# In-Memory Global DSA Singletons
# ==========================================

# 1. Driver Linked List (Primary DSA feature)
driver_list = DriverLinkedList()
for driver in INITIAL_SAMPLE_DRIVERS:
    driver_list.append(driver)

# 2. Ride Request Queue (FIFO)
ride_queue = RideQueue()

# 3. Ride Activity History (LIFO Stack)
activity_stack = ActivityStack()
activity_stack.push({
    "event": "SYSTEM_STARTUP",
    "description": f"System initialized with {driver_list.size()} sample drivers in Linked List.",
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# Dictionary to hold the Priority Queue of eligible drivers for each active ride
# ride_id -> DriverPriorityQueue instance
active_ride_pqs: Dict[int, DriverPriorityQueue] = {}


# ==========================================
# Geographic & Fare Utilities
# ==========================================

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates geographic distance between two coordinates in kilometers using Haversine formula."""
    R = 6371.0  # Earth's radius in kilometers

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return round(R * c, 2)


def calculate_eta(distance_km: float, speed_kmh: float = 25.0) -> float:
    """Estimates travel time in minutes based on distance and average city speed."""
    if distance_km <= 0.0:
        return 2.0  # Minimum ETA
    minutes = (distance_km / speed_kmh) * 60.0
    return round(max(2.0, minutes), 1)


def calculate_fare(distance_km: float, vehicle_type: str = "Bike") -> Dict[str, Any]:
    """Fare calculation according to project rates (no waiting fees):
    - Bike: Rs. 50 base + Rs. 15/km
    - Car (Standard): Rs. 100 base + Rs. 18/km
    - Good Car (Premium): Rs. 150 base + Rs. 22/km
    """
    v_type = vehicle_type.lower()
    if "bike" in v_type:
        base_fare = 50.0
        rate_per_km = 15.0
        label = "Bike (Pink Wheels)"
    elif "premium" in v_type or "good" in v_type:
        base_fare = 150.0
        rate_per_km = 22.0
        label = "Good Car (Premium)"
    else:
        base_fare = 100.0
        rate_per_km = 18.0
        label = "Car (Standard)"

    distance_charge = round(distance_km * rate_per_km, 2)
    total_fare = round(base_fare + distance_charge, 2)

    return {
        "vehicle_type": label,
        "base_fare": base_fare,
        "rate_per_km": rate_per_km,
        "distance_km": round(distance_km, 2),
        "distance_charge": distance_charge,
        "total_fare": total_fare,
        "currency": "PKR"
    }


# ==========================================
# Core Matchmaking Algorithm
# ==========================================

def build_priority_queue_for_ride(pickup_lat: float, pickup_lon: float, excluded_driver_ids: Optional[set] = None) -> DriverPriorityQueue:
    """Step 4 to 8:
    Retrieves registered drivers from Linked List, filters available drivers,
    computes distance and ETA to pickup, and inserts eligible candidates
    into the Binary Min-Heap Priority Queue.
    """
    if excluded_driver_ids is None:
        excluded_driver_ids = set()

    pq = DriverPriorityQueue()
    current = driver_list.head

    while current is not None:
        # Check if driver is registered, available, and not excluded
        if current.is_available and current.driver_id not in excluded_driver_ids:
            dist = haversine_distance(
                current.current_latitude,
                current.current_longitude,
                pickup_lat,
                pickup_lon
            )
            eta = calculate_eta(dist)

            candidate = {
                "driver_id": current.driver_id,
                "driver_name": current.driver_name,
                "phone_number": current.phone_number,
                "vehicle_number": current.vehicle_number,
                "current_latitude": current.current_latitude,
                "current_longitude": current.current_longitude,
                "distance_km": dist,
                "eta_minutes": eta,
            }
            # Step 8: Push into custom Priority Queue (Min-Heap)
            pq.push(candidate)

        current = current.next

    return pq


def request_ride(
    passenger_id: int,
    pickup_location: str,
    destination: str,
    pickup_lat: float,
    pickup_lon: float,
    dest_lat: float,
    dest_lon: float,
    vehicle_type: str = "Bike",
) -> Dict[str, Any]:
    """Workflow:
    1. Passenger submits request
    2. Enter FIFO Queue
    3. Calculate trip distance & fare
    4. Store permanent record in PostgreSQL/SQLite
    5. Matchmaking builds Priority Queue from Linked List
    6. Select top driver with lowest ETA
    """
    trip_distance = haversine_distance(pickup_lat, pickup_lon, dest_lat, dest_lon)
    fare_info = calculate_fare(trip_distance, vehicle_type)

    # 1. Enqueue request into custom FIFO Queue
    request_data = {
        "passenger_id": passenger_id,
        "pickup_location": pickup_location,
        "destination": destination,
        "pickup_lat": pickup_lat,
        "pickup_lon": pickup_lon,
        "dest_lat": dest_lat,
        "dest_lon": dest_lon,
        "distance_km": trip_distance,
        "fare": fare_info["total_fare"],
        "vehicle_type": vehicle_type,
        "requested_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    ride_queue.enqueue(request_data)

    # 2. Save ride record to Database
    insert_sql = """
        INSERT INTO rides (
            passenger_id, driver_id, pickup_location, destination,
            pickup_latitude, pickup_longitude, destination_latitude, destination_longitude,
            distance_km, fare, vehicle_type, status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    ride_id = execute_commit(insert_sql, (
        passenger_id, None, pickup_location, destination,
        pickup_lat, pickup_lon, dest_lat, dest_lon,
        trip_distance, fare_info["total_fare"], vehicle_type, "PENDING"
    ))

    # Dequeue from FIFO queue as it is now actively being processed by matchmaking
    processed_request = ride_queue.dequeue()

    # 3. Log event to LIFO Stack
    activity_stack.push({
        "ride_id": ride_id,
        "passenger_id": passenger_id,
        "event": "RIDE_REQUESTED",
        "description": f"Passenger {passenger_id} requested a {vehicle_type} ride from '{pickup_location}' to '{destination}' (Est. Fare: PKR {fare_info['total_fare']}).",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # 4. Build custom Priority Queue from available drivers in the Linked List
    pq = build_priority_queue_for_ride(pickup_lat, pickup_lon)
    active_ride_pqs[ride_id] = pq

    # 5. Select the best driver (lowest ETA) from Priority Queue
    best_driver = pq.pop()

    if best_driver:
        # Update ride in database to OFFERED
        execute_commit(
            "UPDATE rides SET driver_id = %s, status = %s WHERE id = %s",
            (best_driver["driver_id"], "OFFERED", ride_id)
        )
        activity_stack.push({
            "ride_id": ride_id,
            "driver_id": best_driver["driver_id"],
            "event": "DRIVER_OFFERED",
            "description": f"Ride #{ride_id} offered to Driver {best_driver['driver_name']} (ETA: {best_driver['eta_minutes']} min, {best_driver['distance_km']} km away).",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return {
        "ride_id": ride_id,
        "status": "OFFERED" if best_driver else "NO_DRIVERS_AVAILABLE",
        "assigned_driver": best_driver,
        "fare_info": fare_info,
        "trip_distance_km": trip_distance,
        "remaining_candidates_count": pq.size(),
    }


def accept_ride(ride_id: int, driver_id: int) -> Dict[str, Any]:
    """Driver accepts the ride offer:
    - Mark driver unavailable in Linked List
    - Update ride status in database to ACCEPTED
    - Log event in Activity Stack
    """
    # 1. Update Linked List availability
    driver_list.update_availability(driver_id, False)

    # 2. Update Database
    execute_commit(
        "UPDATE rides SET status = %s, driver_id = %s WHERE id = %s",
        ("ACCEPTED", driver_id, ride_id)
    )

    driver_node = driver_list.search(driver_id)
    driver_name = driver_node.driver_name if driver_node else f"Driver #{driver_id}"

    # 3. Log into Activity Stack
    activity_stack.push({
        "ride_id": ride_id,
        "driver_id": driver_id,
        "event": "RIDE_ACCEPTED",
        "description": f"Driver {driver_name} accepted Ride #{ride_id}. Driver marked BUSY in Linked List.",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    return {
        "ride_id": ride_id,
        "status": "ACCEPTED",
        "driver_id": driver_id,
        "driver_name": driver_name,
        "message": f"Ride accepted successfully. Driver {driver_name} is now en route."
    }


def reject_ride(ride_id: int, driver_id: int) -> Dict[str, Any]:
    """Driver rejects ride offer:
    - Pop the NEXT best driver from this ride's Priority Queue
    - Offer ride to the new candidate
    - If no more drivers in PQ, mark ride UNFULFILLED
    - Log event in Activity Stack
    """
    driver_node = driver_list.search(driver_id)
    driver_name = driver_node.driver_name if driver_node else f"Driver #{driver_id}"

    activity_stack.push({
        "ride_id": ride_id,
        "driver_id": driver_id,
        "event": "RIDE_REJECTED",
        "description": f"Driver {driver_name} rejected Ride #{ride_id}. Searching next priority driver in Min-Heap.",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    pq = active_ride_pqs.get(ride_id)
    next_driver = pq.pop() if pq and not pq.is_empty() else None

    if next_driver:
        execute_commit(
            "UPDATE rides SET driver_id = %s, status = %s WHERE id = %s",
            (next_driver["driver_id"], "OFFERED", ride_id)
        )
        activity_stack.push({
            "ride_id": ride_id,
            "driver_id": next_driver["driver_id"],
            "event": "DRIVER_REASSIGNED",
            "description": f"Ride #{ride_id} re-offered to next priority driver {next_driver['driver_name']} (ETA: {next_driver['eta_minutes']} min).",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return {
            "ride_id": ride_id,
            "status": "OFFERED",
            "assigned_driver": next_driver,
            "message": f"Ride reassigned to next candidate: {next_driver['driver_name']}."
        }
    else:
        execute_commit(
            "UPDATE rides SET status = %s WHERE id = %s",
            ("NO_DRIVERS_AVAILABLE", ride_id)
        )
        activity_stack.push({
            "ride_id": ride_id,
            "event": "MATCHMAKING_EXHAUSTED",
            "description": f"No further available drivers in Priority Queue for Ride #{ride_id}.",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return {
            "ride_id": ride_id,
            "status": "NO_DRIVERS_AVAILABLE",
            "assigned_driver": None,
            "message": "All eligible drivers rejected or none available in priority queue."
        }


def complete_ride(ride_id: int) -> Dict[str, Any]:
    """Ride is completed:
    - Update driver availability to True in Linked List
    - Update ride status in database to COMPLETED
    - Log event in Activity Stack
    """
    rows = execute_query("SELECT driver_id FROM rides WHERE id = %s", (ride_id,))
    driver_id = rows[0]["driver_id"] if rows and rows[0]["driver_id"] else None

    if driver_id:
        driver_list.update_availability(driver_id, True)

    execute_commit(
        "UPDATE rides SET status = %s WHERE id = %s",
        ("COMPLETED", ride_id)
    )

    driver_node = driver_list.search(driver_id) if driver_id else None
    driver_name = driver_node.driver_name if driver_node else "Assigned Driver"

    activity_stack.push({
        "ride_id": ride_id,
        "driver_id": driver_id,
        "event": "RIDE_COMPLETED",
        "description": f"Ride #{ride_id} completed successfully. Driver {driver_name} is now available again.",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    if ride_id in active_ride_pqs:
        del active_ride_pqs[ride_id]

    return {
        "ride_id": ride_id,
        "status": "COMPLETED",
        "message": f"Ride completed. Driver {driver_name} is now marked AVAILABLE in Linked List."
    }


def cancel_ride(ride_id: int) -> Dict[str, Any]:
    """Passenger or system cancels pending/offered ride:
    - Free up driver if accepted
    - Update status to CANCELLED in database
    - Log event in Activity Stack
    """
    rows = execute_query("SELECT driver_id, status FROM rides WHERE id = %s", (ride_id,))
    if rows:
        driver_id = rows[0]["driver_id"]
        status = rows[0]["status"]
        if driver_id and status == "ACCEPTED":
            driver_list.update_availability(driver_id, True)

    execute_commit(
        "UPDATE rides SET status = %s WHERE id = %s",
        ("CANCELLED", ride_id)
    )

    activity_stack.push({
        "ride_id": ride_id,
        "event": "RIDE_CANCELLED",
        "description": f"Ride #{ride_id} was cancelled.",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    if ride_id in active_ride_pqs:
        del active_ride_pqs[ride_id]

    return {
        "ride_id": ride_id,
        "status": "CANCELLED",
        "message": "Ride cancelled."
    }
