"""API routes for Driver operations (backed by custom Linked List)."""

from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.matchmaking import driver_list

router = APIRouter(prefix="/api/drivers", tags=["Drivers"])


class DriverRegisterRequest(BaseModel):
    driver_name: str
    phone_number: str
    vehicle_number: str
    current_latitude: float
    current_longitude: float
    is_available: bool = True
    driver_id: Optional[int] = None


class AvailabilityUpdateRequest(BaseModel):
    is_available: bool


@router.get("")
def get_drivers():
    """Retrieve all drivers registered in the custom Linked List."""
    drivers = driver_list.traverse()
    return {
        "count": driver_list.size(),
        "drivers": drivers,
        "chain_display": driver_list.display()
    }


@router.post("/register")
def register_driver(data: DriverRegisterRequest):
    """Register a new driver node into the custom Linked List."""
    # Generate unique ID if not provided
    if data.driver_id is None:
        # Simple auto-increment ID based on max existing or count
        highest = 100
        current = driver_list.head
        while current is not None:
            if current.driver_id > highest:
                highest = current.driver_id
            current = current.next
        driver_id = highest + 1
    else:
        driver_id = data.driver_id
        if driver_list.search(driver_id):
            raise HTTPException(status_code=400, detail=f"Driver ID {driver_id} is already registered.")

    driver_dict = {
        "driver_id": driver_id,
        "driver_name": data.driver_name,
        "phone_number": data.phone_number,
        "vehicle_number": data.vehicle_number,
        "current_latitude": data.current_latitude,
        "current_longitude": data.current_longitude,
        "is_available": data.is_available,
    }

    new_node = driver_list.append(driver_dict)
    return {
        "message": "Driver registered successfully in Linked List",
        "driver": new_node.to_dict(),
        "total_registered": driver_list.size()
    }


@router.get("/{driver_id}")
def get_driver(driver_id: int):
    """Search for a driver node in the Linked List by driver_id."""
    node = driver_list.search(driver_id)
    if not node:
        raise HTTPException(status_code=404, detail="Driver not found in Linked List")
    return node.to_dict()


@router.delete("/{driver_id}")
def delete_driver(driver_id: int):
    """Delete a driver node from the Linked List by driver_id."""
    deleted = driver_list.delete(driver_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Driver not found in Linked List")
    return {
        "message": f"Driver {driver_id} deleted successfully from Linked List",
        "total_registered": driver_list.size()
    }


@router.patch("/{driver_id}/availability")
def update_driver_availability(driver_id: int, req: AvailabilityUpdateRequest):
    """Update driver availability status in the Linked List."""
    updated = driver_list.update_availability(driver_id, req.is_available)
    if not updated:
        raise HTTPException(status_code=404, detail="Driver not found in Linked List")
    return {
        "driver_id": driver_id,
        "is_available": req.is_available,
        "message": f"Driver availability updated to {'Available' if req.is_available else 'Busy'}"
    }
