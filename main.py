#at this function i do fusion and use converrt from geo and to geo

import asyncio
import mavsdk
from mavsdk import System,telemetry
from cordinate_math import geodetic_to_cartesian_ned,cartesian_to_geodetic


async def setup_drone(drone: System):
    """

    :param drone: the connect string to the drone
    :return: print for the user if the drone get global position it start takeoff

    *if have problem with this flag it can easely remove
    """
    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break


async def get_geo_pos(drone):

    """
    :param drone: connect strings
    :return: the current position of the drone at geo
    """
    default_coordinates = (0, 0, 0)
    try:
        async for position in drone.telemetry.position():
            latitude = position.latitude_deg
            longitude = position.longitude_deg
            altitude = position.absolute_altitude_m
            break
    except Exception as e:
        print(f"Error getting location: {e}")
        print("Using default coordinates.")
        return default_coordinates

    return latitude, longitude, altitude




async def takeoff_presedoure(drone,target_altitude):

    """
    :param drone: the connect strings
    :return: takeoff the drone
    """

    #  need to add change to stabilize mode

    await drone.action.set_takeoff_altitude(target_altitude)
    await asyncio.sleep(1)
    print("-- Arming")
    await drone.action.arm()
    await drone.action.takeoff()
    await asyncio.sleep(15)  # need to change to the spare function
    await geodetic_to_cartesian_ned(drone)
    return



async def absolute_yaw(drone):
    async for attitude_info in drone.telemetry.attitude_euler():
        absolute_yaw = attitude_info.yaw_deg
        return absolute_yaw






async def x_axes(x_dist, drone):
    # get local position
    x_local, y_local, z_local = await geodetic_to_cartesian_ned(drone)
    lat_dist, long_dist, alt_dist = await cartesian_to_geodetic(x_dist, y_local, z_local, drone)
    yaw = await absolute_yaw(drone)
    await drone.action.goto_location(lat_dist, long_dist, alt_dist, yaw)
    print(await geodetic_to_cartesian_ned(drone))
    return



async def y_axes(drone):

    return





async def main():
    global latitude_i, longitude_i, altitude_i
    x_initial = y_initial = z_initial = latitude_i = longitude_i = altitude_i = 0


    drone = System()
    await drone.connect(system_address="udp://:14540")
    #await drone.connect(system_address="serial:///dev/ttyTHS1")
    await setup_drone(drone)


    #get first coordinate with geo
    latitude_i,longitude_i,altitude_i=await get_geo_pos(drone)
    print(f"At GPS position: Latitude={latitude_i}, Longitude={longitude_i}, Altitude={altitude_i} meters")
    x_initial,y_initial,z_initial=await  geodetic_to_cartesian_ned(drone)


        # at this section need add
        # 1) validation that the drone is at offbord mode

    target_altitude = int(input("Enter the target altitude in meters: "))
    await takeoff_presedoure(drone,target_altitude)

    #at this point the go to loop is start

    #await x_axes(15,drone)




    await drone.action.land()




if __name__ == "__main__":
    asyncio.run(main())

