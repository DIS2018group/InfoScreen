import requests
import json
import datetime


STOPS = (
    ("kumpula", "Kumpulan kampus", "Stops located on Kustaa Vaasan tie"),
    ("virtanen", "A.I. Virtasen aukio",
     "Stops located on Väinö Auerin katu"),
)
API_URL = "https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql"
USER_AGENT = (
    "InfoScreen: Designing Interactive Systems course project - "
    "github.com/DIS2018group/InfoScreen"
)


def _build_query(stops):
    query = "{\n"

    for alias, address, desc in stops:
        query += """
            {alias}: stops(name: "{address}") {{
                code
                stoptimesWithoutPatterns {{
                    scheduledArrival
                    realtimeArrival
                    arrivalDelay
                    scheduledDeparture
                    realtime
                    headsign
                    trip {{
                        route {{
                            shortName
                        }}
                    }}
                }}
            }}\n
        """.format(alias=alias, address=address)

    query += "}"

    return query


def _parse_graphql_response(response, stops):
    def seconds_to_datetime(seconds):
        """
        Convert seconds since start of day to a datetime
        """
        dt = datetime.datetime.now()

        hour, minute, second = (
            int(seconds / (60 * 60)),
            int(seconds / 60) % 60,
            int(seconds) % 60
        )
        dt = datetime.datetime(
            year=dt.year, month=dt.month, day=dt.day,
            hour=hour, minute=minute, second=second)

        return dt

    result = {
        "stops": {
            alias: {
                "address": address, "description": desc, "stoptimes": []
            } for alias, address, desc in stops
        }
    }

    for alias, _, _ in stops:
        for stop in response["data"][alias]:
            for stoptime in stop["stoptimesWithoutPatterns"]:
                if stoptime["realtime"]:
                    # Prefer realtime prediction whenever possible
                    arrival_seconds = stoptime["realtimeArrival"]
                else:
                    arrival_seconds = stoptime["scheduledArrival"]

                arrival_datetime = seconds_to_datetime(arrival_seconds)

                trip_result = {
                    "arrival": arrival_datetime,
                    "headsign": stoptime["headsign"],
                    "route": stoptime["trip"]["route"]["shortName"],
                }
                result["stops"][alias]["stoptimes"].append(trip_result)

    return result


def get_timetable():
    query = {"query": _build_query(STOPS)}
    response = requests.post(
        API_URL,
        headers={"user-agent": USER_AGENT},
        json=query)
    response.raise_for_status()

    timetable = _parse_graphql_response(response.json(), STOPS)

    return timetable
