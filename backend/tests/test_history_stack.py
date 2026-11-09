import pytest

from app.dsa.history_stack import HistoryStack


@pytest.fixture
def stack():
    return HistoryStack("test", max_depth=3)


def test_push_and_peek(stack):
    stack.push({"action": "login"})
    stack.push({"action": "search"})
    assert stack.peek()["action"] == "search"
    assert stack.size() == 2


def test_pop_lifo_order(stack):
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2
    assert stack.pop() == 1


def test_pop_empty_raises(stack):
    with pytest.raises(IndexError):
        stack.pop()


def test_is_empty(stack):
    assert stack.is_empty()
    stack.push("x")
    assert not stack.is_empty()


def test_max_depth_trims_oldest(stack):
    stack.push(1)
    stack.push(2)
    stack.push(3)
    stack.push(4)
    assert stack.size() == 3
    assert stack.display() == [4, 3, 2]


def test_display_returns_most_recent_first(stack):
    stack.push("a")
    stack.push("b")
    assert stack.display() == ["b", "a"]


def test_peek_empty_returns_none(stack):
    assert stack.peek() is None
