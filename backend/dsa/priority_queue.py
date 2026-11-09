"""Custom Binary Min-Heap Priority Queue for Driver Matchmaking.

Prioritizes drivers with the lowest Estimated Time of Arrival (ETA).
Uses distance as a tie-breaker when ETAs are identical.
Custom binary min-heap implemented from scratch (NO heapq or queue.PriorityQueue).
"""

from typing import Any, Dict, List, Optional


class DriverPriorityQueue:
    """Custom Binary Min-Heap implementation for Driver Selection."""

    def __init__(self):
        # Internal array representation of the binary min-heap
        self.heap: List[Dict[str, Any]] = []

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left_child(self, i: int) -> int:
        return 2 * i + 1

    def _right_child(self, i: int) -> int:
        return 2 * i + 2

    def _is_higher_priority(self, a: Dict[str, Any], b: Dict[str, Any]) -> bool:
        """Determines if driver 'a' has higher priority (smaller ETA, then smaller distance)."""
        # Primary key: ETA (minutes)
        eta_a = a.get("eta_minutes", 0.0)
        eta_b = b.get("eta_minutes", 0.0)
        if eta_a != eta_b:
            return eta_a < eta_b

        # Secondary tie-breaker: Distance (km)
        dist_a = a.get("distance_km", 0.0)
        dist_b = b.get("distance_km", 0.0)
        if dist_a != dist_b:
            return dist_a < dist_b

        # Tertiary tie-breaker: driver_id for deterministic ordering
        return a.get("driver_id", 0) < b.get("driver_id", 0)

    def _sift_up(self, index: int) -> None:
        """Move element at index up until min-heap property is satisfied."""
        current = index
        while current > 0:
            parent_idx = self._parent(current)
            if self._is_higher_priority(self.heap[current], self.heap[parent_idx]):
                # Swap current with parent
                self.heap[current], self.heap[parent_idx] = self.heap[parent_idx], self.heap[current]
                current = parent_idx
            else:
                break

    def _sift_down(self, index: int) -> None:
        """Move element at index down until min-heap property is satisfied."""
        smallest = index
        size = len(self.heap)

        while True:
            left = self._left_child(smallest)
            right = self._right_child(smallest)
            candidate = smallest

            if left < size and self._is_higher_priority(self.heap[left], self.heap[candidate]):
                candidate = left

            if right < size and self._is_higher_priority(self.heap[right], self.heap[candidate]):
                candidate = right

            if candidate != smallest:
                self.heap[smallest], self.heap[candidate] = self.heap[candidate], self.heap[smallest]
                smallest = candidate
            else:
                break

    def push(self, item: Dict[str, Any]) -> None:
        """Inserts a new driver candidate into the min-heap."""
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self) -> Optional[Dict[str, Any]]:
        """Removes and returns the highest priority driver (lowest ETA)."""
        if self.is_empty():
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        # Move last element to root and sift down
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root

    def peek(self) -> Optional[Dict[str, Any]]:
        """Returns the highest priority driver without removing it."""
        if self.is_empty():
            return None
        return self.heap[0]

    def is_empty(self) -> bool:
        """Returns True if the min-heap is empty."""
        return len(self.heap) == 0

    def size(self) -> int:
        """Returns total number of drivers currently in the priority queue."""
        return len(self.heap)

    def heapify(self, items: List[Dict[str, Any]]) -> None:
        """Builds a min-heap from an arbitrary list of driver items in O(N) time."""
        self.heap = [dict(item) for item in items]
        if len(self.heap) <= 1:
            return
        start_idx = self._parent(len(self.heap) - 1)
        for i in range(start_idx, -1, -1):
            self._sift_down(i)

    def update_priority(self, driver_id: int, new_eta: float, new_distance: float) -> bool:
        """Updates the priority of a specific driver and restores min-heap order."""
        for i, item in enumerate(self.heap):
            if item.get("driver_id") == driver_id:
                item["eta_minutes"] = new_eta
                item["distance_km"] = new_distance
                # Sift up or down as needed
                self._sift_up(i)
                self._sift_down(i)
                return True
        return False

    def display(self) -> List[Dict[str, Any]]:
        """Returns the drivers in sorted priority order without mutating internal state."""
        # Make a copy of the heap and pop one by one
        backup = [dict(x) for x in self.heap]
        temp_pq = DriverPriorityQueue()
        temp_pq.heap = [dict(x) for x in self.heap]
        ordered = []
        while not temp_pq.is_empty():
            ordered.append(temp_pq.pop())
        self.heap = backup
        return ordered
