#!/usr/bin/env python
# coding: utf-8

# ## rental_prices_silver_to_gold
# 
# null

# In[3]:


# Read silver_rental_price

df_silver = spark.read.table("silver_rental_price")

df_silver.show(20, truncate=False)


# In[18]:


# Extract quarter_number and year

from pyspark.sql.functions import substring, col

df_rental_with_year_quarter = df_silver \
    .withColumn("quarter_number", substring(col("quarter"), 2, 1).cast("integer")) \
    .withColumn("year", substring(col("quarter"), 4, 4).cast("integer"))

df_rental_with_year_quarter.show(20, truncate=False)
df_rental_with_year_quarter.count()


# In[24]:


# make a pivot on rental_unit_type

from pyspark.sql.functions import first

df_res = df_rental_with_year_quarter \
    .groupBy("year", "quarter_number", "geography") \
    .pivot("rental_unit_type") \
    .agg(first("average_asking_rent"))

df_res.show(20, truncate=False)
df_res.count()


# In[25]:


# rename the columns as delta doesn't accept some special character including space

df_res = df_res \
    .withColumnRenamed("Apartment - 1 bedroom", "apartment_1_bedroom") \
    .withColumnRenamed("Apartment - 2 bedrooms", "apartment_2_bedrooms") \
    .withColumnRenamed("House - 3 or more bedrooms", "house_3_or_more_bedrooms") \
    .withColumnRenamed("Room", "room")

df_res.printSchema()


# In[26]:


# Save the table gold_rental_price

df_gold_rental_price = df_res.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_rental_price")


# In[28]:


spark.read.table("gold_rental_price").show(20)


# In[ ]:




