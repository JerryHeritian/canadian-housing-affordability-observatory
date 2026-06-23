#!/usr/bin/env python
# coding: utf-8

# ## housing_price_silver_to_gold
# 
# null

# In[1]:


# Read silver table

df_silver = spark.read.table("silver_housing_price")

df_silver.printSchema()
df_silver.show(20, truncate=False)


# In[2]:


# Extract year and month from date_raw

from pyspark.sql.functions import substring, col, split

df_date = df_silver.withColumn(
    "year", split(col("date_raw"), " ").getItem(1).cast("integer")
) \
.withColumn(
    "month", split(col("date_raw"), " ").getItem(0)
)

df_date.show(10)


# In[30]:


# Create column month_number

from pyspark.sql.functions import col, when

df_date = df_date.withColumn(
    "month_number",
    when(col("month").startswith("jan"), 1) \
    .when(col("month").startswith("fév"), 2) \
    .when(col("month").startswith("mar"), 3) \
    .when(col("month").startswith("avr"), 4) \
    .when(col("month").startswith("mai"), 5) \
    .when(col("month").startswith("juin"), 6) \
    .when(col("month").startswith("juil"), 7) \
    .when(col("month").startswith("aoû"), 8) \
    .when(col("month").startswith("sep"), 9) \
    .when(col("month").startswith("oct"), 10) \
    .when(col("month").startswith("nov"), 11) \
    .when(col("month").startswith("déc"), 12) \

)

df_date.show(5, truncate=False)


# In[31]:


# Create quarter column from month number

df_date = df_date.withColumn(
    "quarter",
    ((col("month_number") - 1) /3).cast("integer") + 1
)

df_date.show(20, truncate=False)


# In[32]:


# Select only column needed for gold

df_clean = df_date.select(
    col("quarter"),
    col("year"),
    col("geography"),
    col("house_type"),
    col("benchmark_price")
)

df_clean.show(5, truncate=False)


# In[37]:


# Make a pivot on house_type

from pyspark.sql.functions import first, avg

df_res = df_clean \
    .groupBy("year", "quarter", "geography") \
    .pivot("house_type") \
    .agg(avg("benchmark_price").cast("integer"))

df_res.show(10, truncate=False)


# In[38]:


df_gold_housing_price = df_res.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_housing_price")


# In[41]:


spark.read.table("gold_housing_price").show(20, truncate=False)


# In[ ]:




