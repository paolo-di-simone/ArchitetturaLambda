#!/usr/bin/env python3
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, substring_index, count
from pyspark.sql.window import Window
from pyspark.sql.functions import desc, row_number
import argparse

#spark = SparkSession.builder.appName("job1").getOrCreate()


parser =argparse.ArgumentParser()
parser.add_argument("--input_path", type = str, help="Input file path")
parser.add_argument("--output_path", type = str, help="Output folder path")
args = parser.parse_args()
input_filepath, output_filepath = args.input_path, args.output_path

my_path = input_filepath



spark = SparkSession.builder.appName("MongoDBWriteExample").config("spark.mongodb.output.uri", "mongodb://127.0.0.1:27017/Packets").getOrCreate()

df = spark.read.csv(input_filepath, header  = True).cache()

#-----------------------------------------numero pacchetti per giorno------------------------------------------------#

number_packet = df.select("date").groupBy("date").count()

#----------------------------------------------------numero pacchetti per ogni ora -------------------------------------#

number_packet_hour_tmp = df.withColumn("ora", substring_index(col("time"), ":", 1))

number_packet_hour = number_packet_hour_tmp.select("ora").groupBy("ora").count()

#----------------------------------------------------numero pacchetti per data e mac destinazione----------------------#

mac_dst = df.select("date", "mac_dst").groupBy("date","mac_dst").count()

#----------------------------------------------------numero pacchetti per data e mac sorgente------------------------------#

mac_src = df.select("date", "mac_src").groupBy("date","mac_src").count()

#----------------------------------------------------numero pacchetti per data e tipo Ethernet------------------------------#

tipo = df.select("date", "type").groupBy("date","type").count()

#----------------------------------------------------numero pacchetti per data e protocollo--------------------------------#

filtered_df = df.filter(col("proto").isNotNull())

proto = filtered_df.select("date", "proto").groupBy("date","proto").count()

#----------------------------------------------------numero pacchetti per data e ip_sorgente--------------------------------#

filtered_df = df.filter(col("ip_src").isNotNull())

ip_src = filtered_df.select("date", "ip_src").groupBy("date","ip_src").count()

#----------------------------------------------------numero pacchetti per data e ip_destinazione--------------------------------#

filtered_df = df.filter(col("ip_dst").isNotNull())

ip_dst = filtered_df.select("date", "ip_dst").groupBy("date","ip_dst").count()

#------------------------------------------------------Sport---------------------------------------------#

filtered_df = df.filter(col("sport").isNotNull())

sport = filtered_df.select("date", "sport").groupBy("date","sport").count()

window_spec = Window.partitionBy("date").orderBy(desc("count"))

ranked_df = sport.withColumn("row_num", row_number().over(window_spec))

result_sport = ranked_df.filter(ranked_df.row_num <= 5)

final_result_sport = result_sport.select("date", "sport", "count")


#------------------------------------------------------Dport---------------------------------------------------#

filtered_df = df.filter(col("dport").isNotNull())

dport = filtered_df.select("date", "dport").groupBy("date","dport").count()

window_spec = Window.partitionBy("date").orderBy(desc("count"))

ranked_df = dport.withColumn("row_num", row_number().over(window_spec))

result_dport = ranked_df.filter(ranked_df.row_num <= 5)

final_result_dport = result_dport.select("date", "dport", "count")

#-----------------------------------------------------------Flag Tcp -----------------------------------------------#

filtered_df = df.filter(col("flag_tcp").isNotNull())

flag_tcp = filtered_df.select("date", "flag_tcp").groupBy("date","flag_tcp").count()



# number_packet.show()
# #average_day.show()
# number_packet_hour.show()
# mac_dst.show()
# mac_src.show()
# tipo.show()
# proto.show()
# ip_src.show()
# ip_dst.show()
# result_sport.show()
# result_dport.show()
# flag_tcp.show()

number_packet.write.format("mongodb").mode("append").option("database",
"Packets").option("collection", "NumeroPacchetti").save()

number_packet_hour.write.format("mongodb").mode("append").option("database",
 "Packets").option("collection", "NumeroPacchettiOra").save()

mac_dst.write.format("mongodb").mode("append").option("database",
"Packets").option("collection", "MacDst").save()

mac_src.write.format("mongodb").mode("append").option("database",
"Packets").option("collection", "MacSrc").save()

tipo.write.format("mongodb").mode("append").option("database",
"Packets").option("collection", "Tipo").save()

proto.write.format("mongodb").mode("append").option("database",
"Packets").option("collection", "Protocollo").save()

ip_src.write.format("mongodb").mode("append").option("database",
"Packets").option("collection", "IpSrc").save()

ip_dst.write.format("mongodb").mode("append").option("database",
"Packets").option("collection", "IpDst").save()

final_result_sport.write.format("mongodb").mode("append").option("database",
"Packets").option("collection", "Sport").save()

final_result_dport.write.format("mongodb").mode("append").option("database",
"Packets").option("collection", "Dport").save()

flag_tcp.write.format("mongodb").mode("append").option("database",
"Packets").option("collection", "FlagTcp").save()
