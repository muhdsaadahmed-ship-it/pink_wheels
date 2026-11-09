"""API routes for DSA visual inspection and demonstration."""

from fastapi import APIRouter
from pydantic import BaseModel

from services.matchmaking import (
    activity_stack,
    build_priority_queue_for_ride,
    calculate_eta,
    driver_list,
    haversine_distance,
    ride_queue,
)

router = APIRouter(prefix="/api/dsa", tags=["DSA Demonstrations"])


class MatchmakingSimulateInput(BaseModel):
    pickup_latitude: float = 24.8615
    pickup_longitude: float = 67.0099


@router.get("/linked-list")
def get_linked_list_demo():
    """Inspect the Driver Singly Linked List."""
    nodes = driver_list.traverse()
    return {
        "structure": "Singly Linked List",
        "purpose": "Driver Registration and Availability Tracking",
        "size": driver_list.size(),
        "chain_display": driver_list.display(),
        "nodes": nodes,
    }


@router.get("/queue")
def get_queue_demo():
    """Inspect the FIFO Ride Request Queue."""
    items = ride_queue.display()
    return {
        "structure": "FIFO Queue",
        "purpose": "Passenger Ride Request Management",
        "size": ride_queue.size(),
        "is_empty": ride_queue.is_empty(),
        "front": ride_queue.peek(),
        "items": items,
    }


@router.get("/priority-queue")
def get_priority_queue_demo(lat: float = 24.8615, lon: float = 67.0099):
    """Inspect the Binary Min-Heap Priority Queue for a given coordinate."""
    pq = build_priority_queue_for_ride(lat, lon)
    sorted_order = pq.display()
    return {
        "structure": "Binary Min-Heap Priority Queue",
        "purpose": "Driver Selection by Lowest ETA & Distance",
        "reference_point": {"latitude": lat, "longitude": lon},
        "size": pq.size(),
        "heap_array": pq.heap,
        "sorted_priority_order": sorted_order,
    }


@router.get("/stack")
def get_stack_demo():
    """Inspect the LIFO Activity Stack."""
    items = activity_stack.display()
    return {
        "structure": "LIFO Stack",
        "purpose": "Ride Activity History & Audit Trail",
        "size": activity_stack.size(),
        "is_empty": activity_stack.is_empty(),
        "top": activity_stack.peek(),
        "items": items,
    }


@router.post("/matchmaking")
def simulate_matchmaking(data: MatchmakingSimulateInput):
    """Step-by-step demonstration of the matchmaking algorithm linking Linked List and Priority Queue."""
    steps = []

    # Step 1: Scan Linked list
    steps.append({
        "step": 1,
        "action": "Traverse Linked List",
        "detail": f"Scanning {driver_list.size()} registered driver nodes."
    })

    # Step 2: Filter available drivers
    available_nodes = driver_list.get_available_drivers()
    steps.append({
        "step": 2,
        "action": "Filter Available Drivers",
        "detail": f"Found {len(available_nodes)} drivers with is_available = True."
    })

    # Step 3: Compute distances and ETAs
    candidates = []
    for node in available_nodes:
        dist = haversine_distance(node.current_latitude, node.current_longitude, data.pickup_latitude, data.pickup_longitude)
        eta = calculate_eta(dist)
        candidates.append({
            "driver_id": node.driver_id,
            "driver_name": node.driver_name,
            "distance_km": dist,
            "eta_minutes": eta,
            "vehicle_number": node.vehicle_number
        })
    steps.append({
        "step": 3,
        "action": "Calculate Distance (Haversine) & ETA",
        "detail": f"Calculated ETAs for all {len(candidates)} candidate drivers."
    })

    # Step 4: Build Min-Heap
    pq = build_priority_queue_for_ride(data.pickup_latitude, data.pickup_longitude)
    ranked = pq.display()
    steps.append({
        "step": 4,
        "action": "Build Binary Min-Heap Priority Queue",
        "detail": "Inserted eligible drivers into Min-Heap; root element has the lowest ETA."
    })

    # Step 5: Best driver selection
    best_candidate = ranked[0] if ranked else None
    steps.append({
        "step": 5,
        "action": "Select Top Driver",
        "detail": f"Selected {best_candidate['driver_name']} (ETA: {best_candidate['eta_minutes']} mins, Distance: {best_candidate['distance_km']} km)" if best_candidate else "No driver available"
    })

    return {
        "steps": steps,
        "ranked_drivers": ranked,
        "selected_driver": best_candidate
    }
