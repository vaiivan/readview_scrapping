from pyspark.sql import SparkSession
import pyspark.sql.types 
from pyspark.sql.types import *
import pyspark.sql.functions as F
import re
import requests
import base64
from dotenv import load_dotenv
import os

load_dotenv()

packages = [
    "org.apache.spark:spark-avro_2.12:2.4.4",
    "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1",
    "org.postgresql:postgresql:42.2.18"
]

POSTGRES_DB=os.getenv('POSTGRES_DB')
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .master('spark://spark:7077')\
    .config("spark.jars.packages",",".join(packages))\
    .getOrCreate()


df = spark.read.option("header", True).csv("books_in_print_raw_data.csv")
df.show()

df2 = df.drop('_id')
df2.show()
df2.printSchema()

df3 = df2.filter(df2['ISBN'].isNotNull())
df3.show()

def new_ISBN(ISBN):
    new_ISBN = ISBN.replace("-","")
    return new_ISBN
udfNewISBN = F.udf(new_ISBN, StringType())

df4 = df3.withColumn('New ISBN', udfNewISBN(df3['ISBN']))
df4.show()
df4 = df4.drop(df4['ISBN'])
df4.show()

def correct_date(date):
    date_Regex = re.compile(r'(\w{3}\ \d{4})')
    if date == None:
        return None
    elif date_Regex.match(date):
        return date
    else:
        return None
udfNewDate = F.udf(correct_date, StringType())

df5 = df4.withColumn("New Date", udfNewDate(df4['publish_date']))
df5.show()
df5 = df5.drop(df5['publish_date'])
df5.show()
df5 = df5.filter(df5["New Date"].isNotNull())
df5.show()

def remove_digits(title):
    title_regex = r'^\d+\.'
    correct_title = re.sub(title_regex, "", title).strip()
    return correct_title
udfNewTitle = F.udf(remove_digits, StringType())

df6 = df5.withColumn("New Title", udfNewTitle(df5['title']))
df6.show()
df6 = df6.drop(df6['title'])
df6.show()

df6 = df6.withColumnRenamed("New ISBN", "isbn")
df6 = df6.withColumnRenamed("New Date", "publish_date")
df6 = df6.withColumnRenamed("New Title", "title")
df6 = df6.drop(df6['created_at'])
df6.show(10)

df7 = df6.dropDuplicates(['isbn','author','book_picture','publisher','publish_date','title'])
df7.show(10)
# df7.coalesce(1).write.format("com.databricks.spark.csv").option("header", "true").mode("overwrite").save("mydata6.csv")

def convert_pic(image_url, isbn):
    r = requests.get(image_url)
    with open("{}.png".format(isbn),'wb') as f:
        f.write(r.content)
        
    with open("{}.png".format(isbn), "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        # print(my_string.decode('utf-8'))
        if os.path.exists("{}.png".format(isbn)):
            os.remove("{}.png".format(isbn))
        # print("changed {} to base64".format(isbn))
            return my_string.decode('utf-8')
            
udfimginBase64 = F.udf(convert_pic, StringType())
df8 = df7.withColumn("book_cover", udfimginBase64(df7['book_picture'], df7['isbn']))
print("df2 count", df2.count())
print("df3 count", df3.count())
print("df4 count", df4.count())
print("df6 count", df6.count())
print("df7 count", df7.count())
print("df8 count", df8.count())

print('writing to CSV')
df8.repartition(1).write.format("com.databricks.spark.csv").option("header", "true").save("mydata2.csv")

df8 = df8.drop(df8['book_picture'])
df8.show(10)


