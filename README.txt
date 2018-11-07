##############################################################
Notes from Spark, The Definitive Guide
##############################################################

Apache Spark philosophy
	unified
		wide variety of operations
			simple as loading data and querying using SQL
			complicated as using machine learning
		for example
			you can load data in using SQL
			then evaluate a machine learning model over the data
			spark can combine these steps into one scan over the data
	computing engine
		only responsible for performing computations
		not for storage
		works with a variety of data sources
	libraries
		provide a unified API for common data analysis tasks
		2 sets of APIs
			low level "unstructured" APIs
			high level Structured APIs

Basic Architecture
	manage and coordinate execution of tasks on data across a cluster of computers
	we submit Spark apps to cluster managers > grant resources to app to do work
	cluster manager
		controls physical machines
		allocates resources to Spark app
	use spark shell for exploratory work
	use spark-submit to send app code to cluster for stand-alone execution

Spark App
	driver process
		runs main() function
		sits on a node in the cluster
		responsible for
			maintaining info about Spark app
			responding to user/program input
			analyzing distributing and scheduling work across executors
		driver can be "driven" from a number of different languages via Spark's language APIs
		control Spark app through driver process
	executor processes
		executes code assigned to it by the driver
		reporting state of computation back to the driver node
		almost always running Spark scala code

SparkSession
	driver process manifests itself to the user as a SparkSession object
	entrance point to running Spark code
		1-to-1 correspondence b/w SparkSession and Spark app
	interactive Spark session
		./bin/spark-shell
		./bin/pyspark
		implicitly create SparkSession in interactive mode
	submit precompiled application to Spark engine
		spark-submit

DataFrame
	represents a table of data with rows and columns
	distributed collection = exists on multiple machines
	best to use DataFrame over Datasets, SQL Tables, and RDDs
	available in all languages

Partitions
	Spark breaks data up into chunks = partitions
	partition = collection of rows that sit on one physical machine in our cluster
	parallelism of 1
		only 1 partition
			even if you have thousands of executors available
			data is only available in 1 chunk
		only 1 executor
			even if you have multiple partitions
			only 1 computational resource
	with DF
		do not manipulate partitions manually
		specify high level transformations of data > Spark determines how to split data

Transformations
	core data structures are immutable
	specify how you want a DF to change to get the resulting DF
	lazy evaluation
	2 types of transformations
		narrow transformations = narrow dependency
			1 input partition > 1 output partitionn
			pipelining
				specify multiple filters on DF for a transformation
				all filters performed in memory
		wide transformation = wide dependency
			1 input partition > multiple output partitions
			computation requires a shuffle
				exchange partitions across the cluster
				Spark needs to write results to disk 

Lazy Evalution
	Spark will wait until the very last moment to execute the graph of computation instructions
	predicate pushdown
		Spark can optimize the entire data flow from end to end
		for example
			build a large spark job and then
			the last filter only requires to fetch 1 row from source data >
			only access the single record we need

Action
	trigger the computation
	instructs Spark to compute a result from a series of transformations
	3 types
		view data in the console
		collect data to native objects
		write to output data sources

End-to-End Example
	use DataFrame reader assoc with SparkSession to read in data
		schema inference = ask Spark to figure out schema
		header = true specifies first row is a header not data
	each resulting DataFrame has a set of columns with unspecified # of rows
		reading data = transformation = lazy evaluation
		Spark only took a peek at a couple rows to guess schema
	explain()
		usedful for debugging
		top - end result
		bottom - data sources
	shuffle partitions
		by default Spark will output 200 shuffle partitions
		spark.conf.set("spark.sql.shuffle.partitions", "5")
		will be used when performing a wide transformation
	DF methods
		many methods accept a string for the column name
		groupBy > RelationalGroupedDataset
			fancy DataFrame
			specify key we are going to group by
			the perform aggregation on that grouping
			grouping is specified but user needs to specify aggregation before it can be queried further

Structured APIs
	3 core distributed collection APIs
		Datasets
			Used for statically typed code in Java and Scala
			not available for Python and R bc dynamically typed code 
		Dataframes
		SQL tables and views
			no performance difference between writing SQL queries or writing DataFrame code
				allows you to query data using SQL
				SQL query on DataFrame returns another DataFrame
			createOrReplaceTempView
				make DataFrame into a table or view
	Execution
		1. Write DataFrame/SQL code
		2. If valid code, Spark converts to Logic Plan
			Resolved logical plan > optimized logical plan
		3. Spark transforms Logic Plan to Physical Plan checking for optimizations along the way
		4. Spark then executes the Physical Plan (RDD manipulations) on the cluster

DataFrame
	distributed table like collection with well defined rows and columns
		each row must have same number of columns
			to Spark (in Scala) DataFrames are Datasets of Type Row
		column type information must be consistent
	schema
		define column name and type 
			schema-on-read is fine for ad-hoc analysis
			good idea to define schema for prod ETL jobs
		schema =StructType 
			made up of StructFields
				name
				type
				boolean
					nullable specifies whether the column can contain missing or null values
		Column Type can be
			simple type
				integer or string
			complex type
				array or map
			null value
		df.printSchema()
	partitioning
		defines the physical distribution across the cluster
		partitioning scheme defines how it is allocated
		can set based on values in a certain column or non-deterministically
	columns
		select, manipulate, and remove columns from DataFrames
			these operations represent expressions
			expression = set of tranformations on 1+ values in a record in a DF
		logical constructs that represent a value computed on a per record basis by means of an expression
		df.col("column_name")
			specify column
			useful when performing a join
		df.columns returns list of column names 
	rows
		can create rows manually but rows do not have schema
		if you append Row to DataFrame, must match DF schema
		can access specific field using index

RDD
	DF transformations are really RDD transformations
		Spark UI describes execution in terms of RDDs
	SparkContext
		entry point for lower level API functionality
		access SparkContext through SparkSession
			SparkSession = used to perform computation across a Spark cluster
	RDD = immutable partitioned collection of records that can be operated on in parallel
	unlike DF
		these records are just Java/Python objects
		do not contain known schema
	Python can lose substantial when using RDDs
		running UDFs row by row

Developing Python Spark Apps
	Package multiple python files into egg or zip 
		use --py-files arg with spark-submit 
		submit .py, .zip, or .egg files to be distributed with app

Launching apps with spark-submit
	--class 
		main class for Java/Scala apps
	--master
		local
			local[*] = run on all cores of your machine
		yarn
	--deploy-mode
		client (default) launch the driver program via CLI
		cluster = launch job as as step
	--jars
		comma sep list of jars to include on the driver and executor classpaths
	--py-files
		comma sep list of .py, .zip, or .egg files to place on PYTHONPATH for Python apps
	--files
		comma sep list of files to include in working dir of each executor
	--conf
		PROP=VALUE
	--properties
		path to a file from which to load extra properties
		defaults to conf/spark-defaults.conf
	--driver-memory
		default 1024M
		needs to be set via command line in client mode
		can be set in SparkConf in app if cluster mode
	--executor-memory
		default 1G

	YARN specific
	--num-executors
		number of executors to launch
		default = 2
		if dynamic allocation is enabled, the intial number of executors will be at least num specified

	EMR config
		do not use maximizeResourceAllocation=True
		recent EMR versions have dynamicAllocation enabled
			application may give resources back to the cluster if they are no longer used
			request them again later when there is demand
		using Spark on EMR will determine the ideal # of executors for you
		only need to specify executor memory
		maybe driver memory and overhead as well

##############################################################
Cluster overview
https://spark.apache.org/docs/1.2.0/cluster-overview.html
##############################################################

Spark context in driver program connects with cluster manager
	defined in app code
Spark acquires executor resources within nodes
	process = instance of a program running 
	executors = processes that run computations and store data
SparkContext sends tasks for the executor to run


#########################################################
Spark Memory Mangement
https://0x0fff.com/spark-memory-management/
#########################################################

running same code on Spark 1.5.x and 1.6 will result in diff behavior
	starting Spark 1.6.0 memory management model changed
	can enable spark.memory.useLegacyMode if necessary

reserved memory
	RAM reserved for the system
		not used by spark in any way
		does not participate in Spark memory region size calculations
	hardcoded to 300MB
		can set spark.testing.reservedMemory but not recommended to use in prod
	sets the limit on what you can allocate for spark usage
		even if you wanted to give all the Java heap to spark to cache your data you can't
		need to set aside reserved memory for spark internal objects
	450MB min executor memory = 300MB reserved memory * 1.5 
		must give this minimum 150MB available to spark + user memory
		otherwise will get please use larger heap size error message

user memory
	store data structures
	totally up to you what would be stored in this RAM and how
	spark does not check if you respect this boundary or not > can lead to OOM error

spark memory
	memory pool managed by apache spark
	split into 2 regions
		storage memory
			store spark cached data
			store temp partition unroll data
				if there is not enough memory available to fit the whole partition > will write to disk
			store broadcast variables 
				in a cache with MEMORY_AND_DISK persistence
		execution memory
			store objects required during the execution of spark tasks
				ex: store shuffle intermediate buffer on map side in memory
				ex: store hash table for hash aggregation step
			also supports spilling to disk if not enough memory available
				but blocks cannot be forefully evicted by other threads (tasks)
		boundary set by spark.memory.storageFraction
			default to 0.5
			not static
			one region can grow by borrowing space from another
				cannot evict execution memory 
				can evict storage memory
					its just a cache of blocks stored in RAM
					can simply write to disk instead

java heap = total executor memory
450MB total executor memory minimum = 300MB reserved memory * 1.5
300MB default reserved memory used for spark internals
total executor memory - 300MB reserved memory = remaining user memory + spark memory
remaining = 25% user memory + 75% spark memory
user memory = (total executor memory - 300MB reserved memory) * (1.0 - 0.75 default spark.memory.fraction)
spark memory = (total executor memory - 300MB reserved memory) * 0.75
spark memory = default 50% storage memory + 50% execution memory
storage memory = (total executor memory - 300MB reserved memory) * 0.75 spark memory * 0.5 storage memory portion
