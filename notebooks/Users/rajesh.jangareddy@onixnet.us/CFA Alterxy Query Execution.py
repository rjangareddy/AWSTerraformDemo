# Databricks notebook source
access_key = "AKIA4JV5MOVZZLRZUSWB"
secret_key = "X4RMDE83oFCxXfMpd5R93wBqBjg8CJ2iIxgTDCtZ"
encoded_secret_key = secret_key.replace("/", "%2F")
aws_bucket_name = "cfademos3loadbucket"
mount_name = "cfaonixdemobucket"


# COMMAND ----------

 sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", access_key)
 sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)

# COMMAND ----------

#dbutils.fs.mount("s3a://%s:%s@%s" % (access_key, encoded_secret_key, aws_bucket_name), "/mnt/%s" % mount_name)
# dbutils.fs.unmount("/mnt/cfaonixdemobucket")


# COMMAND ----------

display(dbutils.fs.ls("/mnt/%s" % mount_name))


# COMMAND ----------

df = spark.read.csv("dbfs:/mnt/cfaonixdemobucket/Output.sql", header="True")


# COMMAND ----------

lines = spark.sparkContext.textFile('dbfs:/mnt/cfaonixdemobucket/Output.sql')

squery = lines.collect()
final_sql =""
for l in squery:
    final_sql = final_sql +l.replace('""""','""')+'\n'

# COMMAND ----------

tempS3Dir = "s3a://cfaonixdemobucket/temp"


df_redshift = spark.read \
  .format("com.databricks.spark.redshift") \
  .option("url", "jdbc:redshift://redshift-cluster-demo.c5naqqipvcou.us-east-1.redshift.amazonaws.com:5439/dev") \
  .option("user","awsuser") \
  .option("password", "$marcell2020Onix") \
  .option("query", final_sql) \
  .option("aws_iam_role", "arn:aws:iam::845431993715:role/S3_Access_Role_For_Redshift") \
  .option("tempdir", tempS3Dir) \
  .load()

display(df_redshift)


# COMMAND ----------

df_redshift.write.format('jdbc').options(
      url='jdbc:redshift://redshift-cluster-demo.c5naqqipvcou.us-east-1.redshift.amazonaws.com:5439/dev',	  
      driver='com.amazon.redshift.jdbc42.Driver',
      dbtable='public.cfa_query_output_table',
      user='awsuser',
      password='$marcell2020Onix').mode('overwrite').save() 