import re
import importlib
import json
import base64
import time
import uuid
import threading
import asyncio
from aiohttp import web
import aiohttp_cors
from loguru import logger
from server.plan import Plan
from server.settings import Settings
import server.exceptions
import server.events
import server.database
from server.json_encoder import json_encoder

DEFAULT_SETTINGS = {
    'pilot': {
        'name': 'ENTER YOUR NAME',
        'base': 'BASE'
    },
    'exporters': []
}


class FSLServer:
    """
    Initiates:
        available_exporters: ``dict`` with keys as module id's.
            module_id: module.
        exporters: ``list`` of initiated exporters.
    """
    def __init__(self, settings=None):
        self.available_exporters = {}
        self.exporters = []
        self.app = web.Application()
        self.cors = aiohttp_cors.setup(self.app)
        self.events = server.events.Events()
        if settings:
            self.settings = settings
        else:
            self.settings = Settings('.\\settings.json', DEFAULT_SETTINGS)
        self.define_routes()
        self.import_available_exporters()
        self.runner = web.AppRunner(self.app)
        self.active_plan = None
        self.database = server.database.Database()

    def import_available_exporters(self):
        vpilot = importlib.import_module('server.export.vpilot')
        self.available_exporters[vpilot.ID] = vpilot
        vatsim = importlib.import_module('server.export.vatsim')
        self.available_exporters[vatsim.ID] = vatsim

    def initiate_exporters(self):
        """ Read exporters from settings.

            exporter_options: A ``dict`` with following keys.
                id: id defined in module.ID
                options: options field to pass on the exporter.
                uuid: unique string as a unique key.
        """
        settings_exporters = self.settings.get('exporters')
        self.exporters = []
        for exporter_options in settings_exporters:
            module = self.available_exporters.get(exporter_options['id'])
            if not module:
                # Not found.
                continue

            exporter = module.CLASS(self, exporter_options['options'])
            self.exporters.append(exporter)

    def add_exporter(self, module_id, options={}):
        module = self.available_exporters.get(module_id)
        if not module:
            logger.debug(f"Cannot add exporter. Module doesn't exist: {module_id}")
            return False

        default_options_func = getattr(module, 'default_options', None)
        if default_options_func:
            merged_options = default_options_func(options)
        else:
            merged_options = options

        exporters = self.settings.get('exporters')
        exporters.append({
            'id': module_id,
            'options': merged_options,
            'uuid': str(uuid.uuid4())
        })
        self.settings.set(exporters, 'exporters')
        self.initiate_exporters()

    def define_routes(self):
        self.app.add_routes(
            [
                web.get('/', self.test),
            ]
        )
        plan_resource = self.cors.add(self.app.router.add_resource("/plan"))
        self.cors.add(plan_resource.add_route("POST", self.post_plan), {
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*"
            ),
        })

    async def start_site(self):
        """ Async function to setup site runner and start the site. """
        await self.runner.setup()
        site = web.TCPSite(self.runner, '127.0.0.1', 32030)
        await site.start()

    def server_thread_runner(self):
        """ Blocking, run the server loop """
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.start_site())
        self.loop.run_forever()

    def start(self):
        """ Blocking, shortcut function to run the site. """
        web.run_app(self.app, host='127.0.0.1', port=32030)

    async def test(self, request):
        headers = {}
        headers['Access-Control-Allow-Origin'] = '*'
        return web.Response(text='Test', headers=headers)

    async def basic_auth(self, headers):
        reg = r'^Basic (.*?)$'
        if 'Authorization' not in headers:
            return False

        match = re.match(reg, headers['Authorization'])

        if not match:
            return False

        groups = match.groups()

        if len(groups) > 1:
            return False

        auth = groups[0].encode()
        # print(pin)

        decoded_auth = base64.b64decode(auth)
        decoded_auth = decoded_auth.decode("utf-8").split(':')
        if len(decoded_auth) != 2:
            return False

        # print(decoded_auth)
        decoded_auth_user_name = decoded_auth[0]
        decoded_auth_user_password = decoded_auth[1]

        if decoded_auth_user_name != 'User':
            return False

        if decoded_auth_user_password != self.settings.get('pin'):
            return False

        return True

    async def set_active_plan(self, plan):
        self.active_plan = plan
        await self.events.run_async_observers_for('plan_activated', plan)

    async def post_plan(self, request):
        headers = {}
        # headers['Access-Control-Allow-Origin'] = '*'

        if not await self.basic_auth(request.headers):
            return web.HTTPUnauthorized(headers=headers)

        req_data = await request.json()
        try:
            plan = Plan(req_data["plan"], self)

            secondary_plan = None
            if 'secondary_plan' in req_data:
                secondary_plan = Plan(req_data["secondary_plan"], self)
                if not plan.get('alternate'):
                    plan.plan['alternate'] = secondary_plan.get("destination")

        except server.exceptions.MissingField as exc:
            return web.HTTPUnprocessableEntity(body=json.dumps({
                'error': exc.message
            }))

        await self.set_active_plan(plan)

        export_errors = await self.export(plan)
        body = {
            'plan': plan,
            'secondary_plan': secondary_plan,
            'export_errors': export_errors
        }

        await plan.populate_rich_data()
        logger.debug(plan)
        await self.events.run_async_observers_for('post_plan', plan)
        return web.Response(body=json.dumps(body, default=json_encoder), headers=headers)
        # return web.Response(body='ok')

    async def export(self, plan):
        errors = {}
        for exporter in self.exporters:
            try:
                await exporter.export(plan)
            except server.exceptions.HandledException as exc:
                print(f'Exporter error for {exporter["name"]}: {exc}')
                errors[exporter['name']] = exc.message

        return errors


if __name__ == '__main__':
    SERVER = FSLServer()
    SERVER.settings.set([], 'exporters')
    SERVER.add_exporter('vatsim')
    SERVER.add_exporter('vpilot')
    # SERVER.start()
    t = threading.Thread(target=SERVER.server_thread_runner, daemon=True)
    t.start()
    while True:
        print('blockss')
        # time.sleep(1)
