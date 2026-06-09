# Architecture

## Overview

### Architecture Pattern

Medallion Architecture

### Flow

Bronze → Silver → Gold → Power BI

### Description

The project uses a Microsoft Fabric Lakehouse architecture to ingest, transform, and analyze housing affordability data across Canada.

---

## Bronze Layer

### Purpose

Store raw data exactly as received from source systems.

### Tables

- bronze_interest_rates
- bronze_housing_prices
- bronze_rental_prices
- bronze_immigration

### Description

Raw datasets are ingested without business transformations.

---

## Silver Layer

### Purpose

Clean, standardize and enrich source data.

### Tables

- silver_interest_rates
- silver_housing_prices
- silver_rental_prices
- silver_immigration

### Description

Data is cleaned, standardized and prepared for analytical modeling.

### Main Transformations

- Standardize dates
- Standardize region names
- Convert numeric fields
- Unpivot housing price categories
- Unpivot rental unit categories
- Prepare dimension tables

---

## Gold Layer

### Purpose

Provide business-ready datasets optimized for reporting and analytics.

### Dimensions

- DimDate
- DimRegion
- DimPropertyType
- DimRentalUnitType

### Fact Tables

- FactInterestRates
- FactHousingPrices
- FactRentalPrices
- FactImmigration

### Description

Gold tables follow a Star Schema design and are optimized for Power BI reporting.

---

## Reporting Layer

### Tool

Power BI

### Dashboards

#### Housing Prices

- Benchmark Price by Region
- Benchmark Price by Property Type

#### Rental Market

- Average Asking Rent by CMA
- Average Asking Rent by Rental Unit Type

#### Immigration

- Immigration Trends
- Immigration by Province

#### Housing Affordability

- Interest Rates vs Housing Prices
- Interest Rates vs Rental Prices
- Immigration vs Housing Prices
- Immigration vs Rental Prices

---

## Data Flow

### Dataset #1 - Interest Rates

bronze_interest_rates → silver_interest_rates → FactInterestRates

### Dataset #2 - Housing Prices

bronze_housing_prices → silver_housing_prices → FactHousingPrices

### Dataset #3 - Rental Prices

bronze_rental_prices → silver_rental_prices → FactRentalPrices

### Dataset #4 - Immigration

bronze_immigration → silver_immigration → FactImmigration

### Notes

Dimension tables are generated from Silver tables and shared across the Gold layer.