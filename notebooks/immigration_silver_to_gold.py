#!/usr/bin/env python
# coding: utf-8

# ## immigration_silver_to_gold
# 
# null

# In[1]:


# Read silver_immigration table

df_silver = spark.read.table("silver_immigration")

df_silver.show(20, truncate=False)


# In[2]:


# Create new column quarter_number and year from quarter

from pyspark.sql.functions import substring, col

df_immigration_with_year = df_silver \
    .withColumn("quarter_number", substring(col("quarter"), 2, 1).cast("integer")) \
    .withColumn("year", substring(col("quarter"), 4, 4).cast("integer"))

df_immigration_with_year.printSchema() 
df_immigration_with_year.show(20, truncate=False)


# In[9]:


# Make a pivot on the dataframe, adding Immigrants, Net emigration and Net non-permanent residents

from pyspark.sql.functions import first

df_res = df_immigration_with_year \
    .groupBy("year", "quarter_number") \
    .pivot("metric") \
    .agg(first("value"))

df_res.show(20)


# In[11]:


# Rename column, delta issue

df_gold_immigration = df_res \
    .withColumnRenamed("Immigrants", "immigrants") \
    .withColumnRenamed("Net emigration", "net_emigration") \
    .withColumnRenamed("Net non-permanent residents", "net_non_permanent_residents")


# In[12]:


# Save table gold_immigrat
df_gold_immigration = df_gold_immigration.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_immigration")


# In[ ]:




