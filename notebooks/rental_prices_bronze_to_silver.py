#!/usr/bin/env python
# coding: utf-8

# ## rental_prices_bronze_to_silver
# 
# null

# In[2]:


# Checking the tsv structure

df_raw = spark.read \
    .format("csv") \
    .option("header", "false") \
    .option("delimiter", "\t") \
    .load("Files/Bronze/rental_prices/Rent_price_2019-2025.tsv")

df_raw.select("_c0", "_c1", "_c2", "_c3", "_c4").show(10, truncate=False)


# In[3]:


# Return dataframe containing Q1 2019, so all the quarters needed

df_quarters = df_raw.filter(
    df_raw._c2 == "Q1 2019"
)
df_quarters.select("_c0", "_c1", "_c2", "_c3", "_c4", "_c5").show(truncate=False)


# In[4]:


# Get relevant data with those filters

from pyspark.sql.functions import col

df_data = df_raw.filter(
    col("_c1").isin(
        "House - 3 or more bedrooms",
        "Apartment - 1 bedroom",
        "Apartment - 2 bedrooms",
        "Room"
    )
)

df_data.select("_c0", "_c1", "_c2", "_c3", "_c4").show(30, truncate=False)


# In[5]:


# Fill down the Geography

from pyspark.sql.functions import col, last, monotonically_increasing_id
from pyspark.sql.window import Window

df_numbered = df_data.withColumn(
    "row_id",
    monotonically_increasing_id()
)

window_spec = Window \
    .orderBy("row_id") \
    .rowsBetween(Window.unboundedPreceding, 0)

df_filled = df_numbered.withColumn(
    "geography",
    last(col("_c0"), ignorenulls=True).over(window_spec)
)

df_filled.select(
    "geography", "_c0", "_c1", "_c2", "_c3"
).show(20, truncate=False)


# In[6]:


# Clean dataframe

df_clean_base = df_filled.select(
    col("geography"),
    col("_c1").alias("rental_unit_type"),
    *[col(c) for c in df_filled.columns if c.startswith("_c") and c not in ["_c0", "_c1"]]
)

df_clean_base.show(10, truncate=False)


# In[11]:


# unpivot quarter to a columns into a rows

from pyspark.sql.functions import lit, col
from functools import reduce

quarter_row = df_quarters.first()

dfs = []

for c in df_clean_base.columns:
    if c not in ["geography", "rental_unit_type"]:
        quarter_name = quarter_row[c]

        temp_df = df_clean_base.select(
            lit(quarter_name).alias("quarter"),
            col("geography"),
            col("rental_unit_type"),
            col(c).alias("value")
        )

        dfs.append(temp_df)

df_silver_rental = reduce(
    lambda df1, df2: df1.union(df2), dfs
)

df_silver_rental.show(20, truncate=False)


# In[16]:


# Clean value column

from pyspark.sql.functions import col, regexp_replace, when

df_silver_rental_clean = df_silver_rental.withColumn(
    "value_clean_text",
    regexp_replace(col("value"), "E", "")
)

df_silver_rental_clean = df_silver_rental_clean.withColumn(
    "average_asking_rent",
    when(col("value_clean_text") == "..", None)
    .when(
        col("value_clean_text").contains(","),
        (regexp_replace(col("value_clean_text"), ",", ".").cast("double") * 1000).cast("integer")
    )
    .otherwise(col("value_clean_text").cast("integer"))
)

df_silver_rental_clean = df_silver_rental_clean.select(
    "quarter",
    "geography",
    "rental_unit_type",
    "average_asking_rent"
)

df_silver_rental_clean.printSchema()
df_silver_rental_clean.show(20, truncate=False)


# In[17]:


df_silver_rental_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("silver_rental_price")


# In[18]:


spark.read.table("silver_rental_price").show(20, truncate=False)


# In[ ]:




