from pprint import pprint
import json
import time
import datetime
import csv
import argparse

# CURRENT_TIME in UNIX TS
CURRENT_TIME = int(time.time())

def create_csv(path, data):
    with open(path, 'wb') as csvfile:
        fieldnames = ['host_name', 'current_sw_version', 'uuid', 'last_config_fetch_at', 'last_registration_req_at']
        csvwriter = csv.DictWriter(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL,
                                fieldnames=fieldnames)

        csvwriter.writeheader()

        for d in data:
            csvwriter.writerow({
                'host_name': d.get("host_name"),
                'current_sw_version': d.get("current_sw_version"),
                'uuid': d.get("uuid"), 
                'last_config_fetch_at': datetime.datetime.fromtimestamp(
                        d.get("last_config_fetch_at")
                        ).strftime('%Y-%m-%d %H:%M:%S'), 
                'last_registration_req_at':datetime.datetime.fromtimestamp(
                        d.get("last_registration_req_at")
                        ).strftime('%Y-%m-%d %H:%M:%S')
            })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sensors", help="path to sensors.json")
    #parser.add_argument("csv", help="path to output.csv")
    parser.add_argument("--last_config_fetch", help="Last Config Fetch in days")
    parser.add_argument("--last_registration_req", help="Last Registration Request in days")
    args = parser.parse_args()

    if args.last_config_fetch is not None:
        field = "last_config_fetch_at"
        max_age = int(args.last_config_fetch) * 86400
    if args.last_registration_req is not None:
        field = "last_registration_req_at"
        max_age = int(args.last_registration_req) * 86400

    output = []
    with open(args.sensors) as f:
        data = json.load(f)
    
    i = 0
    j = 0
    for s in data:
        if s.get("deleted_at", None) is None:
            if int(s.get(field, 0)) < CURRENT_TIME - max_age:
                pprint(s.get("host_name") + " " + s.get("uuid"))
                pprint(s.get("host_name"))
                pprint("last_config_fetch_at " + datetime.datetime.fromtimestamp(
                    s.get("last_config_fetch_at")
                    ).strftime('%Y-%m-%d %H:%M:%S'))
                pprint("last_registration_req_at " + datetime.datetime.fromtimestamp(
                    s.get("last_registration_req_at")
                    ).strftime('%Y-%m-%d %H:%M:%S'))
                pprint("config_updated_at " + datetime.datetime.fromtimestamp(
                    s.get("config_updated_at")
                    ).strftime('%Y-%m-%d %H:%M:%S'))   
                pprint("updated_at " + datetime.datetime.fromtimestamp(
                    s.get("updated_at")
                    ).strftime('%Y-%m-%d %H:%M:%S'))               
                pprint("created_at " + datetime.datetime.fromtimestamp(
                    s.get("created_at")
                    ).strftime('%Y-%m-%d %H:%M:%S'))
                j = j + 1
                output.append(s)
            i = i + 1

    create_csv("output.csv", output)
    pprint(j)
    pprint(len(data))

if __name__ == "__main__":
    main()