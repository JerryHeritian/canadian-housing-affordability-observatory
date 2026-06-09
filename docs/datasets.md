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
Date

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



## Dataset #3 — Rental Prices

### Source
Statistics Canada

https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=4610009201

### File
Rent_price_2019-2025.csv

### Business Name
Average Asking Rent

### Description
Quarterly Statistics Canada dataset providing average asking rents by rental unit type for Canadian Census Metropolitan Areas (CMAs).

### Raw Grain
Quarter + CMA + Rental Unit Type

### Gold Grain
Quarter + CMA

### Justification
Used to measure rental affordability across major Canadian metropolitan areas. This dataset complements CREA housing prices by providing rental market trends and supports analysis of the relationship between rents, immigration, and interest rates.



## Dataset #4 — Immigration

### Source
Statistics Canada

https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710004001

### File
Immigration_2000-2025.csv

### Table
17-10-0040-01

### Business Name
Immigration

### Description
Quarterly estimates of immigration and other international migration components for Canada and provinces.

### Raw Grain
Quarter + Province

### Gold Grain
Quarter + Province

### Justification
Used to analyze the relationship between immigration levels, housing prices, and rental affordability.