import json
from ISMS.models import Sensor
def prettify_data(data):
    prettified_data = {"temperature": [], "humidity": [], "pressure": [], "lpg": [], "methane": [], "hydrogen": [], "smoke": [], "ppm": [], "date_time":[]}
    for sens in data:
        for column in prettified_data.keys():
            prettified_data[column].append(getattr(sens, column))
    return json.dumps(prettified_data, default=str)