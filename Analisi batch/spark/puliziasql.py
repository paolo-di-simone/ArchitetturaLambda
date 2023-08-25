from pyspark.sql import SparkSession
from pyspark.sql.functions import col, substring_index, count
from pyspark.sql.functions import col, when
import argparse



parser =argparse.ArgumentParser()
parser.add_argument("--input_path", type = str, help="Input file path")
parser.add_argument("--output_path", type = str, help="Output folder path")
args = parser.parse_args()
input_filepath, output_filepath = args.input_path, args.output_path

my_path = input_filepath

spark = SparkSession.builder.appName("CSVProcessing").getOrCreate()

df = spark.read.csv(input_filepath, header  = True).cache()
columns_to_drop = ["Ip_version", "ihl", "tos", "len", "id", "flags", "frag", "ttl", "checksum", "sequence","ack","dataofs","window"] 
df = df.drop(*columns_to_drop)

df = df.filter(df["type"] != 34525)


type_expr = (
    when(col("type") == "2048", "IPv4")
    .when(col("type") == "2054", "ARP")
    .otherwise(col("type"))
)

proto_expr = (
     when(col("proto") == 17, "UDP")
    .when(col("proto") == 1, "ICMP")
    .when(col("proto") == 6, "TCP")
    .otherwise(col("proto"))
)



df_with_conversions = df.withColumn("type", type_expr).withColumn("proto", proto_expr)



#df_with_conversions.show()

output_csv_path = "/home/filippo/big_data/kathara-lab_load-balancer-ws-rnd/kathara-lab_loadbalancer-ws-rnd_prova_più_client_meno_server/shared/output/output_finale"

df_with_conversions.write.option("header", "true").csv(output_csv_path, mode="overwrite")
