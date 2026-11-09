"""Custom Hash Table Implementation for Instant Driver Lookup.

Demonstrates an O(1) Key-Value Hash Table with Chaining for collision resolution.
Uses an array of buckets, where each bucket is a Singly Linked List of HashNodes.
Academic Demonstration of:
1. Hash Function (Modulo Hashing)
2. Collision Resolution via Chaining
3. Constant-time O(1) Average Lookup vs O(N) Linked List Traversal
"""

from typing import Any, Dict, List, Optional


class HashNode:
    """Node representing a Key-Value pair in the collision chain."""

    def __init__(self, key: int, value: Dict[str, Any], next_node: Optional["HashNode"] = None):
        self.key: int = key
        self.value: Dict[str, Any] = value
        self.next: Optional["HashNode"] = next_node


class DriverHashTable:
    """Custom Hash Table with Chaining for O(1) Driver Lookup."""

    def __init__(self, capacity: int = 10):
        self.capacity: int = capacity
        # Array of buckets initialized to None
        self.buckets: List[Optional[HashNode]] = [None] * capacity
        self._count: int = 0

    def _hash(self, key: int) -> int:
        """Hash function using modulo arithmetic: index = key % capacity."""
        return abs(hash(key)) % self.capacity

    def put(self, key: int, value: Dict[str, Any]) -> None:
        """Inserts or updates a key-value pair in O(1) average time."""
        index = self._hash(key)
        head = self.buckets[index]

        # Check if key already exists in this bucket chain; update if found
        current = head
        while current is not None:
            if current.key == key:
                current.value = value
                return
            current = current.next

        # Key not found; insert new node at the head of the chain (O(1) insertion)
        new_node = HashNode(key=key, value=value, next_node=head)
        self.buckets[index] = new_node
        self._count += 1

    def get(self, key: int) -> Optional[Dict[str, Any]]:
        """Retrieves a driver by key (driver_id) in O(1) average time."""
        index = self._hash(key)
        current = self.buckets[index]

        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        return None

    def delete(self, key: int) -> bool:
        """Deletes a key-value pair from the hash table."""
        index = self._hash(key)
        current = self.buckets[index]
        prev = None

        while current is not None:
            if current.key == key:
                if prev is None:
                    # Target is head of bucket chain
                    self.buckets[index] = current.next
                else:
                    prev.next = current.next
                self._count -= 1
                return True
            prev = current
            current = current.next

        return False

    def size(self) -> int:
        """Returns the total number of items in the hash table."""
        return self._count

    def display_buckets(self) -> List[Dict[str, Any]]:
        """Returns a visual representation of all buckets and their collision chains."""
        result = []
        for i in range(self.capacity):
            chain = []
            current = self.buckets[i]
            while current is not None:
                chain.append({
                    "driver_id": current.key,
                    "driver_name": current.value.get("driver_name", ""),
                    "vehicle_number": current.value.get("vehicle_number", "")
                })
                current = current.next

            result.append({
                "bucket_index": i,
                "chain_length": len(chain),
                "chain": chain
            })
        return result
