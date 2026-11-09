# Pink Wheels — DSA-Based Ride Booking Project

> Safe rides. Fair prices. • University Data Structures & Algorithms Project

Pink Wheels is a women-focused bike ride-booking demonstration application designed for Karachi, Pakistan. The primary academic objective is to demonstrate four foundational Data Structures and Algorithms in a realistic, interactive ride-hailing architecture without production bloat.

---

## 🧠 Core Data Structures & Algorithms

| # | Data Structure | Implementation File | System Role | Key Operations |
|---|---|---|---|---|
| **1** | **Singly Linked List** | `backend/dsa/linked_list.py` | **Driver Registration (Primary Feature)**: In-memory chain of registered driver nodes. Drivers stay registered even when busy/offline. | `append()`, `insert()`, `delete()`, `search()`, `traverse()`, `display()`, `size()` |
| **2** | **FIFO Queue** | `backend/dsa/queue.py` | **Ride Request Management**: First-In, First-Out queue storing incoming passenger requests. | `enqueue()`, `dequeue()`, `peek()`, `is_empty()`, `size()`, `display()` |
| **3** | **Binary Min-Heap Priority Queue** | `backend/dsa/priority_queue.py` | **Driver Selection**: Custom min-heap prioritizes available drivers by lowest Estimated Time of Arrival (ETA), with distance as tie-breaker. | `push()`, `pop()`, `peek()`, `is_empty()`, `size()`, `heapify()`, `update_priority()` |
| **4** | **LIFO Stack** | `backend/dsa/stack.py` | **Ride Activity History**: Last-In, First-Out audit trail of system events (`RIDE_REQUESTED`, `DRIVER_OFFERED`, `RIDE_ACCEPTED`, `RIDE_COMPLETED`). | `push()`, `pop()`, `peek()`, `is_empty()`, `size()`, `display()` |

---

## ⚡ Custom Matchmaking Algorithm (`backend/services/matchmaking.py`)

1. **Request Intake**: Passenger submits pickup and destination; request enters custom **FIFO Queue**.
2. **Linked List Traversal**: Algorithm scans the **Singly Linked List** and filters registered drivers whose `is_available == True`.
3. **Haversine Distance**: Calculates geographic distance from candidate driver to pickup coordinates.
4. **ETA Estimation**: Calculates travel time using Karachi average city transit speed (25 km/h).
5. **Min-Heap Construction**: Eligible drivers are pushed into the **Binary Min-Heap Priority Queue**.
6. **Optimal Selection**: The root element (lowest ETA) is extracted and offered the ride.
7. **Rejection Cascade**: If the offered driver rejects, the next best driver is popped from the heap.
8. **Acceptance & Availability**: On acceptance, driver availability is updated to `False` in the Linked List.
9. **Trip Completion**: When trip completes, driver availability is restored to `True` in the Linked List and ride is marked `COMPLETED` in PostgreSQL.

---

## 💰 Fare Calculation Formula

- **Bike (Pink Wheels)**: Rs. 50 base fare + Rs. 15 per km
- **Car (Standard)**: Rs. 100 base fare + Rs. 18 per km
- **Good Car (Premium)**: Rs. 150 base fare + Rs. 22 per km
- *No waiting fees or complex surge pricing.*

$$\text{Fare} = \text{Base Fare} + (\text{Distance in km} \times \text{Rate per km})$$

---

## 🚀 How to Run

### Backend (FastAPI + psycopg/SQLite)

```bash
cd backend
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Run API server
python -m uvicorn main:app --reload --port 8000
```
- API Docs: `http://localhost:8000/docs`

### Frontend (Vue 3 + Vite + Tailwind + Leaflet)

```bash
cd frontend
npm install
npm run dev
```
- Web Application: `http://localhost:5173`

---

## 🧪 Running the DSA Test Suite

```bash
cd backend
.venv\Scripts\pytest tests/test_full_system.py tests/test_dsa_workflow.py -v
```

All 13 integration tests verify the Linked List, FIFO Queue, Min-Heap Priority Queue, LIFO Stack, and Matchmaking lifecycle.
