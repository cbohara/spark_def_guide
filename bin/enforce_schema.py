from pyspark.sql.types import StructField, StructType, StringType, LongType
from pyspark.sql import SparkSession

if __name__ == "__main__":
	spark = SparkSession.builder.master("local").appName("Enforce Schema").getOrCreate()
	myManualSchema = StructType([
		StructField("DEST_COUNTRY_NAME", StringType(), True),
		StructField("ORIGIN_COUNTRY_NAME", StringType(), True),
		StructField("count", LongType(), False)
	])

	df = spark.read.format("json").schema(myManualSchema) \
		.load("/Users/charlieohara/cbohara/spark_def_guide/data/flight-data/json/2015-summary.json")
	df.printSchema()
