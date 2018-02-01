# -*- coding: utf-8 -*-

from pyee.base import EventEmitter

from concurrent.futures import ThreadPoolExecutor

__all__ = ['ExecutorEventEmitter']


class ExecutorEventEmitter(EventEmitter):
    """An event emitter class which runs handlers in a concurrent.futures
    executor.

    By default, this class creates a default ThreadPoolExecutor, but
    a custom executor may also be passed in explicitly.
    """
    def __init__(self, executor=None):
        super().__init__()
        if executor:
            self._executor = executor
        else:
            self._executor = ThreadPoolExecutor()

    def _emit_run(self, f, args, kwargs):
        future = self._executor.submit(f, *args, **kwargs)

        @future.add_done_callback
        def _callback(f):
            exc = f.exception()
            if exc:
                self.emit('error', exc)

    def emit(self, event, *args, **kwargs):
        """Emit ``event``, passing ``*args`` and ``**kwargs`` to each attached
        function. Returns ``True`` if any functions are attached to ``event``;
        otherwise returns ``False``.

        This class runs all emitted events in a concurrent.futures executor.
        errors captured by the resulting Future are automatically emitted on
        the ``error`` event.
        """

        super(self).emit(event, *args, **kwargs)