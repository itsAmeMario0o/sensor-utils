from tetpyclient import RestClient
from pprint import pprint
from tempfile import NamedTemporaryFile
import csv
import argparse
import urllib3
import shutil

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#API_ENDPOINT="https://<UI_VIP_OR_DNS_FOR_TETRATION_DASHBOARD>"
API_ENDPOINT="https://pliny.cisco.com"

restclient = RestClient(API_ENDPOINT,
                credentials_file='api_credentials.json',
                verify=False)

current_sensors = {}

def populate_sensors():
    resp = restclient.get('/sensors')
    pprint(resp)
    if resp.status_code == 200:
        for i in resp.json().get("results", []):
            current_sensors[i.get("uuid")] = i

def get_sensor(uuid):
    pprint(uuid)
    if len(current_sensors) == 0:
        pprint("Populating sensors...")
        populate_sensors()
    
    c = current_sensors.get(uuid, {})
    if c.get("deleted_at", None) is not None:
        return None
    else:
        return c

def update_csv(path, uuid):
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open(path, 'rb') as csvfile:
        fields_reader = csv.reader(csvfile)
        
        fields = []
        fields = fields_reader.next()
        if "deleted" not in fields:
            fields.append("deleted")

        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        writer.writeheader()
        for row in reader:
            if row.get("uuid") == uuid:
                row['deleted'] = True

            writer.writerow(row)
    shutil.move(tempfile.name, path)

def delete_sensor(uuid):
    resp = restclient.delete('/sensors/' + uuid)

    return resp

def csv_reader(path, action, dry):
    with open(path, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pprint(row.get("host_name") + " uuid: " + row.get("uuid"))
            if action == "delete":
                pprint("checking sensor...")
                s = get_sensor(row.get("uuid"))
                if s is None or s.get("host_name") != row.get("host_name"):
                    if dry:
                        pprint("dry run...")
                    pprint("sensor not matching.")
                else:
                    pprint("deleting sensor...")
                    if not dry:
                        resp = delete_sensor(row.get("uuid"))
                        if resp.status_code > 199 and resp.status_code < 300:
                            pprint("updating csv...")
                            update_csv(path, row.get("uuid"))
                        pprint(resp)
                    else:
                        pprint("dry run...")
                        pprint("updating csv...")
                        update_csv(path, row.get("uuid"))
            elif action == "get":
                get_sensor(row.get("uuid"))
            

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sensors", help="path to csv file")
    parser.add_argument("--dry", action='store_true', help="simulate, do not execute")
    args = parser.parse_args()

    csv_reader(args.sensors, "delete", args.dry)

if __name__ == "__main__":
    main()