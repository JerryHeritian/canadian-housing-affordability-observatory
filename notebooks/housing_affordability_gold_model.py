#!/usr/bin/env python
# coding: utf-8

# ## housing_affordability_gold_model
# 
# null

# In[1]:


# Read gold table to see schema

df_rental = spark.read.table("gold_rental_price")
df_housing = spark.read.table("gold_housing_price")
df_rates = spark.read.table("gold_interest_rates")
df_immigration = spark.read.table("gold_immigration")

df_rental.printSchema()
df_housing.printSchema()
df_rates.printSchema()
df_immigration.printSchema()


# In[2]:


# Rename columns

df_rental = df_rental \
    .withColumnRenamed("quarter_number", "quarter") \
    .withColumnRenamed("apartment_1_bedroom", "apartment_1_bedroom_rent") \
    .withColumnRenamed("apartment_2_bedrooms", "apartment_2_bedrooms_rent") \
    .withColumnRenamed("house_3_or_more_bedrooms", "house_3_or_more_bedrooms_rent") \
    .withColumnRenamed("room", "room_rent")

df_housing = df_housing \
    .withColumnRenamed("Apartment", "apartment_sale") \
    .withColumnRenamed("house", "house_sale")

df_immigration = df_immigration \
    .withColumnRenamed("quarter_number", "quarter")


# In[3]:


# Rental + housing price

df_fact_base = df_rental.join(
    df_housing,
    ["year", "quarter", "geography"],
    "left"
)


# In[4]:


# Add interest rates

df_fact_base = df_fact_base.join(
    df_rates,
    ["year", "quarter"],
    "left"
)


# In[5]:


# Add immigration

df_fact = df_fact_base.join(
    df_immigration,
    ["year", "quarter"],
    "left"
)


# In[6]:


# Adding date key

from pyspark.sql.functions import col, lit, concat

df_fact = df_fact.withColumn(
    "date_key",
    concat(col("year"), lit("_Q"), col("quarter"))
)


# In[7]:


# save table

df_fact.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("fact_housing_affordability")


# In[8]:


spark.read.table("fact_housing_affordability").show(10)


# In[ ]:




