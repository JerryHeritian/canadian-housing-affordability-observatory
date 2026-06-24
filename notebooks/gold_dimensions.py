#!/usr/bin/env python
# coding: utf-8

# ## gold_dimensions
# 
# null

# In[2]:


# read fact table

df_fact = spark.read.table("fact_housing_affordability")


# In[4]:


# Adding column quarter_year

from pyspark.sql.functions import concat, col, lit

df_dim_date = df_fact.select(
    "year",
    "quarter"
).distinct()

df_dim_date = df_dim_date.withColumn(
    "year_quarter",
    concat(
        col("year"),
        lit("-Q"),
        col("quarter")
    )
)

df_dim_date.show(5)


# In[6]:


# Save table dim date

df_dim_date.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("dim_date")


# In[8]:


# Select distinct geography

df_dim_geography = df_fact.select(
    "geography"
).distinct()


# In[14]:


# Add city column

from pyspark.sql.functions import split

df_dim_geography = df_dim_geography.withColumn(
    "city",
    split(col("geography"), ",").getItem(0)
)

df_dim_geography.show(5, truncate=False)


# In[15]:


# Save table

df_dim_geography.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("dim_geography")


# In[17]:


spark.read.table("dim_geography").show(5)


# In[ ]:




