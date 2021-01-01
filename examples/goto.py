#!/usr/bin/env python3

import asyncio
from mavsdk import System
import sys

async def run(latitude, longitude, altitude):
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        terrain_altitude = terrain_info.absolute_altitude_m
        print(f"Terrain altitude at home location is: {terrain_altitude:.0f} meters AMSL")
        break

    await asyncio.sleep(1)
    flying_alt = terrain_altitude + altitude
    print(f"New flying altitude is: {flying_alt:.0f} meters AMSL")
    #goto_location() takes Absolute MSL altitude
    await drone.action.goto_location(latitude, longitude, flying_alt, 0)

if __name__ == "__main__":

    if len(sys.argv) != 4:
    	sys.stderr.write("Invalid number of arguments.\n")
    	sys.stderr.write("Usage: %s latitude[degrees] longitude[degrees] altitude_rel[meters]\n" % (sys.argv[0], ))
    	sys.exit(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(eval(sys.argv[1]), eval(sys.argv[2]), eval(sys.argv[3])))
