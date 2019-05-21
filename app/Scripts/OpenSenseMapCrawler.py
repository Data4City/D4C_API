import argparse
import json
import os.path
import time
from datetime import datetime
from typing import Dict, Generator, List, Tuple

import requests

api_path = "http://localhost:8080"
args = None


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


def get_location(box_json) -> Tuple[float, float]:
    try:
        return box_json["loc"][0]["geometry"]["coordinates"]
    except Exception:
        return None, None


def crawl_and_save_to_api(box_cache: List):
    sensors_list = []
    for box_json in get_osm_box_info(box_cache):
        try:
            sensors = box_json.get("sensors", [])
            osm_serial = "osm_" + box_json["_id"]
            check = long, lat = get_location(box_json)
            body = {"serial": osm_serial, "lat": lat, "long": long} if check else {"serial": osm_serial}
            d_kit = requests.post(api_path + "/v1/kit", json=body).json()
            kit_id = d_kit["id"]
            sensors_list.append((kit_id, sensors))
        except Exception:
            continue

    if bool(args.sensors):
        for kit, sensors_in_kit in sensors_list:
            try:
                post_sensors(kit, sensors_in_kit)
            except Exception:
                continue


def post_values(kit_id, measurement_id, values):
    for value in values:
        try:

            if measurement_id and kit_id:
                requests.post(api_path + "/v1/kit/{kit_id}/measurement/{measurement_id}".format(
                    kit_id=kit_id, measurement_id=measurement_id),
                              json={
                                  "data": value['value'],
                                  "timestamp": value['createdAt']}
                              )
        except Exception:
            continue


def post_sensors(kit_id, sensors):
    for sensor in sensors:
        try:
            if all(k in sensor for k in ("lastMeasurement", "_id", "boxes_id", "sensorType", "title")):

                sense_req = requests.post(api_path + "/v1/kit/{kit_id}/sensor".format(kit_id=kit_id),
                                          json={
                                              "name": sensor["title"],
                                              "model": sensor["sensorType"]
                                          })
                if sense_req.status_code == 201:
                    d_sensor = sense_req.json()
                    measure_req = requests.post(
                        api_path + "/v1/kit/{kit_id}/sensor/{sensor_id}/measurement".format(sensor_id=d_sensor["id"],
                                                                                            kit_id=kit_id),
                        json={
                            "name": sensor["title"],
                            "symbol": sensor["unit"]}
                    )

                    if measure_req.status_code == 201:
                        d_measurement = measure_req.json()
                        last_measurement = sensor.get('lastMeasurement', {})
                        if 'createdAt' in last_measurement:
                            if bool(args.values):
                                post_values(kit_id, d_measurement["id"], get_sensor_values(sensor, last_measurement))
        except Exception:
            continue


def crawl_results():
    open_sense_path = 'openSenseCache.json'
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
    parser = argparse.ArgumentParser(description="Which options should be saved")
    parser.add_argument("--sensors", metavar='-s', help="Save sensors?", default=True)
    parser.add_argument("--values", metavar='-v', help="Save values?", default=True)
    args = parser.parse_args()
    crawl_results()
