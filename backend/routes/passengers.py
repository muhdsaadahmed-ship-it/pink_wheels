"""API routes for Passenger records."""

from fastapi import APIRouter
from pydantic import BaseModel
from database import execute_commit, execute_query

router = APIRouter(prefix="/api/passengers", tags=["Passengers"])


class PassengerCreateRequest(BaseModel):
    name: str
    phone: str


@router.get("")
def get_passengers():
    """Retrieve all passengers from the database."""
    rows = execute_query("SELECT * FROM passengers ORDER BY id ASC")
    return {"passengers": rows}


@router.post("")
def create_passenger(req: PassengerCreateRequest):
    """Create a new passenger record in the database."""
    new_id = execute_commit(
        "INSERT INTO passengers (name, phone) VALUES (%s, %s)",
        (req.name, req.phone)
    )
    return {"id": new_id, "name": req.name, "phone": req.phone}
