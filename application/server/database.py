import aiosqlite


class Database:
    def __init__(self):
        self.database = 'data.db'
        pass

    async def airports(self):
        async with aiosqlite.connect(self.database) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM airports') as cursor:
                return dict(await cursor.fetchone())

    async def airport_from_ident(self, ident):
        async with aiosqlite.connect(self.database) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM airports WHERE ident=?', (ident, )) as cursor:
                airport = await cursor.fetchone()
                if airport:
                    return dict(airport)

    async def navaid_from_ident(self, ident):
        async with aiosqlite.connect(self.database) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM navaids WHERE ident=?', (ident, )) as cursor:
                navaid = await cursor.fetchall()
                if navaid:
                    return navaid

    async def waypoint_from_ident(self, ident):
        async with aiosqlite.connect(self.database) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM waypoints WHERE ident=?', (ident, )) as cursor:
                waypoint = await cursor.fetchall()
                if waypoint:
                    return waypoint

    async def route_from_ident(self, ident):
        async with aiosqlite.connect(self.database) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM routes WHERE ident=?', (ident, )) as cursor:
                route = await cursor.fetchall()
                if route:
                    return route

    async def high_route_from_ident(self, ident):
        async with aiosqlite.connect(self.database) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM high_routes WHERE ident=?', (ident, )) as cursor:
                high_route = await cursor.fetchall()
                if high_route:
                    return high_route
