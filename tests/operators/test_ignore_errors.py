import time
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


def test_ignore_errors():
    scheduler = TestScheduler()
    source = scheduler.create_cold_observable(on_next(50, 42), on_error(300, "ABC"))
    result = scheduler.start(lambda: source.pipe(ignore_errors()))

    assert result.messages == [on_next(250, 42), on_completed(500)]
