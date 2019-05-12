import json
import os.path
import time
from datetime import datetime
from typing import Dict, Generator, List

import requests


def create_box_cache(open_sense_path: str, ) -> List:
    r = requests.get("https://api.opensensemap.org/boxes").json()
    with open(open_sense_path, 'w') as outfile:
        json.dump(r, outfile, ensure_ascii=False)
    return r


def get_osm_box_info(box_cache: List) -> Generator[Dict[str, str], None, None]:
    for box_ids in box_cache:
        box = requests.get("{base_box_url}/{box_id}".format(
            base_box_url="https://api.opensensemap.org/boxes",
            box_id=box_ids['_id']
        )).json()
        yield box


def get_sensor_values(sensor: Dict[str, str], last_measurement) -> Generator[Dict[str, str], None, None]:
    m_string = "https://api.opensensemap.org/boxes/{box_id}/data/{sensor_id}?to-date={created_at}".format(
        box_id=sensor['boxes_id'],
        sensor_id=sensor['_id'],
        created_at=last_measurement['createdAt']
    )

    for measurement in requests.get(m_string).json():
        yield measurement


def crawl_and_save_to_api(box_cache: List):
    api_path = "http://localhost:8080"
    for box_json in get_osm_box_info(box_cache):
        print(box_json)
        sensors = box_json.get("sensors", [])
        osm_serial = "osm_" + box_json["_id"]
        d_kit = requests.post(api_path + "/v1/kit", json={"serial": osm_serial}).json()
        kit_id = d_kit["id"]
        if sensors:
            for sensor in sensors:
                if all(k in sensor for k in ("lastMeasurement", "_id", "boxes_id", "sensorType", "title")):

                    sense_req = requests.post(api_path + "/v1/{}/sensor".format(kit_id),
                                              json={
                                                  "name": sensor["title"],
                                                  "model": sensor["sensorType"]
                                              })
                    if sense_req.status_code == 201:
                        d_sensor = sense_req.json()
                        measure_req = requests.post(api_path + "/v1/measurement/{}".format(d_sensor["id"]),
                                                    json={
                                                        "name": sensor["title"],
                                                        "symbol": sensor["unit"]}
                                                    )

                        if measure_req.status_code == 201:
                            d_measurement = measure_req.json()
                            last_measurement = sensor.get('lastMeasurement', {})
                            if 'createdAt' in last_measurement:
                                for value in get_sensor_values(sensor, last_measurement):
                                    requests.post(api_path + "/v1/{}/{}/value".format(kit_id, d_measurement["id"]),
                                                  json={
                                                      "data": value['value'],
                                                      "timestamp": value['createdAt']}
                                                  )


def crawl_results():
    open_sense_path: str = 'openSenseCache.json'
    if os.path.exists(open_sense_path):
        box_cache = {}
        if (datetime.now() - datetime.strptime(time.ctime(os.path.getmtime(open_sense_path)),
                                               "%a %b %d %H:%M:%S %Y")).days > 4:
            box_cache = create_box_cache(open_sense_path)
        else:
            with open(open_sense_path) as infile:
                box_cache = json.load(infile)

        crawl_and_save_to_api(box_cache)
    else:
        crawl_and_save_to_api(create_box_cache(open_sense_path))


if __name__ == '__main__':
    crawl_results()
