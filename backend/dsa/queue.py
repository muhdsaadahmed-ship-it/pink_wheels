"""Custom FIFO Queue Implementation for Ride Request Management.

Demonstrates First-In, First-Out (FIFO) queue using custom Node pointers.
No built-in Python queue module or list pop(0) replacement is used.
"""

from typing import Any, Dict, List, Optional


class QueueNode:
    """Node representing an element in the FIFO Queue."""

    def __init__(self, data: Dict[str, Any], next_node: Optional["QueueNode"] = None):
        self.data: Dict[str, Any] = data
        self.next: Optional["QueueNode"] = next_node


class RideQueue:
    """Custom FIFO Queue for incoming ride requests."""

    def __init__(self):
        self.front: Optional[QueueNode] = None
        self.rear: Optional[QueueNode] = None
        self._count: int = 0

    def enqueue(self, item: Dict[str, Any]) -> None:
        """Adds a ride request to the back (rear) of the queue."""
        new_node = QueueNode(data=item)
        if self.rear is None:
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._count += 1

    def dequeue(self) -> Optional[Dict[str, Any]]:
        """Removes and returns the oldest ride request from the front of the queue."""
        if self.is_empty():
            return None
        
        target = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self._count -= 1
        return target.data

    def peek(self) -> Optional[Dict[str, Any]]:
        """Returns the oldest ride request without removing it."""
        if self.is_empty():
            return None
        return self.front.data

    def is_empty(self) -> bool:
        """Returns True if queue contains no elements, False otherwise."""
        return self.front is None

    def size(self) -> int:
        """Returns the total number of items currently in the queue."""
        return self._count

    def display(self) -> List[Dict[str, Any]]:
        """Traverses the queue from front to rear and returns items in FIFO order."""
        result = []
        current = self.front
        while current is not None:
            result.append(current.data)
            current = current.next
        return result
