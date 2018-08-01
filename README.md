# Tetration Sensor Management Tools

This repo host some simple tool to help with sensor management at scale.

## Files

### delete_from_csv.py

Takes an input file that has at least a `uuid` and an `host_name` column to delete all the sensors. This script needs the `api_credentials.json` with software sensor management permissions from Tetration UI. For now you will need to update the file and replace `API_ENDPOINT` with your Tetration cluster URL (https only).

For any sensors in the CSV file, the script with check if the sensor matches an existing sensor on the cluster, and if the uuid and hostname matches. If it does it will delete. If delete is successful, the csv file will get updated with an extra column `deleted`.

To run in dry run mode (does everything except delete) use `--dry` in command args.

Command syntax:

`python delete_from_csv.py input_file.csv`

`python delete_from_csv.py input_file.csv --dry`

Note: input_file will be modified by the script.

### get_inactive_sensors.py

Takes a `sensors.json` file as input which can be downloaded at: [https://<UI_VIP_OR_DNS_FOR_TETRATION_DASHBOARD>/sensors.json](https://<UI_VIP_OR_DNS_FOR_TETRATION_DASHBOARD>/sensors.json) (careful, make sure you select the right scope and are logged as site admin before going to this URL) and gives two options:

- `--last_config_fetch` gets a list based on last config fetch date. This is expecting an int with the number of days since last config fetch.
- `--last_registration_req` gets a list based on the last sensor registration request. This is expecting an int with the number of days since last sensor registration.

Output file will be called `output.csv` and will be in the same folder.

Command syntax:

`python get_inactive_sensors.py sensors.json --last_config_fetch 60`

`python get_inactive_sensors.py sensors.json --last_registration_req 60`

## License

Please refer to the file *LICENSE.pdf* in same directory of this README file.