from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col, format_number
import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql.functions import split, concat, col, from_unixtime, unix_timestamp, window
from pyspark.sql.functions import to_timestamp, window, lit, expr, to_json, struct
from pyspark.sql.functions import collect_list, create_map, sum

import logging


################################################ DEFINIZIONE PARAMETRI ################################################


kafka_parameters = {
	"APP_NAME": "Packet streaming",
	"BOOTSTRAP_SERVER": "localhost:9092",
	"TOPIC_INPUT": "my-topic",
	"TOPIC_OUTPUT": "output-topic",
	"CHECKPOINT_LOCATION": "file:///home/paolods/Desktop/Progetto/checkpoint",
	"WINDOW_DURATION": "1 seconds",
	"WINDOW_SLIDE": "50 milliseconds"
}

influxdb_parameters = {
	"TOKEN": "kEqIpjRQ6jy_RdFghsuJK268Su0nByfAP8ciupp8Q5B4nCCVg_4GVCWOplm4MrmF2kpQ5zOBWkQQHlXoqwkZeg==",
	"ORG": "paolo",
	"URL": "http://localhost:8086",
	"BUCKET": "bucket"
}

columns = [
    "date", "time", "mac_dst", "mac_src", "type", "ip_version", "ihl", "tos",
    "len", "id", "flags", "frag", "ttl", "proto", "checksum", "ip_src", "ip_dst",
    "sport", "dport", "sequence", "ack", "flag_tcp", "dataofs", "window", "payload"
]


################################################ LETTURA DA TOPIC KAFKA ################################################


# Inizializzazione sessione spark
spark = SparkSession.builder.appName(kafka_parameters["APP_NAME"]).getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Lettura da topic kafka
lines_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_parameters["BOOTSTRAP_SERVER"]) \
    .option("subscribe", kafka_parameters["TOPIC_INPUT"]) \
    .load()

lines_df = lines_df.selectExpr("CAST(value AS STRING) as data")
split_cols = split(lines_df["data"], ",")
parsed_df = lines_df.select(split_cols.alias("csv_data"))

for idx, col_name in enumerate(columns):
    parsed_df = parsed_df.withColumn(col_name, parsed_df["csv_data"][idx])

parsed_df = parsed_df.drop("csv_data")

parsed_df = parsed_df.withColumn("timestamp", to_timestamp(concat(col("date"), lit(","), col("time")), "yyyy-MM-dd,HH:mm:ss.SSSSSS"))


################################################ ELABORAZIONE CON SPARK STREAMING ################################################


windowed_df = parsed_df \
	.withWatermark("timestamp", kafka_parameters["WINDOW_DURATION"]) \
	.groupBy(window("timestamp", kafka_parameters["WINDOW_DURATION"]), "ip_src") \
	.count()

windowed_df = windowed_df.withColumnRenamed("count", "n_packets_by_ip_src")


################################################ SCRITTURA DATI SU INFLUXDB ################################################


# Crea la connessione a InfluxDB
client = InfluxDBClient(url=influxdb_parameters["URL"], token=influxdb_parameters["TOKEN"], org=influxdb_parameters["ORG"])


# Funzione scrittura dati su InfluxDB
def write_to_influxdb(row):

	write_api = client.write_api(write_options=SYNCHRONOUS)

	try:

		try:
		    timestamp = datetime.strptime(str(row.window.end), "%Y-%m-%d %H:%M:%S.%f")
		except ValueError:
		    timestamp = datetime.strptime(str(row.window.end), "%Y-%m-%d %H:%M:%S")

		timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")
		point = Point("packet")
		point.time(timestamp, WritePrecision.NS)
		point.tag("ip_src", row.ip_src)
		point.field("n_packets_by_ip_src", row.n_packets_by_ip_src)

		write_api.write(bucket=influxdb_parameters["BUCKET"], org=influxdb_parameters["ORG"], record=point)

		print("Oggetto point")
		print("Timestamp:", timestamp)
		print("IP:", row.ip_src)
		print("N packets:", row.n_packets_by_ip_src)
		print()

	except Exception as e:
		print("Errore nell'inserimento dei dati su InfluxDB:", e)


# Scrivi i messaggi in InfluxDB
windowed_df \
	.writeStream \
    .outputMode("complete") \
    .foreach(write_to_influxdb) \
    .start() \
    .awaitTermination()
