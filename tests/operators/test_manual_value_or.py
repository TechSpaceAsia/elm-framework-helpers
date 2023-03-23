import time
from reactivex.notification import OnError
from reactivex.testing import ReactiveTest, TestScheduler
from elm_framework_helpers.operators import manual_value_or_operator

on_next = ReactiveTest.on_next
on_error = ReactiveTest.on_error
on_completed = ReactiveTest.on_completed
subscribe = ReactiveTest.subscribe


def test_manual_value_or_toggle():
    scheduler = TestScheduler()
    manual = scheduler.create_hot_observable(
        on_next(250, 42),
        on_next(300, None),
        on_next(400, 10),
        on_completed(500),
    )
    source = scheduler.create_hot_observable(
        on_next(220, 1),
        on_next(360, 2),
        on_next(370, None),
        on_next(380, 3),
        on_next(410, None),
        on_next(420, 100),
    )

    result = scheduler.start(lambda: manual.pipe(manual_value_or_operator(source)))

    assert result.messages == [
        on_next(250, 42),
        on_next(360, 2),
        on_next(370, None),
        on_next(380, 3),
        on_next(400, 10),
        on_completed(500),
    ]
    assert manual.subscriptions == [subscribe(200, 500)]
    assert source.subscriptions == [subscribe(300, 400)]


def test_manual_value_or_manual_completes_while_using_source():
    scheduler = TestScheduler()
    manual = scheduler.create_hot_observable(
        on_next(250, 42),
        on_next(300, None),
        on_completed(500),
    )
    source = scheduler.create_hot_observable(
        on_next(220, 1),
        on_next(360, 2),
        on_next(370, None),
        on_next(420, 100),
        on_next(520, 100),
    )

    result = scheduler.start(lambda: manual.pipe(manual_value_or_operator(source)))

    assert result.messages == [
        on_next(250, 42),
        on_next(360, 2),
        on_next(370, None),
        on_next(420, 100),
        on_completed(500),
    ]
    assert manual.subscriptions == [subscribe(200, 500)]
    assert source.subscriptions == [subscribe(300, 500)]