import orjson
import reactivex
from reactivex import Observable, Subject, operators
from typing import Any, Callable
from elm_framework_helpers.schedulers import NamedEventLoopScheduler
from websocket_server import WebsocketServer
from logging import getLogger
from reactivex.disposable import CompositeDisposable


logger = getLogger(__name__)


def log_continue(err, _src):
    logger.exception("Error on websocket trigger")
    return reactivex.empty()


class HtmxWebsocketServer(WebsocketServer):
    _new_clients: Subject
    _scheduler: reactivex.abc.SchedulerBase
    subscription: CompositeDisposable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._new_clients = Subject()
        self.set_fn_new_client(lambda *_: self._new_clients.on_next(None))
        self._scheduler = NamedEventLoopScheduler("htmx_websocket_server")
        self.subscription = CompositeDisposable()

    def server_close(self):
        self.subscription.dispose()
        self._scheduler.dispose()
        super().server_close()

    def add_action_received(self, trigger_name, cb):
        def on_message_received(client, server, message):
            try:
                message = orjson.loads(message)
                if trigger_name == message["HEADERS"]["HX-Trigger"]:
                    cb(message)
            except:
                pass

        self.set_fn_message_received(on_message_received)

    @property
    def scheduler(self):
        return self._scheduler

    def add_string_trigger(
        self,
        src: Observable,
        cb: Callable[[Any], str] | None = None,
        trigger_on_new_client: bool = True,
    ):
        cb = cb or (lambda x: x)
        src = src.pipe(
            operators.observe_on(self._scheduler),
        )
        if trigger_on_new_client:
            src = src.pipe(
                operators.combine_latest(self._new_clients),
                operators.map(
                    lambda x: x[0]
                ),  # don't want value to become a tuple inclusive of the client
            )

        def send(x):
            try:
                self.send_message_to_all(cb(x))
            except Exception as e:
                logger.exception("Error sending socket message")

        self.subscription.add(
            src.pipe(
                operators.catch(log_continue),
                operators.repeat(),
            ).subscribe(send)
        )
