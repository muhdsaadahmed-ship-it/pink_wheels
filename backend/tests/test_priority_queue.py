import pytest

from app.dsa.priority_queue import DriverAllocationEntry, DriverPriorityQueue


def entry(driver_id, eta, ts, distance=1.0):
    return DriverAllocationEntry(
        driver_id=driver_id,
        passenger_request_id="req-1",
        estimated_arrival_time=eta,
        distance=distance,
        request_timestamp=ts,
    )


@pytest.fixture
def pq():
    return DriverPriorityQueue()


def test_push_and_pop_min_first(pq):
    pq.push(entry(1, eta=8.0, ts=100))
    pq.push(entry(2, eta=3.0, ts=200))
    pq.push(entry(3, eta=5.0, ts=300))
    assert pq.pop().driver_id == 2
    assert pq.pop().driver_id == 3
    assert pq.pop().driver_id == 1
    assert pq.is_empty()


def test_peek_does_not_remove(pq):
    pq.push(entry(1, eta=4.0, ts=100))
    assert pq.peek().driver_id == 1
    assert pq.size() == 1


def test_pop_empty_raises(pq):
    with pytest.raises(IndexError):
        pq.pop()


def test_is_empty(pq):
    assert pq.is_empty()
    pq.push(entry(1, eta=1.0, ts=1))
    assert not pq.is_empty()


def test_heapify_produces_valid_order(pq):
    pq.heapify([entry(i, eta=float(10 - i), ts=i) for i in range(10)])
    previous_eta = float("-inf")
    while not pq.is_empty():
        eta = pq.pop().estimated_arrival_time
        assert eta >= previous_eta
        previous_eta = eta


def test_update_priority_reorders(pq):
    pq.push(entry(1, eta=9.0, ts=100))
    pq.push(entry(2, eta=5.0, ts=200))
    assert pq.peek().driver_id == 2
    assert pq.update_priority(1, estimated_arrival_time=2.0) is True
    assert pq.peek().driver_id == 1


def test_update_priority_missing_returns_false(pq):
    assert pq.update_priority(99, estimated_arrival_time=1.0) is False


def test_remove_entry(pq):
    pq.push(entry(1, eta=3.0, ts=100))
    pq.push(entry(2, eta=4.0, ts=200))
    assert pq.remove(1) is True
    assert pq.peek().driver_id == 2
    assert pq.remove(99) is False


def test_tie_break_by_request_timestamp_then_driver_id(pq):
    pq.push(entry(3, eta=3.0, ts=200))
    pq.push(entry(2, eta=3.0, ts=100))
    pq.push(entry(1, eta=3.0, ts=100))
    assert pq.pop().driver_id == 1
    assert pq.pop().driver_id == 2
    assert pq.pop().driver_id == 3


def test_unavailable_driver_can_be_marked(pq):
    pq.push(entry(1, eta=3.0, ts=100))
    pq.update_priority(1, driver_availability=False)
    assert pq.display()[0]["driver_availability"] is False
