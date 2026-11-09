"""Custom LIFO Stack Implementation for Ride Activity History.

Demonstrates Last-In, First-Out (LIFO) stack using custom Node pointers.
Tracks ride events (requested, offered, accepted, rejected, completed, cancelled).
The most recent event is always at the top of the stack.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


class StackNode:
    """Node representing an activity event in the LIFO Stack."""

    def __init__(self, data: Dict[str, Any], next_node: Optional["StackNode"] = None):
        self.data: Dict[str, Any] = data
        self.next: Optional["StackNode"] = next_node


class ActivityStack:
    """Custom LIFO Stack for ride activity logging and audit trail."""

    def __init__(self):
        self.top: Optional[StackNode] = None
        self._count: int = 0

    def push(self, activity: Dict[str, Any]) -> None:
        """Pushes a new ride activity onto the top of the stack."""
        # Ensure timestamp is recorded
        if "timestamp" not in activity:
            activity["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_node = StackNode(data=activity, next_node=self.top)
        self.top = new_node
        self._count += 1

    def pop(self) -> Optional[Dict[str, Any]]:
        """Pops and returns the most recent ride activity from the top of the stack."""
        if self.is_empty():
            return None
        target = self.top
        self.top = self.top.next
        self._count -= 1
        return target.data

    def peek(self) -> Optional[Dict[str, Any]]:
        """Returns the most recent ride activity without removing it."""
        if self.is_empty():
            return None
        return self.top.data

    def is_empty(self) -> bool:
        """Returns True if the stack has no elements."""
        return self.top is None

    def size(self) -> int:
        """Returns the number of activity records in the stack."""
        return self._count

    def display(self) -> List[Dict[str, Any]]:
        """Traverses the stack from top to bottom (most recent first)."""
        result = []
        current = self.top
        while current is not None:
            result.append(current.data)
            current = current.next
        return result
