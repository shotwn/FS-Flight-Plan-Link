import csv
import os
import aiohttp
import asyncio
import aiosqlite

DATABASE = 'data.db'

AIRPORTS_URL = 'https://ourairports.com/data/airports.csv'
AIRPORTS_HEADERS = [
    'id',
    'ident',
    'type',
    'name',
    'latitude_deg',
    'longitude_deg',
    'elevation_ft',
    'continent',
    'iso_country',
    'iso_region',
    'municipality',
    'scheduled_service',
    'gps_code',
    'iata_code',
    'local_code',
    'home_link',
    'wikipedia_link',
    'keywords'
]

NAVAIDS_URL = 'https://ourairports.com/data/navaids.csv'
NAVAIDS_HEADERS = [
    'id',
    'filename',
    'ident',
    'name',
    'type',
    'frequency_khz',
    'latitude_deg',
    'longitude_deg',
    'elevation_ft',
    'iso_country',
    'dme_frequency_khz',
    'dme_channel',
    'dme_latitude_deg',
    'dme_longitude_deg',
    'dme_elevation_ft',
    'slaved_variation_deg',
    'magnetic_variation_deg',
    'usageType',
    'power',
    'associated_airport'
]

AIRPORT_FREQUENCIES_URL = 'https://ourairports.com/data/airport-frequencies.csv'
AIRPORT_FREQUENCIES_HEADERS = [
    'id',
    'airport_ref',
    'airport_ident',
    'type',
    'description',
    'frequency_mhz'
]

RUNWAYS_URL = 'https://ourairports.com/data/runways.csv'
RUNWAYS_HEADERS = [
    'id',
    'airport_ref',
    'airport_ident',
    'length_ft',
    'width_ft',
    'surface',
    'lighted',
    'closed',
    'le_ident',
    'le_latitude_deg',
    'le_longitude_deg',
    'le_elevation_ft',
    'le_heading_degT',
    'le_displaced_threshold_ft',
    'he_ident',
    'he_latitude_deg',
    'he_longitude_deg',
    'he_elevation_ft',
    'he_heading_degT',
    'he_displaced_threshold_ft'
]


async def fetch(session, url, db, table_name, table_headers):
    async with session.get(url) as response:
        csv_str = await response.text()
        csv_data = csv.DictReader(csv_str.splitlines())
        to_db = []
        for col in csv_data:
            to_db.append(tuple(col.values()))

        q_marks = ['?' for x in range(len(table_headers))]
        await db.executemany(f'INSERT INTO {table_name} ({", ".join(table_headers)}) VALUES ({", ".join(q_marks)});', to_db)
        await db.commit()


async def create_table(db, table_name, fields):
    await db.execute(f'DROP TABLE IF EXISTS {table_name}')
    await db.execute(f'CREATE TABLE {table_name} ({", ".join(fields)})')


async def main():
    async with aiosqlite.connect(DATABASE) as db:
        await create_table(db, 'airports', AIRPORTS_HEADERS)
        await create_table(db, 'navaids', NAVAIDS_HEADERS)
        await create_table(db, 'airport_frequencies', AIRPORT_FREQUENCIES_HEADERS)
        await create_table(db, 'runways', RUNWAYS_HEADERS)

        async with aiohttp.ClientSession() as session:
            await asyncio.wait([
                fetch(session, AIRPORTS_URL, db, 'airports', AIRPORTS_HEADERS),
                fetch(session, NAVAIDS_URL, db, 'navaids', NAVAIDS_HEADERS),
                fetch(session, AIRPORT_FREQUENCIES_URL, db, 'airport_frequencies', AIRPORT_FREQUENCIES_HEADERS),
                fetch(session, RUNWAYS_URL, db, 'runways', RUNWAYS_HEADERS)
            ])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
