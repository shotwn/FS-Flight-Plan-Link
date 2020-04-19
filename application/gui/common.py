import asyncio
import threading
from PySide2.QtCore import Signal
from loguru import logger


class GUICommon:
    act = Signal(dict)

    def __init__(self, gui_root):
        super().__init__()
        self.gui_root = gui_root
        self.act.connect(self._act)

    def _act(self, params):
        """
        Signal receiver:
        params: a list with following values
            [0] : action, a callable.
            [1] : args, args to pass on callable.
            [2] : kwargs, kwargs to pass on callable.

        raises:
            ValueError: if params len > 3 or len == 0
            Exception: Other exceptions from the action.
        """

        length = len(params)
        if length == 0:
            raise ValueError

        logger.debug(f"GUI will emit {str(params[0])}")

        action = params[0]
        args = []
        kwargs = {}

        if length > 1:
            args = params[1]

        if length > 2:
            kwargs = params[2]

        if length > 3:
            raise ValueError

        action(*args, **kwargs)

    def pack_and_emit(self, func, *args, **kwargs):
        logger.debug(f'Pack and emit is being used. {[func, args, kwargs]}')
        return self.act.emit([func, args, kwargs])

    def run_async_payload(self, func, *args, **kwargs):
        """ Wrapper to be run in different thread """

        try:
            future = asyncio.run_coroutine_threadsafe(
                func(*args, **kwargs), loop=self.gui_root.fslapp.server.loop
            )
            result = future.result()
            logger.debug(result)
            return result
        except asyncio.TimeoutError as err:
            logger.error(err)
        except Exception as exc:
            logger.error(exc)
            raise exc

    def run_async(self, func, *args, **kwargs):
        """ Call async functions and run them in an asyncio thread. """
        thread = threading.Thread(target=self.run_async_payload, args=(func, *args), kwargs=kwargs)
        thread.start()
