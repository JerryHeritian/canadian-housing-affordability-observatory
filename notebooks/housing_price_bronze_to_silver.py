#!/usr/bin/env python
# coding: utf-8

# ## housing_price_bronze_to_silver
# 
# null

# In[ ]:


# Read all data from tsv files, and add in one dataframe

from pyspark.sql.functions import lit, col, expr
from functools import reduce

files = {
    "CALGARY.tsv": "Calgary, Census metropolitan area (CMA)",
    "EDMONTON.tsv": "Edmonton, Census metropolitan area (CMA)",
    "WINNIPEG.tsv": "Winnipeg, Census metropolitan area (CMA)",
    "VICTORIA.tsv": "Victoria, Census metropolitan area (CMA)",
    "HALIFAX_DARTMOUTH.tsv": "Halifax, Census metropolitan area (CMA)",
    "MONTREAL_CMA.tsv": "Montréal, Census metropolitan area (CMA)",
    "QUEBEC_CMA.tsv": "Québec, Census metropolitan area (CMA)",
    "OTTAWA.tsv": "Ottawa – Gatineau (Ontario part), Census metropolitan area (CMA)"
}

dfs = []

for file_name, geography in files.items():
    df = spark.read \
        .format("csv") \
        .option("header", "true") \
        .option("delimiter", "\t") \
        .load(f"Files/Bronze/housing_prices/{file_name}") \
        .withColumn("geography", lit(geography))
    dfs.append(df)

df_all = reduce(
    lambda df1, df2: df1.unionByName(df2), dfs
)

df_all.show(10, truncate=False)


# In[ ]:


# Unpivot column Apartment_Benchmark_SA and Single_Family_Benchmark_SA in house_type

df_silver_housing = df_all.select(
    col("date").alias("date_raw"),
    col("geography"),
    expr("""
        stack(
            2,
            'Apartment', Apartment_Benchmark_SA,
            'house', Single_Family_Benchmark_SA
        ) as (house_type, benchmark_price)
    """)
)

df_silver_housing.show(20, truncate=False)


# In[ ]:


#

df_silver_housing.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("silver_housing_price")

spark.read.table("silver_housing_price").show(20, truncate=False)


# In[ ]:




