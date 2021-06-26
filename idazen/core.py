import asyncio
import logging
import struct

from bleak import BleakClient
from bleak import BleakScanner


UUID_HEIGHT = "99fa0021-338a-1024-8a49-009c0215f78a"
UUID_COMMAND = "99fa0002-338a-1024-8a49-009c0215f78a"

UP = struct.pack("<H", 71)
DOWN = struct.pack("<H", 70)
STOP = struct.pack("<H", 255)

MIN_HEIGHT_CM = 62
DELTA = 0.6
SLEEP_STEP = 0.2
DESK_KEYWORD = "Desk "


def to_native(cm):
    return int((cm - MIN_HEIGHT_CM) * 100)


def to_cm(native):
    return (int(native) / 100) + MIN_HEIGHT_CM


async def scan(timeout=10):
    desks = {}
    for device in await BleakScanner.discover(timeout=timeout):
        if device.name.startswith(DESK_KEYWORD):
            desks[device.name] = device.address
    return desks


async def move(desk, target):
    async with BleakClient(desk, timeout=10) as client:

        async def height():
            data = await client.read_gatt_char(UUID_HEIGHT)
            pos, speed = struct.unpack("<Hh", data)
            return to_cm(pos)

        async def up():
            await client.write_gatt_char(UUID_COMMAND, UP, response=True)

        async def down():
            await client.write_gatt_char(UUID_COMMAND, DOWN, response=True)

        async def stop():
            await client.write_gatt_char(UUID_COMMAND, STOP, response=True)

        h = await height()
        logging.debug(f"start height {h}")

        while abs(target - h) > DELTA:
            logging.debug(f"current height {h}")

            if target > h:
                await up()
            else:
                await down()

            await asyncio.sleep(SLEEP_STEP)
            h = await height()

        await stop()

    logging.debug(f"final height {h}")
    return h
