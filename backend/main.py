"""FastAPI Main Application for Pink Wheels DSA Project.

A simple, educational backend demonstrating 4 core data structures:
1. Singly Linked List (Driver Registration)
2. FIFO Queue (Ride Request Management)
3. Binary Min-Heap Priority Queue (Driver Matchmaking)
4. LIFO Stack (Activity History)
"""

import sys
import os

# Ensure backend directory is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routes.drivers import router as drivers_router
from routes.passengers import router as passengers_router
from routes.rides import router as rides_router
from routes.dsa import router as dsa_router

# Initialize database tables on startup
init_db()

app = FastAPI(
    title="Pink Wheels - DSA Ride Booking API",
    description="Academic ride-booking API demonstrating Linked List, Queue, Priority Queue, and Stack.",
    version="1.0.0"
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(drivers_router)
app.include_router(passengers_router)
app.include_router(rides_router)
app.include_router(dsa_router)


@app.get("/")
def root():
    return {
        "project": "Pink Wheels — DSA-Based Ride Booking Project",
        "description": "Safe rides. Fair prices. Women-focused bike ride-booking demonstration.",
        "dsa_features": [
            "1. Singly Linked List (Driver Registration)",
            "2. FIFO Queue (Ride Request Management)",
            "3. Binary Min-Heap Priority Queue (Driver Matchmaking)",
            "4. LIFO Stack (Ride Activity History)"
        ],
        "endpoints": [
            "/api/drivers",
            "/api/passengers",
            "/api/rides",
            "/api/dsa/linked-list",
            "/api/dsa/queue",
            "/api/dsa/priority-queue",
            "/api/dsa/stack",
            "/api/dsa/matchmaking",
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
