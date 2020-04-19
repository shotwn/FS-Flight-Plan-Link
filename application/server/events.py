from loguru import logger
import functools
import asyncio


class Events:
    def __init__(self):
        self.observers = {}

    def run_observers_for(self, event, *args, **kwargs):
        all_observers = self.observers.get(event, None)
        results = {}
        for observer in all_observers:
            if not asyncio.iscoroutinefunction(observer):
                observer(*args, **kwargs)
                result = observer(*args, **kwargs)
                results[observer] = result

        return results

    async def run_async_observers_for(self, event, *args, **kwargs):
        all_observers = self.observers.get(event, None)
        if not all_observers:
            return

        results = {}
        for observer_packed in all_observers:
            observer = observer_packed['observer']
            obs_args = observer_packed.get('args', []) + args
            obs_kwargs = observer_packed.get('kwargs', {})
            obs_kwargs.update(kwargs)
            # observer(obs_args)
            logger.debug(
                f"\nEvent triggered {event}"
                + f"\nObserver: {observer}"
                + f"\nArgs: {obs_args}"
                + f"\nKwargs: {obs_kwargs}"
            )

            if asyncio.iscoroutinefunction(observer):
                result = await observer(*obs_args, **obs_kwargs)
                results[observer] = result
            else:
                loop = asyncio.get_event_loop()
                if obs_kwargs:
                    results[observer] = await loop.run_in_executor(None, functools.partial(observer, *obs_args, **obs_kwargs))
                else:
                    results[observer] = await loop.run_in_executor(None, observer, *obs_args)

        return results

    def on(self, event, observer, *args, **kwargs):
        if event not in self.observers:
            self.observers[event] = []

        self.observers[event].append({
            'observer': observer,
            'args': args,
            'kwargs': kwargs
        })
        print(self.observers)
