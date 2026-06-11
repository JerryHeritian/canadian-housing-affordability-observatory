#!/usr/bin/env python
# coding: utf-8

# ## interest_rates_silver_to_gold
# 
# null

# In[1]:


# Welcome to your new notebook

df = spark.read.table("silver_interest_rates")
df.show(5)


# In[2]:


# Create year, quarter, month column within gold dataframe

from pyspark.sql.functions import year, quarter, month, col

df_gold = df \
    .withColumn("year", year(col("date"))) \
    .withColumn("quarter", quarter(col("date"))) \
    .withColumn("month", month(col("date")))

df_gold.show(10)


# In[3]:


# Save gold table

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_interest_rates")


# In[4]:


spark.read.table("gold_interest_rates").show(10)


# In[ ]:




