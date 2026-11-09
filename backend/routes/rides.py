"""API routes for Ride lifecycle and matchmaking actions."""

from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database import execute_query
from services.matchmaking import (
    accept_ride,
    calculate_fare,
    cancel_ride,
    complete_ride,
    driver_list,
    haversine_distance,
    reject_ride,
    request_ride,
)

router = APIRouter(prefix="/api/rides", tags=["Rides"])


class RideRequestInput(BaseModel):
    passenger_id: int = 1
    pickup_location: str
    destination: str
    pickup_latitude: float
    pickup_longitude: float
    destination_latitude: float
    destination_longitude: float
    vehicle_type: str = "Bike"


class DriverActionInput(BaseModel):
    driver_id: int


class FareEstimateInput(BaseModel):
    pickup_latitude: float
    pickup_longitude: float
    destination_latitude: float
    destination_longitude: float
    vehicle_type: str = "Bike"


@router.post("/estimate-fare")
def estimate_trip_fare(data: FareEstimateInput):
    """Calculates distance and fare without placing a request."""
    dist = haversine_distance(
        data.pickup_latitude,
        data.pickup_longitude,
        data.destination_latitude,
        data.destination_longitude,
    )
    fare = calculate_fare(dist, data.vehicle_type)
    return fare


@router.post("/request")
def create_ride_request(data: RideRequestInput):
    """Submits a new ride request, runs matchmaking, and offers to the best driver."""
    result = request_ride(
        passenger_id=data.passenger_id,
        pickup_location=data.pickup_location,
        destination=data.destination,
        pickup_lat=data.pickup_latitude,
        pickup_lon=data.pickup_longitude,
        dest_lat=data.destination_latitude,
        dest_lon=data.destination_longitude,
        vehicle_type=data.vehicle_type,
    )
    return result


@router.get("")
def list_rides(status: Optional[str] = None):
    """Returns ride records from PostgreSQL/database."""
    if status:
        query = "SELECT * FROM rides WHERE status = %s ORDER BY id DESC"
        rides = execute_query(query, (status,))
    else:
        query = "SELECT * FROM rides ORDER BY id DESC"
        rides = execute_query(query)

    # Attach driver name if driver_id is present
    for r in rides:
        if r.get("driver_id"):
            driver_node = driver_list.search(r["driver_id"])
            r["driver_name"] = driver_node.driver_name if driver_node else f"Driver #{r['driver_id']}"
            r["driver_phone"] = driver_node.phone_number if driver_node else ""
            r["vehicle_number"] = driver_node.vehicle_number if driver_node else ""
        else:
            r["driver_name"] = None

    return {"rides": rides}


@router.get("/{ride_id}")
def get_ride(ride_id: int):
    """Retrieve details for a specific ride."""
    rides = execute_query("SELECT * FROM rides WHERE id = %s", (ride_id,))
    if not rides:
        raise HTTPException(status_code=404, detail="Ride not found")
    ride = rides[0]
    if ride.get("driver_id"):
        driver_node = driver_list.search(ride["driver_id"])
        ride["driver_name"] = driver_node.driver_name if driver_node else f"Driver #{ride['driver_id']}"
        ride["driver_phone"] = driver_node.phone_number if driver_node else ""
        ride["vehicle_number"] = driver_node.vehicle_number if driver_node else ""
    return ride


@router.post("/{ride_id}/accept")
def handle_accept_ride(ride_id: int, data: DriverActionInput):
    """Driver accepts the offered ride."""
    return accept_ride(ride_id, data.driver_id)


@router.post("/{ride_id}/reject")
def handle_reject_ride(ride_id: int, data: DriverActionInput):
    """Driver rejects the ride offer, prompting reassignment to the next best driver."""
    return reject_ride(ride_id, data.driver_id)


@router.post("/{ride_id}/complete")
def handle_complete_ride(ride_id: int):
    """Marks ride as completed and restores driver availability."""
    return complete_ride(ride_id)


@router.post("/{ride_id}/cancel")
def handle_cancel_ride(ride_id: int):
    """Cancels ride and restores driver availability if needed."""
    return cancel_ride(ride_id)
