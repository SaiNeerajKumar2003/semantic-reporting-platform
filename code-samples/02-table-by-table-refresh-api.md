# Enhanced Refresh API: Table-by-Table Orchestration

**Insights 2.0 — Enterprise Analytics Platform Modernization**

Author: Sai Neeraj Kumar | Project: Insights 2.0 | Impact: 92% Refresh Improvement

---

## Executive Summary

The Enhanced Refresh API enables granular, table-by-table refresh orchestration instead of full-dataset refresh. By refreshing each table independently, this approach:

- Isolates failures to specific tables
- Provides granular performance monitoring
- Enables intelligent refresh sequencing
- Supports 3-4 refreshes per day instead of 1
- Maintains constant performance as data grows

**Key Achievement:** Reduced refresh time from 4 hours 15 minutes to 20 minutes through table-level orchestration combined with Incremental Refresh Policy.

---

## Problem Statement

### Before Table-by-Table Refresh

| Aspect | Impact |
|--------|--------|
| **Approach** | Full dataset deletion and re-import |
| **Duration** | 4 hours 15 minutes |
| **Failure Handling** | Entire dataset lost; restart from scratch |
| **Performance Visibility** | No insight into bottlenecks |
| **Frequency** | Once per day (limited by window) |
| **Individual Table Issues** | Cannot isolate or retry specific tables |
| **Scalability** | Time increases with data volume |

### After Table-by-Table Refresh

| Aspect | Improvement |
|--------|------------|
| **Approach** | Sequential table-by-table refresh (dimensions then facts) |
| **Duration** | 20 minutes |
| **Failure Handling** | Only failed table loses data; others preserved |
| **Performance Visibility** | Each table monitored independently |
| **Frequency** | 3-4 refreshes per day |
| **Individual Table Optimization** | Can retry or optimize specific tables |
| **Scalability** | Constant duration regardless of data volume |

---

## Technical Architecture

### Refresh Strategy

Table-by-table refresh requires intelligent sequencing to maintain data integrity:

**Refresh Order (Dependencies Matter)**

| Sequence | Table | Dependency | Duration |
|----------|-------|-----------|----------|
| 1 | DimDate | None (independent) | 2 minutes |
| 2 | DimCustomer | None (independent) | 3 minutes |
| 3 | DimProduct | None (independent) | 3 minutes |
| 4 | FactSales | Depends on dimensions | 12 minutes |

**Rationale:**
- Dimensions refresh first (no dependencies)
- Fact tables refresh after (depend on dimensions)
- Ensures referential integrity throughout refresh cycle
- Prevents foreign key constraint violations

### API Endpoints

**Refresh Trigger Endpoint**

```
Method:   POST
URL:      https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/datasets/{DATASET_ID}/refreshes
Purpose:  Trigger refresh for specific table
Response: HTTP 202 (Accepted) with requestId
```

**Refresh Status Endpoint**

```
Method:   GET
URL:      https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/datasets/{DATASET_ID}/refreshes
Purpose:  Get refresh history and current status
Response: List of refresh operations with status
```

### Request Payload Structure

| Element | Purpose | Value |
|---------|---------|-------|
| **type** | Refresh operation type | "full" |
| **commitMode** | Transaction semantics | "transactional" (all-or-nothing) |
| **applyRefreshPolicy** | Use incremental refresh | true |
| **retryCount** | Automatic retry attempts | 2 |
| **objects** | Tables to refresh | [{table: "DimDate"}, {table: "FactSales"}] |

---

## Implementation Details

### Authentication

**Service Principal Credentials**

| Component | Type | Purpose |
|-----------|------|---------|
| **Tenant ID** | Azure AD identifier | Organization context |
| **Client ID** | Service Principal | Application identity |
| **Client Secret** | Credential | Authentication token |

**Authentication Flow:**
1. Initialize MSAL (Microsoft Authentication Library)
2. Acquire token using service principal credentials
3. Include token in Bearer header for all API requests
4. Token auto-refreshes for long-running operations

### Error Handling & Resilience

**Throttling Strategy**

| Scenario | Handling |
|----------|----------|
| **Rate Limit (429)** | Read Retry-After header, wait, retry request |
| **Server Error (5xx)** | Exponential backoff with max 5 retries |
| **Network Timeout** | Automatic retry with 60-second timeout |
| **Session Token Expiry** | Automatic token refresh every 30 attempts |

**Benefits:**
- Handles API throttling gracefully
- Recovers from transient failures automatically
- Respects service rate limits
- Prevents cascading failures

### Monitoring & Logging

**Per-Table Metrics**

| Metric | Tracked | Use Case |
|--------|---------|----------|
| **Refresh Duration** | Each table | Identify slow tables |
| **Request ID** | Each refresh | Correlate with Power BI logs |
| **Status** | Completed/Failed/Timeout | Overall success tracking |
| **Error Messages** | Failure details | Debugging and alerts |

**Logging Format**

```
[2025-05-28 08:00:15] Triggering refresh for: DimDate
[2025-05-28 08:00:15] Request ID: abc123xyz
[2025-05-28 08:02:10] Final Status: Completed (Duration: 2.08 mins)
[2025-05-28 08:02:10] Triggering refresh for: DimCustomer
```

---

## Orchestration Flow

### Complete Pipeline Execution

```
PIPELINE START
│
├─ Authenticate (get access token)
│
├─ TABLE 1: DimDate
│  ├─ Wait for dataset idle
│  ├─ Trigger refresh (POST request)
│  ├─ Poll status every 5-30 seconds
│  ├─ Log: Completed (2 min)
│  │
├─ TABLE 2: DimCustomer
│  ├─ Wait for dataset idle
│  ├─ Trigger refresh
│  ├─ Poll status
│  ├─ Log: Completed (3 min)
│  │
├─ TABLE 3: DimProduct
│  ├─ Wait for dataset idle
│  ├─ Trigger refresh
│  ├─ Poll status
│  ├─ Log: Completed (3 min)
│  │
├─ TABLE 4: FactSales
│  ├─ Wait for dataset idle
│  ├─ Trigger refresh
│  ├─ Poll status
│  ├─ Log: Completed (12 min)
│
├─ Generate Summary Report
│  ├─ Total tables: 4
│  ├─ Successful: 4
│  ├─ Failed: 0
│  ├─ Total duration: 20 minutes
│
PIPELINE END
```

### Dataset Lock Management

**Concurrency Control**

| State | Behavior |
|-------|----------|
| **Idle** | Ready for refresh (no active operation) |
| **Refreshing** | Locked (prevents concurrent refresh) |
| **Failed/Cancelled** | Lock released; can retry |

**Implementation:**
- Before triggering each table, check dataset idle status
- Poll every 10 seconds
- Maximum wait: 60 minutes
- Timeout exception if dataset remains locked

---

## Performance Impact

### Refresh Time Breakdown

| Phase | Duration | Percentage |
|-------|----------|-----------|
| DimDate refresh | 2 minutes | 10% |
| DimCustomer refresh | 3 minutes | 15% |
| DimProduct refresh | 3 minutes | 15% |
| FactSales refresh | 12 minutes | 60% |
| **Total** | **20 minutes** | **100%** |

**Key Insight:** FactSales takes 60% of time because it contains most data. Dimensions complete quickly.

### Capacity Utilization

**Before Table-by-Table Refresh**

| Time | Activity | Capacity Used |
|------|----------|--------------|
| 0-255 min | Full dataset refresh | 85% |
| 255+ min | Normal operations | 15% |

**After Table-by-Table Refresh**

| Time | Activity | Capacity Used |
|------|----------|--------------|
| 0-20 min | Table-by-table refresh | 25% |
| 20+ min | Normal operations | 15% |

**Result:** Premium capacity utilization reduced from 85% to 25% during refresh window

### Scalability Model

Refresh duration remains constant as data volume grows:

| Scenario | Historical Data | Daily Refresh Duration | Frequency |
|----------|-----------------|----------------------|-----------|
| Year 1 | 365 days | 20 minutes | 4x daily |
| Year 2 | 730 days | 20 minutes | 4x daily |
| Year 3 | 1,095 days | 20 minutes | 4x daily |
| Year 5 | 1,825 days | 20 minutes | 4x daily |

**Why Constant Duration?**
- Incremental Refresh Policy limits queried data to 30 days
- Historical data never refreshed
- Table-by-table approach handles only incremental tables

---

## Failure Isolation Benefits

### Scenario: FactSales Refresh Fails

**Legacy Approach (Full Dataset Refresh):**
- Entire dataset lost
- All 20 reports inaccessible
- Must restart refresh from beginning
- Data unavailable 4+ hours
- Manual intervention required

**Table-by-Table Approach:**
- Only FactSales missing latest data
- DimDate, DimCustomer, DimProduct intact
- Can retry just FactSales table
- Retry takes 12 minutes
- System automatically retries

**Business Impact:**
- Reports show recent dimension data (most important)
- Facts show previous day (acceptable interim state)
- Dimensions updated automatically in retry
- No manual intervention needed

---

## Integration with Incremental Refresh

### Two-Tier Optimization

| Tier | Component | Responsibility | Data Reduction |
|------|-----------|---|---|
| **Tier 1** | Incremental Refresh Policy | Partition management (2y frozen + 30d incremental) | 95% volume reduction |
| **Tier 2** | Enhanced Refresh API | Table orchestration, sequencing, monitoring | Granular control |

**Combined Effect:**

```
Tier 1: Query only 30 days (95% reduction)
   ↓
Tier 2: Refresh DimDate (2 min)
        Refresh DimCustomer (3 min)
        Refresh DimProduct (3 min)
        Refresh FactSales (12 min)
   ↓
Result: 20-minute complete refresh
        with per-table visibility
        and failure isolation
```

---

## Operational Requirements

### Service Principal Setup

**Prerequisites:**

| Component | Configuration |
|-----------|---|
| **Azure AD Application** | Registered service principal |
| **Client Secret** | Generated and stored securely |
| **Workspace Access** | Service principal has Admin role |
| **API Permissions** | Power BI API enabled in Azure AD |

**Security Best Practice:** Store credentials in Azure Key Vault, not in code

### Scheduling

**Recommended Schedule**

| Property | Value | Rationale |
|----------|-------|-----------|
| **Frequency** | Daily | Refresh cycle frequency |
| **Time** | 8:00 AM | Outside peak hours |
| **Retry Schedule** | 2 attempts, 30-minute intervals | Handles transient failures |
| **Timeout** | 2 hours per table | Prevents indefinite hangs |

**Alternative Schedules:**

```
Option 1: Single Daily (Conservative)
  - 8:00 AM: Full refresh cycle

Option 2: Multiple Daily (Recommended)
  - 8:00 AM: Full refresh
  - 12:00 PM: Full refresh
  - 4:00 PM: Full refresh
  - 8:00 PM: Full refresh

Option 3: Incremental Frequency (Advanced)
  - Every 4 hours for incremental tables only
  - Less frequent for dimension tables
```

---

## Troubleshooting Guide

### Common Issues

| Issue | Root Cause | Resolution |
|-------|-----------|-----------|
| **All tables timeout** | Dataset permanently locked | Check Power BI Service for stuck refresh; restart capacity if needed |
| **Specific table always fails** | Table-level issue | Check table structure, partitions, and source query |
| **Throttling errors (429)** | Too frequent refreshes | Increase interval between refreshes |
| **Request ID missing** | Premium capacity behavior | Check Power BI logs; not critical (can recover) |
| **Token expiry mid-refresh** | Long-running operation | Auto-refresh every 30 attempts handles this |

### Validation Checklist

**Before First Refresh:**
- [ ] Service principal created and assigned Admin role
- [ ] Client secret stored securely
- [ ] Power BI API enabled in Azure AD
- [ ] Workspace ID and Dataset ID verified
- [ ] Test refresh on single table first

**After First Refresh:**
- [ ] All tables completed successfully
- [ ] Refresh duration near expectations (20 min)
- [ ] Logs show proper sequencing (dimensions before facts)
- [ ] Dataset accessible during and after refresh
- [ ] Premium capacity utilization acceptable

---

## Monitoring & Alerts

### Key Metrics to Track

| Metric | Alert Threshold | Action |
|--------|-----------------|--------|
| **Refresh Duration** | > 30 minutes | Investigate bottleneck; check data volume |
| **Failure Rate** | > 10% of refreshes | Review error logs; check table health |
| **Retry Attempts** | > 5 per month | Increase retry count or investigate source |
| **Capacity Usage** | > 50% during refresh | Extend refresh window or add capacity |

### Dashboard Components

**Real-Time Monitoring**

```
Current Status: In Progress
├─ DimDate:      ✓ Completed (2 min)
├─ DimCustomer:  ✓ Completed (3 min)
├─ DimProduct:   ✓ Completed (3 min)
└─ FactSales:    ⏳ Running (8 min elapsed)

Overall Progress: 16 of 20 minutes (80% complete)
Estimated End: 08:20 AM
```

**Historical Trending**

```
Last 30 Refreshes
├─ Successful: 28 (93%)
├─ Partial Failure: 2 (7%)
├─ Total Failures: 0
├─ Average Duration: 20.3 minutes
└─ Slowest: 23.5 minutes
```

---

## Related Documentation

### Code Implementation

The technical implementation details are available in:
- **02-table-by-table-refresh-api.py** — Python code for orchestration (complete source code)

### Architecture Documentation

- [Refresh Strategy Overview](../refresh-strategy.md) — Complete refresh architecture
- [Incremental Refresh Configuration](04-incremental-refresh-config.md) — Power BI partitioning setup
- [Project README](../README.md) — Complete project context

---

## Key Learnings

### What Table-by-Table Refresh Enables

| Capability | Benefit |
|-----------|---------|
| **Failure Isolation** | One table failure doesn't block entire dataset |
| **Performance Monitoring** | Know exactly which table is slow |
| **Selective Optimization** | Can target specific table improvements |
| **Independent Retry** | Retry failed tables without full restart |
| **Frequency Flexibility** | Can refresh 3-4 times daily |
| **Scalability** | Performance constant as data grows |

### What Requires Additional Setup

**Incremental Refresh Policy needed for:**
- Data volume reduction (query only 30 days instead of 2+ years)
- Constant refresh duration as data grows
- Non-blocking refresh window

**When Combined (Incremental + Enhanced API):**
- 95% volume reduction (Incremental)
- Granular table control (Enhanced API)
- 92% total improvement (4h 15m → 20m)

---

## Conclusion

The Enhanced Refresh API provides table-by-table orchestration that transforms refresh strategy from "full dataset or nothing" to "intelligent table sequencing with granular visibility."

Combined with Incremental Refresh Policy:
- Reduces data queried by 95%
- Orchestrates refresh table-by-table
- Maintains constant 20-minute duration
- Enables 3-4 daily refreshes
- Isolates failures to specific tables
- Provides per-table monitoring

This approach enabled Insights 2.0 to scale from 50 independent datasets to 1 shared semantic model while maintaining performance and reliability.

**Implementation Status:** Production, 4 tables, 20-minute refresh cycle

---

**Last Updated:** May 28, 2026 | **Status:** Active Production