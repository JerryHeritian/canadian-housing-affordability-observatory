#!/usr/bin/env python
# coding: utf-8

# ## interest_rates_silver_to_gold
# 
# null

# In[18]:


# Welcome to your new notebook

df = spark.read.table("silver_interest_rates")
df.show(5)


# In[19]:


# Create year, quarter, month column within gold dataframe

from pyspark.sql.functions import year, quarter, month, col

df_gold = df \
    .withColumn("year", year(col("date"))) \
    .withColumn("quarter", quarter(col("date"))) \
    .withColumn("month", month(col("date")))

df_gold.show(10)


# In[20]:


# Aggregate average of interest rate for each quarter

from pyspark.sql.functions import avg

df_gold_interest_rate = df_gold \
    .groupBy("year", "quarter") \
    .agg(
        avg("interest_rate").alias("interest_rate")
    )

df_gold_interest_rate.show(10)


# In[21]:


df_gold_interest_rate.printSchema()


# In[22]:


# Save gold table

df_res.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("gold_interest_rates")


# In[23]:


spark.read.table("gold_interest_rates").show(20)


# In[ ]:




