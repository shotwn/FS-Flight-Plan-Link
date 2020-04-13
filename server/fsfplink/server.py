import re
import importlib
import json
import base64
from aiohttp import web
import aiohttp_cors
from fsfplink.plan import Plan
from fsfplink.settings import Settings
import fsfplink.exceptions
from fsfplink.json import json_encoder

DEFAULT_SETTINGS = {
    'pilot': {
        'name': 'ENTER YOUR NAME',
        'base': 'BASE'
    },
    'vPilot': {
        'export_dir': '.\\'
    }
}


class FSFPLServer:
    def __init__(self):
        self.exporters = []
        self.app = web.Application()
        self.cors = aiohttp_cors.setup(self.app)
        self.settings = Settings('.\\settings.json', DEFAULT_SETTINGS)
        self.define_routes()
        self.fetch_exporters()

    def fetch_exporters(self):
        vpilot = importlib.import_module('fsfplink.export.vpilot')
        self.exporters.append({
            'module': vpilot,
            'name': vpilot.NAME,
            'class': getattr(vpilot, vpilot.CLASSNAME)(self)
        })
        vatsim = importlib.import_module('fsfplink.export.vatsim')
        self.exporters.append({
            'module': vatsim,
            'name': vatsim.NAME,
            'class': getattr(vatsim, vatsim.CLASSNAME)(self)
        })

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

    def start(self):
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

        except fsfplink.exceptions.MissingField as exc:
            return web.HTTPUnprocessableEntity(body=json.dumps({
                'error': exc.message
            }))

        export_errors = await self.export(plan)
        body = {
            'plan': plan,
            'secondary_plan': secondary_plan,
            'export_errors': export_errors
        }

        return web.Response(body=json.dumps(body, default=json_encoder), headers=headers)

    async def export(self, plan):
        errors = {}
        for exporter in self.exporters:
            try:
                await exporter["class"].export(plan)
            except fsfplink.exceptions.HandledException as exc:
                print(f'Exporter error for {exporter["name"]}: {exc}')
                errors[exporter['name']] = exc.message

        return errors


if __name__ == '__main__':
    SERVER = FSFPLServer()
    SERVER.start()
