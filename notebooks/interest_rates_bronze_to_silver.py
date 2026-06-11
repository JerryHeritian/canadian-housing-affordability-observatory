#!/usr/bin/env python
# coding: utf-8

# ## interest_rates_bronze_to_silver
# 
# null

# In[ ]:


# Copy a source API in Bronze/interest_rate folder

import json
import requests

url = "https://www.bankofcanada.ca/valet/observations/B114039/json"

response = requests.get(url)

data = response.json()

with open("/lakehouse/default/Files/Bronze/interest_rate/interest_rates_raw.json", "w") as f:
    json.dump(data, f)


# In[16]:


# Read Json source, just copied

df_raw = spark.read \
    .format("json") \
    .load("Files/Bronze/interest_rate/interest_rates_raw.json")

df_raw.select("observations").show(truncate=False)


# In[21]:


# As the Json has his own format, so need to explode the Json to extract only observations content

from pyspark.sql.functions import explode

df_explode = df_raw.select(explode("observations").alias("observation"))

df_explode.show(5)
df_explode.printSchema()


# In[24]:


# explode the observation into d:date and v:value, so can get rid of B114039

df_interest_rates = df_explode.select(
    "observation.d",
    "observation.B114039.v"
)

df_interest_rates.show(5)
df_interest_rates.printSchema()


# In[31]:


# Get clean dataframe with readable header, and typed value

from pyspark.sql.functions import col, to_date

df_interest_rates_clean = df_interest_rates.select(
    to_date(col("d")).alias("date"),
    col("v").cast("double").alias("interest_rate")
)

df_interest_rates_clean.printSchema()
df_interest_rates_clean.show(5)


# In[32]:


# Save the result into a table named silver_interest_rates

df_interest_rates_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("silver_interest_rates")


# In[3]:


df = spark.read.table("silver_interest_rates")

df.show(10)
df.printSchema()
df.count()


# In[ ]:




