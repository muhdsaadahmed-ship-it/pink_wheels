import pytest

from app.dsa.linked_list import UserLinkedList, add_user, remove_user


@pytest.fixture
def lst():
    return UserLinkedList("test")


def test_append_and_size(lst):
    lst.append(1, "passenger", "A", "pending", "offline")
    lst.append(2, "passenger", "B", "verified", "offline")
    assert lst.size() == 2
    assert lst.head.user_id == 1
    assert lst.head.next.user_id == 2


def test_insert_at_beginning_and_middle(lst):
    lst.append(1, "passenger", "A", "pending", "offline")
    lst.append(3, "passenger", "C", "pending", "offline")
    lst.insert(1, 2, "passenger", "B", "pending", "offline")
    assert [n.user_id for n in lst.traverse()] == [1, 2, 3]
    lst.insert(0, 0, "passenger", "Z", "pending", "offline")
    assert lst.head.user_id == 0


def test_insert_out_of_range_raises(lst):
    with pytest.raises(IndexError):
        lst.insert(5, 1, "passenger", "A", "pending", "offline")


def test_delete_head_middle_and_missing(lst):
    for i in (1, 2, 3):
        lst.append(i, "passenger", f"U{i}", "pending", "offline")
    assert lst.delete(2) is True
    assert [n.user_id for n in lst.traverse()] == [1, 3]
    assert lst.delete(1) is True
    assert lst.head.user_id == 3
    assert lst.delete(99) is False
    assert lst.size() == 1


def test_search_found_and_not_found(lst):
    lst.append(7, "driver", "D", "verified", "online")
    node = lst.search(7)
    assert node is not None
    assert node.display_name == "D"
    assert node.availability_status == "online"
    assert lst.search(8) is None


def test_traverse_and_display(lst):
    lst.append(1, "passenger", "A", "verified", "offline")
    assert len(lst.traverse()) == 1
    display = lst.display()
    assert display[0]["user_id"] == 1
    assert display[0]["verification_status"] == "verified"


def test_add_and_remove_user_helpers():
    add_user(10, "passenger", "P", "verified")
    add_user(20, "driver", "D", "verified", "online")
    assert remove_user(10, "passenger") is True
    assert remove_user(20, "driver") is True
    assert remove_user(30, "passenger") is False
