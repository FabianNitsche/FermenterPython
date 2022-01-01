from influxdb import InfluxDBClient
from datetime import datetime

class Storage(object):
    def __init__(self):
        self._client = InfluxDBClient("localhost", 8086, "pi", "raspberry", "home")

    def write_data(self, data, setTemperature, heaterOn):
        time = self._get_time_string()
        json = [
            {
                "measurement" : "temperature",
                "time" : time,
                "fields" : {
                    "value" : round(data.temperature, 1)
                }
            },
            {
                "measurement" : "pressure",
                "time" : time,
                "fields" : {
                    "value" : round(data.pressure)
                }
            },
            {
                "measurement" : "humidity",
                "time" : time,
                "fields" : {
                    "value" : round(data.humidity, 1)
                }
            },
            {
                "measurement" : "set_temperature",
                "time" : time,
                "fields" : {
                    "value" : round(setTemperature, 1)
                }
            },
            {
                "measurement" : "heater",
                "time" : time,
                "fields" : {
                    "value" : 60.0 if heaterOn else 6.0
                }
            }

        ]
        self._write_to_db(json)

    def _write_to_db(self, json):
        self._client.write_points(json)

    def _get_time_string(self):
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")