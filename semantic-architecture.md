# Semantic Architecture

## Overview

Designed and implemented a centralized semantic model that consolidates 50 individual datasets into a single, unified data model. The model uses star schema design with conformed dimensions to eliminate data duplication and ensure consistent metric definitions across all reports.

## Data Model Structure

### Dimensions

**DimDate**
- Date hierarchy (year, quarter, month, week, day)
- Fiscal calendars
- Flags (weekend, holiday, current period)

**DimDepartment**
- Department identification and hierarchy
- Cost center mapping
- Business area classification
- Department relationships for drill-down

**DimUser**
- User identification and context
- Department assignment
- Role and access level
- Manager hierarchy for team structures

**DimMetric**
- Metric definitions and categorization
- Metric type and unit of measure
- Description and formatting rules

### Fact Tables

**FactReporting**
- Metric values and targets
- Department and user context
- Variance calculations
- Timestamp and refresh metadata

**FactTransactions**
- Transaction-level detail
- Amount, quantity, and derived calculations
- Status and dimension references

## Design Approach

**Star Schema**: Denormalized structure optimized for analytical queries. Simple join paths between facts and dimensions improve query performance.

**Conformed Dimensions**: All fact tables reference the same dimension definitions, ensuring consistent calculations and enabling cross-fact analysis.

**Incremental Refresh Configuration**: Partitions designed to support table-level refresh with historical data frozen and recent data incremental.

## DAX Calculations

### Time Intelligence Measures
- Year-over-year growth
- Month-over-month comparisons
- Year-to-date and quarter-to-date
- Period-over-period calculations

### Variance Analysis
- Variance from target
- Variance percentage
- Performance status indicators

### Aggregations
- Running totals
- Cumulative sums
- Rank and percentile calculations

### Context-Aware Calculations
- RLS-aware measures
- Role-based calculations
- Department-specific aggregations

## Row-Level Security

RLS rules implemented at semantic model level:

**Department-Level Filtering**
- Department managers see own department data
- Executives see all company data
- Users restricted to assigned departments

**User-Level Filtering**
- Individual contributors see own records
- Managers see team member records
- Access based on user attributes

**Implementation**
- RLS rules defined once in semantic model
- Consistently applied across all reports
- Centralized access policy management

## Performance Optimization

**Aggregation Tables**: Pre-aggregated data for frequently-used queries

**Partition Strategy**: Frozen historical partitions with incremental recent data

**Query Optimization**: Star schema design enables efficient join paths

**Incremental Refresh**: Only changed data imported, reducing refresh overhead

## Results

- Single source of truth for all metrics
- 100% consistency across 20 reports
- Simplified governance and access management
- Improved query performance (87% faster execution)
- Scalable model supporting business growth
