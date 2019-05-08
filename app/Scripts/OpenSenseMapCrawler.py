import json
import os.path
import time
from datetime import datetime
from typing import Dict

import requests
from Resources.generalKitResource import

def create_box_cache(open_sense_path) -> Dict:
    r = requests.get(open_sense_path).json()
    with open(open_sense_path, 'w') as outfile:
        json.dump(r, outfile, ensure_ascii=False)
    return r


def get_sensor_values(boxes):
    base_box_url = "https://api.opensensemap.org/boxes"
    for box_ids in boxes:
        box = requests.get(f"{base_box_url}/{box_ids['_id']}").json()
        sensors = box.get("sensors", None)
        # TODO CREATE OR GET BOX
        if sensors:
            for sensor in sensors:
                # TODO CREATE OR GET SENSOR
                last_measurement = sensor.get('lastMeasurement', None)
                if last_measurement:
                    m_string = f"https://api.opensensemap.org/boxes/{sensor['boxes_id']}/data/{sensor['_id']}?to-date={last_measurement['createdAt']}"
                    measurements = requests.get(m_string)
                    print(measurements.json())


def crawl_results():
    open_sense_path : str = 'openSenseCache.json'
    if os.path.exists(open_sense_path):
        if (datetime.now() - datetime.strptime(time.ctime(os.path.getmtime(open_sense_path)),
                                               "%a %b %d %H:%M:%S %Y")).days > 4:
            get_sensor_values(create_box_cache(open_sense_path))
        with open(open_sense_path) as infile:
            get_sensor_values(json.load(infile))
    else:
        get_sensor_values(create_box_cache())


if __name__ == '__main__':
    crawl_results()
