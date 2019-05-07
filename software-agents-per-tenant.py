from collections import defaultdict
from datetime import datetime
from tetpyclient import RestClient

rc = RestClient("xx", api_key="xx", api_secret="xx", verify=False)

resp = rc.get("/sensors")

sensors = resp.json()["results"]
tenants = defaultdict(set)

for sensor in sensors:
    active = datetime.fromtimestamp(sensor["last_config_fetch_at"])
    host_name = "{:25} \t\t{}".format(sensor["host_name"], active.strftime("%m/%d/%Y"))
    for intf in sensor["interfaces"]:
        tenant = intf["vrf"]
        tenants[tenant].add(host_name)

for tenant, hosts in tenants.items():
    if tenant != "Tetration":
        print "{} (count = {}):".format(tenant, len(hosts))
        for host in hosts:
                print "\t{}".format(host)