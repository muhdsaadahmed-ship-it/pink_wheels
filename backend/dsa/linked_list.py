"""Custom Singly Linked List Implementation for Driver Registration.

This is an academic demonstration of a Singly Linked List.
No Python built-in lists are used for internal node chaining.
"""

from typing import Any, Dict, List, Optional


class DriverNode:
    """Node representing a registered driver in the Singly Linked List."""

    def __init__(
        self,
        driver_id: int,
        driver_name: str,
        phone_number: str,
        vehicle_number: str,
        current_latitude: float,
        current_longitude: float,
        is_available: bool = True,
        next_node: Optional["DriverNode"] = None,
    ):
        self.driver_id = driver_id
        self.driver_name = driver_name
        self.phone_number = phone_number
        self.vehicle_number = vehicle_number
        self.current_latitude = current_latitude
        self.current_longitude = current_longitude
        self.is_available = is_available
        self.next: Optional["DriverNode"] = next_node

    def to_dict(self) -> Dict[str, Any]:
        """Convert node data to dictionary format for API responses."""
        return {
            "driver_id": self.driver_id,
            "driver_name": self.driver_name,
            "phone_number": self.phone_number,
            "vehicle_number": self.vehicle_number,
            "current_latitude": self.current_latitude,
            "current_longitude": self.current_longitude,
            "is_available": self.is_available,
        }


class DriverLinkedList:
    """Singly Linked List for managing registered drivers."""

    def __init__(self):
        self.head: Optional[DriverNode] = None
        self._count: int = 0

    def append(self, driver_data: Dict[str, Any]) -> DriverNode:
        """Appends a new driver node to the end of the linked list."""
        new_node = DriverNode(
            driver_id=driver_data["driver_id"],
            driver_name=driver_data["driver_name"],
            phone_number=driver_data.get("phone_number", ""),
            vehicle_number=driver_data.get("vehicle_number", ""),
            current_latitude=float(driver_data.get("current_latitude", 24.8607)),
            current_longitude=float(driver_data.get("current_longitude", 67.0011)),
            is_available=driver_data.get("is_available", True),
        )

        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

        self._count += 1
        return new_node

    def insert(self, index: int, driver_data: Dict[str, Any]) -> DriverNode:
        """Inserts a new driver node at a specific index."""
        if index < 0 or index > self._count:
            raise IndexError("Index out of bounds")

        new_node = DriverNode(
            driver_id=driver_data["driver_id"],
            driver_name=driver_data["driver_name"],
            phone_number=driver_data.get("phone_number", ""),
            vehicle_number=driver_data.get("vehicle_number", ""),
            current_latitude=float(driver_data.get("current_latitude", 24.8607)),
            current_longitude=float(driver_data.get("current_longitude", 67.0011)),
            is_available=driver_data.get("is_available", True),
        )

        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for _ in range(index - 1):
                if current is not None:
                    current = current.next
            if current is not None:
                new_node.next = current.next
                current.next = new_node

        self._count += 1
        return new_node

    def delete(self, driver_id: int) -> bool:
        """Deletes a driver node by driver_id. Returns True if deleted, False otherwise."""
        if self.head is None:
            return False

        # If head is the target
        if self.head.driver_id == driver_id:
            self.head = self.head.next
            self._count -= 1
            return True

        current = self.head
        while current.next is not None:
            if current.next.driver_id == driver_id:
                current.next = current.next.next
                self._count -= 1
                return True
            current = current.next

        return False

    def search(self, driver_id: int) -> Optional[DriverNode]:
        """Searches for a driver node by driver_id. Returns node or None."""
        current = self.head
        while current is not None:
            if current.driver_id == driver_id:
                return current
            current = current.next
        return None

    def traverse(self) -> List[Dict[str, Any]]:
        """Traverses the linked list from head to tail and returns list of driver dicts."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.to_dict())
            current = current.next
        return result

    def display(self) -> str:
        """Returns a human-readable visual chain representation of the linked list."""
        if self.head is None:
            return "Head -> NULL"
        elements = []
        current = self.head
        while current is not None:
            elements.append(f"[{current.driver_id}: {current.driver_name} ({'Available' if current.is_available else 'Busy'})]")
            current = current.next
        return " -> ".join(elements) + " -> NULL"

    def size(self) -> int:
        """Returns the total number of registered drivers."""
        return self._count

    def update_availability(self, driver_id: int, is_available: bool) -> bool:
        """Updates the availability status of a registered driver."""
        node = self.search(driver_id)
        if node:
            node.is_available = is_available
            return True
        return False

    def get_available_drivers(self) -> List[DriverNode]:
        """Returns all registered drivers whose availability status is True."""
        available = []
        current = self.head
        while current is not None:
            if current.is_available:
                available.append(current)
            current = current.next
        return available
