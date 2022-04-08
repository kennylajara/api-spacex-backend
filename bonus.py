from datetime import datetime

import psycopg2
from haversine import haversine, Unit


def find_closest_to_point(list_of_satellites, point):
    """
    Finds the satellite with the closest distance to the given point.
    :param list_of_satellites: list of tuples containing the satellite's id and coordinates
    :point: tuple containing the longitude and latitude of the point
    :return: tuple containing the satellite's id and the distance to the point
    """
    min_distance = None
    closest_satellite = None
    for satellite in list_of_satellites:
        distance = haversine(point, satellite[1], Unit.KILOMETERS)
        if min_distance is None or distance < min_distance:
            min_distance = distance
            closest_satellite = satellite[0]
    return closest_satellite, min_distance


def select_satellites(conn, time):
    """
    Selects all the satellites from the database.
    :param conn: connection to the database
    :return: list of tuples containing the satellite's id and coordinates
    """
    # Query the database
    sql = f"""
        SELECT id, (ARRAY_AGG (
                latitude || ',' || longitude
                ORDER BY creation_date DESC
            ))[1] AS coordinates
        FROM starlink_historical_data
        WHERE creation_date<='{time}'
        GROUP BY id;
    """
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    # Convert the rows to a list of tuples containing
    # the satellite's id and its coordinates
    satellites = []
    for row in rows:
        if row[1] is not None:
            lat, lon = row[1].split(",")
            lat, lon = float(lat), float(lon)
            satellites.append((row[0], (lat, lon)))

    return satellites


if __name__ == "__main__":

    # Connect to the database
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            database="postgres",
            password="postgres",
        )
    except psycopg2.Error as e:
        print("Unable to connect to database")
        print(e)

    # Ask for the time
    while(True):
        time = input("Enter a time (YYYY-MM-DD HH:MM:SS): ").strip().replace(" ", "T")
        # Validate the time format
        try:
            datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
            break
        except ValueError:
            print("Invalid time format")

    # Ask for the point
    while(True):
        point = input("Enter a point (lat,lon): ").strip('()').replace(" ", "")
        coords = point.split(",")
        # Validate the point format
        try:
            if len(coords) != 2:
                raise ValueError

            lat, lon = float(coords[0]), float(coords[1])
            if lon < -180 or lon > 180 or lat < -90 or lat > 90:
                raise ValueError
            else:
                break
        except ValueError:
            print("Invalid point format")


    satellites = select_satellites(conn, time)
    closest = find_closest_to_point(satellites, (lat, lon))
    print(f"The closest satellite is {closest[0]} at {closest[1]:.2f} km")
