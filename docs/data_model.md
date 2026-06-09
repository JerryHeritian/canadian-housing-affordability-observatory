# Data Model

## Dimension - Date
### Business Name
Date
### Description
Shared calendar dimension used across all datasets.
### Columns

- DateKey
- Date
- Year
- Quarter
- Month
- MonthName


## Dimension - Region
### Business Name
Region
### Description
Geographic dimension used to standardize provinces and Census Metropolitan Areas (CMAs).
### Columns
- RegionKey
- RegionName
- RegionType
- Province


## Dimension - Rental Unit Type
### Business Name
Rental Unit Type
### Description
Rental housing category used by Statistics Canada Quarterly Rent Statistics.
### Columns
- RentalUnitTypeKey
- RentalUnitType


## Dimension - Property Type
### Business Name
Property Type
### Description
Residential property category used by CREA Housing Price Index.
### Columns
- PropertyTypeKey
- PropertyType


## Fact Table - Interest Rates
### Source
Dataset #1 - Interest Rates
### Grain
Month
### Columns
- DateKey
- InterestRate


## Fact Table - Housing Prices
### Source
Dataset #2 - Housing Prices
### Grain
Month + Region + Property Type
### Columns
- DateKey
- RegionKey
- PropertyTypeKey
- BenchmarkPrice


## Fact Table - Rental Prices
### Source
Dataset #3 - Rental Prices
### Grain
Quarter + CMA + Rental Unit Type
### Columns
- DateKey
- RegionKey
- RentalUnitTypeKey
- AverageRent


## Fact Table - Immigration
### Source
Dataset #4 - Immigration
### Grain
Quarter + Province
### Columns
- DateKey
- RegionKey
- Immigrants
- Emigrants
- ReturningEmigrants
- NetTemporaryEmigration
- NetNonPermanentResidents


## Design Notes
- Interest rates are national indicators and do not require a RegionKey.
- Housing prices are analyzed by region and property type.
- Rental prices are analyzed by CMA and rental unit type.
- Immigration data is analyzed by province.
- DimDate is shared across all fact tables.
- DimRegion is shared across housing, rental, and immigration datasets.