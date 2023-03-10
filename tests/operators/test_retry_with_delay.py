from elm_framework_helpers.operators.retry_with_delay import resettable_counter, retry_with_delay
import pytest

from reactivex.notification import OnError
from reactivex.testing import ReactiveTest, TestScheduler
from reactivex.testing.subscription import Subscription
from reactivex import operators, interval, concat, combine_latest, of
import reactivex
import pytest
from elm_framework_helpers.operators import ignore_errors

on_next = ReactiveTest.on_next
on_error = ReactiveTest.on_error
on_completed = ReactiveTest.on_completed
subscribe = ReactiveTest.subscribe

def test_retry_with_delay_with_single_retry():
    # Arrange
    test_scheduler = TestScheduler()
    source = test_scheduler.create_cold_observable(
        ReactiveTest.on_next(100, 'a'),
        ReactiveTest.on_next(200, 'b'),
        ReactiveTest.on_error(300, Exception('boom')),
    )
    delay_pattern = [10, 20, 30]
    reset_after = test_scheduler.create_cold_observable(on_completed(1000))

    # Act
    results = test_scheduler.start(lambda: source.pipe(retry_with_delay(
        resettable_counter(delay_pattern), reset_after
    )))

    # Assert
    assert results.messages == [
        ReactiveTest.on_next(300, 'a'),
        ReactiveTest.on_next(400, 'b'),
        ReactiveTest.on_next(610, 'a'),
        ReactiveTest.on_next(710, 'b'),
        ReactiveTest.on_next(930, 'a'),
    ]

def test_retry_with_delay_with_reset():
    # Arrange
    test_scheduler = TestScheduler()
    source = test_scheduler.create_cold_observable(
        ReactiveTest.on_next(100, 'a'),
        ReactiveTest.on_error(200, Exception('boom')),
    )
    delay_pattern = (60, 130, 75)
    reset_after = test_scheduler.create_cold_observable(on_completed(10))

    # Act
    results = test_scheduler.start(lambda: source.pipe(retry_with_delay(
        resettable_counter(delay_pattern), reset_after
    )))

    # Assert
    assert results.messages == [
        ReactiveTest.on_next(300, 'a'),
        ReactiveTest.on_next(560, 'a'),
        ReactiveTest.on_next(820, 'a'),
    ]


def test_resettable_counter_with_list():
    # Arrange
    values = [1, 2, 3, 4, 5]
    gen = resettable_counter(values)
    
    # Act / Assert
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3
    assert gen.send(0) == None
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3
    assert next(gen) == 4
    assert next(gen) == 5
    with pytest.raises(Exception) as exc: # TODO this behaves the way we expect but fails to be caught if using pytest.raises(StopIteration).. Not sure why
        next(gen)
    assert exc

def test_resettable_counter_with_infinite_iterator():
    # Arrange
    def i():
        i = 0
        while True:
            i += 1
            yield i
    gen = resettable_counter(i)
    
    # Act / Assert
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3
    assert gen.send(0) == None
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3
    assert next(gen) == 4
    assert next(gen) == 5
    assert next(gen) == 6
    assert next(gen) == 7
    assert gen.send(0) == None
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3
    assert next(gen) == 4
    assert next(gen) == 5
    assert next(gen) == 6

def test_resettable_counter_with_infinite_loop():
    # Arrange
    values = [1, 2, 3]
    gen = resettable_counter(values, infinite_behavior="loop")
    
    # Act / Assert
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3
    assert gen.send(0) == None
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3
    assert next(gen) == 1
    assert gen.send(0) == None
    assert next(gen) == 1

def test_resettable_counter_with_infinite_last():
    # Arrange
    values = [1, 2, 3]
    gen = resettable_counter(values, infinite_behavior="last")
    
    # Act / Assert
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3
    assert gen.send(0) == None
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3
    assert next(gen) == 3
    assert next(gen) == 3
    assert next(gen) == 3
    assert next(gen) == 3
    assert gen.send(0) == None
    assert next(gen) == 1
