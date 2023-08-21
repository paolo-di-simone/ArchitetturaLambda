import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

influxdb_parameters = {
	"TOKEN": "kEqIpjRQ6jy_RdFghsuJK268Su0nByfAP8ciupp8Q5B4nCCVg_4GVCWOplm4MrmF2kpQ5zOBWkQQHlXoqwkZeg==",
	"ORG": "paolo",
	"URL": "http://localhost:8086",
	"BUCKET": "bucket"
}

client = influxdb_client.InfluxDBClient(url=influxdb_parameters["URL"], token=influxdb_parameters["TOKEN"], org=influxdb_parameters["ORG"])

query_api = client.query_api()

query = """
	from(bucket: "bucket")
	  |> range(start: 2023-07-01T00:00:00Z, stop: 2023-08-31T23:59:59Z)
	  |> filter(fn: (r) => r._measurement == "packet")
"""

tables = query_api.query(query, org=influxdb_parameters["ORG"])

for table in tables:
	for record in table.records:
		print(record)
		
client.close()
