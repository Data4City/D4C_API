import argparse
import json
import os.path
import time
from datetime import datetime
from typing import Dict, Generator, List, Tuple
from requests_futures.sessions import FuturesSession

import requests
import re
from datetime import datetime
api_path = "http://localhost:8080"
args = None
session = FuturesSession(max_workers=20)


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
        print("Error at get locatio")
        return None


def crawl_and_save_to_api(box_cache: List):
    future_sensor_list = []
    for box_json in get_osm_box_info(box_cache):
        try:
            sensors = box_json.get("sensors", [])
            osm_serial = "osm_" + box_json["_id"]
            check = get_location(box_json)
            if check and len(check) == 2:
                lat, long = check
                body = {"serial": osm_serial, "lat": lat, "long": long}
            else:
                body = {"serial": osm_serial}
            future_sensor_list.append((session.post(api_path + "/v1/kit", json=body), sensors))
        except Exception as e:
            print(e)
            continue

    if bool(args.sensors):
        for kit_future, sensor_list in future_sensor_list:
            kit_id = kit_future.result().json()["id"]
            for sensors_in_kit in sensor_list:
                try:
                    post_sensors(kit_id, sensors_in_kit)
                except Exception:
                    print("Sensor error")
                    continue


def post_values(kit_id, measurement_id, values):
    for value in values:
        try:
            if measurement_id and kit_id:
                timestamp = re.sub('[ZT]', ' ', value['createdAt'])

                session.post(api_path + "/v1/kit/{kit_id}/measurement/{measurement_id}".format(
                    kit_id=kit_id, measurement_id=measurement_id),
                             json={
                                 "data": value['value'],
                                 "timestamp": timestamp}
                             )

        except Exception as e:
            print(e)
            continue


def post_sensors(kit_id, sensor):
    future_sensor_list = []
    try:
        if all(k in sensor for k in ("lastMeasurement", "_id", "boxes_id", "sensorType", "title")):
            future_sensor_list.append(session.post(api_path + "/v1/kit/{kit_id}/sensor".format(kit_id=kit_id),
                                                   json={
                                                       "name": sensor["title"],
                                                       "model": sensor["sensorType"]
                                                   }))

    except Exception as e:
        print(e)

    future_measurements_list = []
    for sensor_result in future_sensor_list:
        sense_req = sensor_result.result()
        if sense_req.status_code == 201:
            d_sensor = sense_req.json()
            future_measurements_list.append(session.post(
                api_path + "/v1/sensor/{sensor_id}/measurement".format(sensor_id=d_sensor["id"]),
                json={
                    "kit_id": kit_id,
                    "name": sensor["title"],
                    "symbol": sensor["unit"]}
            ))

    for future_measurement in future_measurements_list:
        measure_req = future_measurement.result()
        if measure_req.status_code == 201:
            d_measurement = measure_req.json()
            last_measurement = sensor.get('lastMeasurement', {})
            if 'createdAt' in last_measurement:
                if bool(args.values):
                    post_values(kit_id, d_measurement["id"], get_sensor_values(sensor, last_measurement))


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
    start = datetime.now()
    parser = argparse.ArgumentParser(description="Which options should be saved")
    parser.add_argument("--sensors", metavar='-s', help="Save sensors?", default=True)
    parser.add_argument("--values", metavar='-v', help="Save values?", default=True)
    args = parser.parse_args()
    crawl_results()
    end = datetime.now()
    print("Crawled the api in {}".format(str((end-start).min)))
