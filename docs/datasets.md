# Dataset Inventory

## Dataset #1 - Interest Rates

### Source
Bank of Canada Valet API

### Endpoint
https://www.bankofcanada.ca/valet/observations/B114039/json

### Series
B114039

### Business Name
Target Rate (Policy Interest Rate)

### Description
Official Bank of Canada policy interest rate.

### Raw Grain
Rate change date

### Gold Grain
Month

### Justification
Used to measure the impact of monetary policy on housing affordability.



## Dataset #2 — Housing Prices

### Source
CREA (Canadian Real Estate Association)

https://stats.crea.ca/en-CA/

### File
Seasonally Adjusted (M).xlsx

### Business Name
Composite Benchmark Price

### Description
Benchmark home price published by CREA. Represents the value of a typical residential property and is widely used by Canadian housing market analysts.

### Raw Grain
Month + Region

### Gold Grain
Month + Region

### Justification
Used to measure housing affordability across Canadian regions. Benchmark Price is preferred over Average Sale Price because it better reflects the value of a typical property and reduces distortions caused by luxury or atypical sales.








## Dataset #4 - Immigration

### Source
Statistics Canada

### Table
17-10-0040-01

### Business Name
Quarterly Immigration Components

### Description
Quarterly estimates of immigrants, emigrants, returning emigrants, temporary emigration and non-permanent residents for Canada and provinces.

### Raw Grain
Province + Quarter

### Gold Grain
Province + Quarter

### Justification
Used to analyze the relationship between immigration and housing affordability indicators such as house prices and rents.