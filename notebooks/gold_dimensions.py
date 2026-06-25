#!/usr/bin/env python
# coding: utf-8

# ## gold_dimensions
# 
# null

# In[3]:


# read fact table

df_fact = spark.read.table("fact_housing_affordability")

df_fact.show(5)


# In[4]:


# Adding column quarter_year

from pyspark.sql.functions import concat, col, lit

df_dim_date = df_fact.select(
    "year",
    "quarter",
    "date_key"
).distinct()

df_dim_date = df_dim_date.withColumn(
    "year_quarter",
    concat(col("year"), lit("-Q"), col("quarter"))
)

df_dim_date.show(5)


# In[5]:


# Save table dim date

df_dim_date.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("dim_date")


# In[6]:


# Select distinct geography

df_dim_geography = df_fact.select(
    "geography"
).distinct()


# In[7]:


# Add city column

from pyspark.sql.functions import split

df_dim_geography = df_dim_geography.withColumn(
    "city",
    split(col("geography"), ",").getItem(0)
)

df_dim_geography.show(5, truncate=False)


# In[8]:


# Save table

df_dim_geography.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("dim_geography")


# In[9]:


spark.read.table("dim_geography").show(5)


# In[10]:


spark.read.table("fact_housing_affordability").printSchema()
spark.read.table("dim_date").printSchema()


# In[ ]:




