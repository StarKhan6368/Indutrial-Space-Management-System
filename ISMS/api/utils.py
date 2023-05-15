import json, os

def prettify_data(sensor_data: list) -> str:
    prettified_data = {"temperature": [], "humidity": [], "pressure": [], "lpg": [], "methane": [], 
                       "hydrogen": [], "smoke": [], "ppm": [], "date_time": [] }
    for sensor in sensor_data:
        for column in prettified_data:
            prettified_data[column].append(getattr(sensor, column))
    return json.dumps(prettified_data, default=str)


def is_host_responsive(host: str) -> bool:
    response = os.system(f"ping -c 1 {host} > /dev/null 2>&1")
    return response == 0