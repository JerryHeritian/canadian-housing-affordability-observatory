#!/usr/bin/env python
# coding: utf-8

# ## immigration_bronze_to_silver
# 
# null

# In[3]:


# Read the CSV like a text to detect the format

df_raw = spark.read.text("Files/Bronze/immigration/Immigration_2000-2025.csv")

df_raw.show(20, truncate=False)


# In[1]:


# Create a filtered Dataframe to get only relevant data

df_csv = spark.read \
    .format("csv") \
    .option("header", "false") \
    .option("delimiter", "\t") \
    .load("Files/Bronze/immigration/Immigration_2000-2025.tsv")

df_filtered = df_csv.filter(
    df_csv._c0.isin(
        "Immigrants 3",
        "Net emigration 4 5",
        "Net non-permanent residents 10 11 12"
    )
)

df_filtered.show(truncate=False)


# In[3]:


# Create a new column named "metric", and adjust ligns name (Immigrants 3 -> Immigrants) 

from pyspark.sql.functions import when

df_filtered = df_filtered.withColumn(
    "metric",
    when(df_filtered._c0 == "Immigrants 3", "Immigrants")
    .when(df_filtered._c0 == "Net emigration 4 5", "Net emigration")
    .when(df_filtered._c0 == "Net non-permanent residents 10 11 12", "Net non-permanent residents")
)

df_filtered.select("_c0", "metric").show(truncate=False)
df_filtered.show(truncate=False)


# In[4]:


# Create dataframe containing only quarter

df_quarters = df_csv.filter(
    df_csv._c0 == "Components of population growth"
)

df_quarters.show(truncate=False)


# In[9]:


# Create silver dataframe

from pyspark.sql.functions import lit, col
from functools import reduce

quarter_row = df_quarters.first()

dfs = []

for c in df_filtered.columns:
    if c not in ["_c0", "metric"]:
        quarter_name = quarter_row[c]

        temp_df = df_filtered.select(
            lit(quarter_name).alias("quarter"),
            col("metric"),
            col(c).alias("value")
        )

        dfs.append(temp_df)

df_silver_immigration = reduce(
    lambda df1, df2: df1.union(df2),
    dfs
)

df_silver_immigration.show(20, truncate=False)


# In[13]:


# Clean value column, remove "," dans cast to integer

from pyspark.sql.functions import regexp_replace, col

df_silver_immigration_clean = df_silver_immigration.withColumn(
    "value", 
    regexp_replace(col("value"), ",", "").cast("integer")
)

df_silver_immigration_clean.printSchema()
df_silver_immigration_clean.show(20, truncate=False)


# In[14]:


df_silver_immigration_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("silver_immigration")


# In[16]:


spark.read.table("silver_immigration").show(20, truncate=False)


# In[18]:


spark.read.table("silver_immigration").count()


# In[ ]:




