from reactivex import scheduler
import threading
import functools
from typing import Optional
from reactivex.scheduler import ThreadPoolScheduler
from concurrent.futures import ThreadPoolExecutor


def named_thread_factory(target, name) -> threading.Thread:
    return threading.Thread(target=target, daemon=True, name=name)


class NamedNewThreadScheduler(scheduler.NewThreadScheduler):
    def __init__(self, name: str):
        return super().__init__(functools.partial(named_thread_factory, name=name))


class PrefixedThreadPoolScheduler(ThreadPoolScheduler):
    def __init__(
        self, max_workers: Optional[int] = None, thread_name_prefix: Optional[str] = ""
    ) -> None:
        super().__init__(max_workers)
        self.executor: ThreadPoolExecutor = ThreadPoolExecutor(
            max_workers=max_workers, thread_name_prefix=thread_name_prefix or ""
        )


class NamedEventLoopScheduler(scheduler.EventLoopScheduler):
    def __init__(self, name: str, exit_if_empty: bool = False):
        return super().__init__(
            thread_factory=lambda target: threading.Thread(
                target=target, daemon=True, name=name
            ),
            exit_if_empty=exit_if_empty,
        )
