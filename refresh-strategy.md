# Refresh Strategy: Two-Tier Approach

## Problem Statement

Legacy refresh approach required full dataset refresh of all 50 datasets daily, taking 4+ hours and causing infrastructure strain. Duplicate data existed across datasets, leading to redundant refresh operations. No visibility into individual table performance or failures.

## Solution: Two-Tier Refresh Strategy

### Tier 1: Power BI Incremental Refresh Policy

**Configuration**
- Historical partitions (2+ years): Frozen, no refresh
- Incremental partition (30 days): Daily refresh
- Partition elimination strategy reduces daily data volume by ~95%

**Implementation**
- Configured at dataset level in Power BI
- Automatic partition management
- Seamless data retention and refresh

**Benefit**
- Reduces import volume significantly
- Maintains complete historical context
- Enables fast incremental updates

### Tier 2: Enhanced Refresh API - Table-by-Table Orchestration

**Approach**
- Python-based orchestration using Enhanced Refresh API
- Individual table refresh instead of full dataset refresh
- Sequential refresh with monitoring

**Example Refresh Flow**
```
DimDate (5 min) → DimDepartment (2 min) → DimUser (3 min) → 
FactReporting (45 min) → FactTransactions (10 min)

Total: 20 minutes (vs 4 hours full refresh)
```

**Key Features**
- Table-level performance monitoring
- Failure isolation (one table failure doesn't block others)
- Granular error handling and retry logic
- Identifies bottleneck tables for optimization

**Implementation**
- Detects changed partitions
- Triggers refresh for affected tables
- Monitors individual table refresh status
- Records performance metrics per table
- Validates data quality after refresh

## Performance Results

| Metric | Before | After | Improvement |
|--------|--------|-------|------------|
| Refresh Duration | 4 hours 15 min | 20 minutes | 92% reduction |
| Success Rate | 85% | 99% | 14% improvement |
| Data Freshness | 4+ hours lag | 20 minutes | 12x better |
| Visibility | None | Per-table metrics | Complete |
| Failure Impact | Blocks all | Isolated to one table | Resilience |

## Technical Implementation

**Incremental Refresh Policy Configuration**
- Specifies historical and incremental date ranges
- Defines partition elimination strategy
- Configured per table requiring incremental behavior

**Enhanced Refresh API Integration**
- Service principal authentication
- API calls for table-level refresh triggering
- Status monitoring and completion detection
- Error handling with retry logic

**Orchestration Logic**
- Determines tables requiring refresh
- Sequencing of refresh operations
- Performance tracking and optimization
- Alerting on failures or performance degradation

## Failure Isolation Benefit

**Traditional Full Refresh**
- Entire dataset refresh fails
- All tables must be retried
- Extended downtime

**Table-by-Table Approach**
- Single table failure isolated
- Other tables already completed
- Only failed table requires retry
- Reduced impact and faster recovery

## Scalability

- Table-by-table approach scales with data growth
- Partition strategy supports increasing data volumes
- Individual table monitoring enables targeted optimization
- Supports parallel refresh of independent tables

## Continuous Optimization

Performance metrics enable identification of:
- Bottleneck tables (e.g., FactReporting consistently 45 minutes)
- Optimization opportunities (SQL query tuning, partition adjustment)
- Refresh time trends and patterns
- Infrastructure utilization

## Results

- 92% reduction in refresh duration (4 hours → 20 minutes)
- 99% success rate (reliable pipeline)
- Complete visibility into refresh performance
- Failure isolation improving resilience
- Foundation for continuous optimization

