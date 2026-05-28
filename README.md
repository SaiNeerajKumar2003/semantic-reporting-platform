# 📊 Insights 2.0: Enterprise Analytics Platform Modernization

## 🎯 Project Summary

Designed and implemented a comprehensive enterprise analytics platform modernization that consolidated 50 fragmented Power BI reports into 20 standardized solutions. Architected a two-tier refresh strategy combining Power BI's native incremental refresh with Enhanced Refresh API orchestration, reducing refresh cycles from **4 hours to 20 minutes**. Built a centralized embedded analytics portal with department and user-level access control serving **1000+ users**.

---

## 📈 Key Results at a Glance

| Metric | Before | After | Improvement |
|--------|--------|-------|------------|
| ⏱️ **Refresh Duration** | 4 hours 15 min | 20 minutes | **92% ↓** |
| 📑 **Reports** | 50 fragmented | 20 consolidated | **60% ↓** |
| 💾 **Datasets** | 50 individual | 1 semantic model | **100% ✓** |
| ✅ **Success Rate** | 85% | 99% | **14% ↑** |
| 🔄 **Duplicate Refreshes** | 50 daily | Eliminated | **100% ✓** |
| ⚡ **Query Speed** | 8-12 sec | 1-2 sec | **87% ↓** |
| 📊 **Dashboard Load** | 30-45 sec | 3-5 sec | **91% ↓** |
| 👥 **Portal Capacity** | Manual | 1000+ users | **✓ Enterprise** |

---

## 💻 Code Samples — Proof of Implementation

**See `/code-samples/` folder for actual working code:**

| Artifact | What It Proves | Lines |
|----------|---|---|
| **[01-embed-token-generation.py](/code-samples/01-embed-token-generation.py)** | Built portal with RLS security | 230 |
| **[02-table-by-table-refresh-api.py](/code-samples/02-table-by-table-refresh-api.py)** | Orchestrated 92% refresh improvement | 570 |
| **[03-dax-time-intelligence-offset.dax](/code-samples/03-dax-time-intelligence-offset.dax)** | Advanced DAX beyond standard functions | 500+ |
| **[04-incremental-refresh-config.md](/code-samples/04-incremental-refresh-config.md)** | Configured Power BI native optimization | 280 |

**[→ Full code-samples README](/code-samples/README.md)** explaining each artifact

---

## 🏗️ Architecture Transformation

### ❌ TRADITIONAL DISTRIBUTED APPROACH (BEFORE)

```
┌─────────────────────────────────────────────────────────────────┐
│                   FRAGMENTED ARCHITECTURE                       │
│                                                                  │
│  50 POWER BI REPORTS                                            │
│  ├─ Report 1  →  Dataset 1  →  ┐                              │
│  ├─ Report 2  →  Dataset 2  →  │                              │
│  ├─ Report 3  →  Dataset 3  →  │  SAME DATA                  │
│  ├─ Report 4  →  Dataset 4  →  │  DUPLICATED                 │
│  ├─ Report 5  →  Dataset 5  →  │  50 TIMES                   │
│  ├─ ...                          │                              │
│  └─ Report 50 →  Dataset 50 → ┘                              │
│                                                                  │
│                    SQL SERVER TABLES                            │
│                                                                  │
│  ❌ CHALLENGES:                                                 │
│     • Data duplication (50 copies of same data)                │
│     • All 50 datasets refresh daily (wasteful)                 │
│     • 50 different metric definitions (inconsistent)           │
│     • Metrics in Report 1 ≠ Metrics in Report 2               │
│     • 4+ hour refresh cycles (infrastructure strain)           │
│     • Manual access control (governance nightmare)             │
│     • Difficult to add new reports (must create dataset)       │
│     • High operational overhead                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### ✅ CENTRALIZED SEMANTIC MODEL APPROACH (AFTER)

```
┌─────────────────────────────────────────────────────────────────┐
│                 CENTRALIZED ARCHITECTURE                        │
│                                                                  │
│           ┌─────────────────────────────────────┐              │
│           │  CENTRALIZED SEMANTIC MODEL         │              │
│           │  (Power BI - Star Schema)          │              │
│           │                                     │              │
│           │  DIMENSIONS:                        │              │
│           │  • DimDate (with hierarchies)      │              │
│           │  • DimDepartment (organization)    │              │
│           │  • DimUser (access control)        │              │
│           │  • DimMetric (categorization)      │              │
│           │                                     │              │
│           │  FACTS:                             │              │
│           │  • FactReporting                    │              │
│           │  • FactTransactions                │              │
│           │                                     │              │
│           │  DAX MEASURES:                      │              │
│           │  • YoY Growth, Variance, etc.      │              │
│           │  • 50-100+ Calculations (ONCE)     │              │
│           │                                     │              │
│           │  RLS RULES:                         │              │
│           │  • Department-level filtering      │              │
│           │  • User-level filtering             │              │
│           │  • Centralized & Consistent        │              │
│           └──────────────┬──────────────────────┘              │
│                          │                                      │
│                          ↓                                      │
│           ┌──────────────────────────┐                        │
│           │  20 REPORTS              │                        │
│           │  (All using same model)  │                        │
│           │                          │                        │
│           │  ✓ Consistent metrics    │                        │
│           │  ✓ Same RLS rules        │                        │
│           │  ✓ Unified data          │                        │
│           └──────────────┬───────────┘                        │
│                          │                                      │
│                          ↓                                      │
│           ┌──────────────────────────┐                        │
│           │  ANALYTICS PORTAL        │                        │
│           │                          │                        │
│           │  • Azure AD SSO          │                        │
│           │  • Dept-level filtering  │                        │
│           │  • User-level access     │                        │
│           │  • 1000+ users           │                        │
│           └──────────────────────────┘                        │
│                                                                  │
│                  SQL SERVER TABLES                              │
│                                                                  │
│  ✅ BENEFITS:                                                   │
│     ✓ Single data source (no duplication)                      │
│     ✓ One metric definition (100% consistent)                  │
│     ✓ Centralized RLS (governance)                             │
│     ✓ 20-minute refresh (efficient)                            │
│     ✓ Easy to add reports (reuse model)                        │
│     ✓ Enterprise-grade security                                │
│     ✓ Scalable & maintainable                                  │
│     ✓ Better cost efficiency                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⭐ Semantic Model: Star Schema Design

```
                          ┌──────────────┐
                          │   DIM_DATE   │
                          ├──────────────┤
                          │ DateKey (PK) │
                          │ Date         │
                          │ Year, Month  │
                          │ Quarter, Week│
                          │ DayOfWeek    │
                          │ IsWeekend    │
                          └──────┬───────┘
                                 │
                  ┌──────────────┼──────────────┐
                  │              │              │
        ┌─────────▼────────┐     │    ┌─────────▼────────┐
        │  DIM_DEPARTMENT  │     │    │   DIM_USER       │
        ├──────────────────┤     │    ├──────────────────┤
        │ DepartmentKey(PK)│     │    │ UserKey (PK)     │
        │ Department ID    │     │    │ UserID           │
        │ Dept Name        │     │    │ Full Name        │
        │ Dept Head        │     │    │ Department (FK)  │
        │ Cost Center      │     │    │ Manager ID       │
        │ Business Area    │     │    │ Role             │
        └────────┬─────────┘     │    │ Access Level     │
                 │               │    └────────┬─────────┘
                 └───────────────┼────────────┘
                                 │
                        ┌────────▼────────┐
                        │ FACT_REPORTING  │
                        ├─────────────────┤
                        │ ReportingKey(PK)│
                        │ DateKey (FK)    │
                        │ DepartmentKey(F)│
                        │ UserKey (FK)    │
                        │ MetricKey (FK)  │
                        │ MetricValue     │
                        │ MetricTarget    │
                        │ Variance        │
                        │ Timestamp       │
                        └────────┬────────┘
                                 │
                        ┌────────▼──────────┐
                        │  DIM_METRIC       │
                        ├───────────────────┤
                        │ MetricKey (PK)    │
                        │ MetricID          │
                        │ Metric Name       │
                        │ Category          │
                        │ Type              │
                        │ Unit of Measure   │
                        └───────────────────┘

KEY BENEFITS:
✓ Shared across ALL 20 reports
✓ Conformed dimensions (consistent)
✓ Star schema (optimized for analytics)
✓ Single metric definition
✓ Centralized RLS rules
✓ Easy to maintain & extend
```

---

## 🔄 Refresh Strategy: Two-Tier Optimization

### LEGACY FULL REFRESH (4+ HOURS)

```
┌────────────────────────────────────────────────────────────────┐
│  Step 1: DELETE ALL DATA                                       │
│  └─ Clear all 50 datasets completely                          │
│                                                                 │
│  Step 2: RE-IMPORT EVERYTHING                                  │
│  └─ Import 2+ years of historical data (all unchanged)        │
│  └─ Import 30 days of incremental data                        │
│  └─ Duration: ~2.5 hours                                      │
│                                                                 │
│  Step 3: RECALCULATE ALL                                       │
│  └─ Rebuild all aggregations                                  │
│  └─ Recalculate all measures                                  │
│  └─ Duration: ~1 hour                                         │
│                                                                 │
│  Step 4: VALIDATE & INDEX                                      │
│  └─ Duration: ~0.5 hours                                      │
│                                                                 │
│  ❌ TOTAL: 4+ HOURS                                            │
│  ❌ If ANY step fails: Entire process must retry              │
│  ❌ All infrastructure heavily utilized                        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

### ✅ NEW TWO-TIER REFRESH (20 MINUTES)

```
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│  TIER 1: POWER BI INCREMENTAL REFRESH POLICY                  │
│  ┌──────────────────────────────────────────────────────┐     │
│  │  Historical Data (2+ years)  │ Incremental (30 days)│     │
│  │  ┌──────────────────────┐    │ ┌──────────────────┐ │     │
│  │  │ FROZEN               │    │ │ REFRESH DAILY   │ │     │
│  │  │ • No import          │    │ │ • Import only   │ │     │
│  │  │ • No refresh         │    │ │   new data      │ │     │
│  │  │ • Already in model   │    │ │ • ~95% volume   │ │     │
│  │  │                      │    │ │   reduction     │ │     │
│  │  └──────────────────────┘    │ └──────────────────┘ │     │
│  │                                                       │     │
│  │  Result: Partition elimination handles 95% of work  │     │
│  │  Time: ~2 minutes                                   │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  TIER 2: ENHANCED REFRESH API - TABLE-BY-TABLE                │
│  ┌──────────────────────────────────────────────────────┐     │
│  │                                                       │     │
│  │  DimDate         ──→   5 min  ✓ COMPLETE            │     │
│  │  DimDepartment   ──→   2 min  ✓ COMPLETE            │     │
│  │  DimUser         ──→   3 min  ✓ COMPLETE            │     │
│  │  FactReporting   ──→  45 min  ✓ COMPLETE (isolated) │     │
│  │  FactTransactions──→  10 min  ✓ COMPLETE            │     │
│  │                                                       │     │
│  │  IF FactReporting FAILS:                             │     │
│  │  └─ Only FactReporting retries                       │     │
│  │  └─ Other 4 tables already live & producing data    │     │
│  │  └─ Users get 80% fresh data (4/5 tables)           │     │
│  │                                                       │     │
│  │  Result: Complete visibility + failure isolation     │     │
│  │  Time: ~20 minutes total                             │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  ✅ TOTAL: 20 MINUTES (92% FASTER)                            │
│  ✅ One table failure ≠ total failure                         │
│  ✅ Granular performance monitoring                           │
│  ✅ Infrastructure utilization optimized                      │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 🌐 Portal Access Control Flow

```
USER ACCESSES PORTAL (portal.company.com)
            │
            ↓
    ┌──────────────────────┐
    │  AZURE AD LOGIN      │
    │  (Single Sign-On)    │
    │                      │
    │  User: sjkumar       │
    │  Dept: Sales         │
    │  Role: Manager       │
    └──────────┬───────────┘
               │
               ↓
    ┌──────────────────────┐
    │  IDENTIFY USER       │
    │  └─ Department: Sales│
    │  └─ Role: Manager    │
    │  └─ Access Lvl: 2    │
    └──────────┬───────────┘
               │
               ↓
    ┌──────────────────────────────┐
    │  REPORT DISCOVERY ENGINE     │
    │  Query: Show reports for     │
    │  • Department = Sales        │
    │  • Access Level >= 2         │
    │  • Role = Manager            │
    └──────────┬───────────────────┘
               │
               ↓
    ┌──────────────────────────────┐
    │  AVAILABLE REPORTS:          │
    │  ✓ Sales Dashboard           │
    │  ✓ Sales Performance         │
    │  ✓ Regional Analysis         │
    │  ✗ Finance Reports (hidden)  │
    │  ✗ HR Data (hidden)          │
    │  ✗ Board Reports (hidden)    │
    └──────────┬───────────────────┘
               │
         User Selects:
         Sales Dashboard
               │
               ↓
    ┌──────────────────────┐
    │  PERMISSION CHECK    │
    │  ✓ User has access   │
    │  ✓ Continue          │
    └──────────┬───────────┘
               │
               ↓
    ┌──────────────────────────────┐
    │  GENERATE EMBED TOKEN        │
    │  WITH RLS CONTEXT            │
    │  • Department = Sales        │
    │  • UserID = sjkumar          │
    │  • Role = Manager            │
    └──────────┬───────────────────┘
               │
               ↓
    ┌──────────────────────────────┐
    │  EMBED POWER BI REPORT       │
    │  (Secure token + RLS applied)│
    │                              │
    │  RLS Automatic Filtering:    │
    │  ✓ Show: Sales data only     │
    │  ✓ Hide: Finance data        │
    │  ✓ Show: Manager-level view  │
    │  ✓ Hide: Confidential data   │
    └──────────┬───────────────────┘
               │
               ↓
    ┌──────────────────────────────┐
    │  USER SEES FILTERED REPORT   │
    │  • Sales dept metrics        │
    │  • Team member data          │
    │  • Appropriate detail level  │
    │  • No access to other depts  │
    └──────────────────────────────┘
```

---

## 📊 Performance Improvements Visualization

```
REFRESH DURATION IMPROVEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEFORE:  ████████████████████████████████████████████  4 HOURS
AFTER:   ████  20 MINUTES

IMPROVEMENT: ↓ 92% FASTER


QUERY EXECUTION TIME IMPROVEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEFORE:  ██████████  8-12 seconds
AFTER:   ██  1-2 seconds

IMPROVEMENT: ↓ 87% FASTER


DASHBOARD LOAD TIME IMPROVEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEFORE:  ██████████████████  30-45 seconds
AFTER:   ██  3-5 seconds

IMPROVEMENT: ↓ 91% FASTER


DATASETS & CONSOLIDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEFORE:  50 Individual Datasets
         ██████████████████████████████████████████████ 50

AFTER:   1 Shared Semantic Model
         ██ 1

IMPROVEMENT: ✓ 100% CONSOLIDATED
```

---

## 🏢 Architecture Layers

```
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│ 4️⃣  PRESENTATION LAYER                                         │
│     ├─ 20 Standardized Power BI Reports                       │
│     ├─ Embedded in Portal                                      │
│     └─ Department-Specific Dashboards                         │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 3️⃣  SEMANTIC LAYER (Centralized)                              │
│     ├─ Star Schema Design                                      │
│     ├─ Dimensions + Fact Tables                               │
│     ├─ DAX Measures (50-100+)                                 │
│     ├─ RLS Rules (Dept + User Level)                          │
│     └─ Single Source of Truth                                 │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 2️⃣  REFRESH LAYER (Two-Tier Orchestration)                    │
│     ├─ Power BI Incremental Refresh Policy                    │
│     ├─ Enhanced Refresh API (Python)                          │
│     ├─ Table-by-Table Refresh                                 │
│     ├─ Performance Monitoring                                 │
│     └─ Error Handling & Recovery                              │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1️⃣  DATA WAREHOUSE LAYER                                       │
│     ├─ SQL Server Tables                                       │
│     ├─ Dimensions                                             │
│     ├─ Facts with Partitions                                  │
│     ├─ Incremental Load Strategy                              │
│     └─ Data Quality Validation                                │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 💡 Key Design Decisions

**Why Semantic Consolidation?**
> 50 individual datasets led to duplicate data, inconsistent calculations, and governance challenges. A centralized semantic model provides single source of truth, eliminates redundancy, and simplifies maintenance.

**Why Two-Tier Refresh?**
> Combining Power BI's incremental refresh (handles 95% of volume reduction efficiently) with Enhanced Refresh API (provides granular control and monitoring) achieves both speed and visibility that neither approach alone provides.

**Why Portal-Based Distribution?**
> Centralized portal with integrated access control is more scalable and maintainable than scattered reports with individual permissions. Automated department and user-level filtering via RLS ensures consistent data access policies.

**Why RLS at Semantic Layer?**
> Defining RLS rules once in semantic model ensures consistency across all reports, eliminates duplication, and provides single point of control for access policies.

---

## 💻 Technology Stack

```
POWER BI & ANALYTICS          BACKEND & AUTOMATION
├─ Power BI Desktop            ├─ Python (Orchestration)
├─ Power BI Service            ├─ SQL Server (Warehouse)
├─ DAX                         ├─ Flask (Portal)
├─ Power Query                 └─ Azure SQL (Data)
├─ Incremental Refresh
└─ Enhanced Refresh API        CLOUD & INFRASTRUCTURE
                               ├─ Microsoft Azure
SECURITY & AUTHENTICATION      ├─ Azure Container Apps
├─ Azure AD (SSO)              ├─ Azure Front Door
├─ Row-Level Security (RLS)    └─ Azure Backup
├─ Role-Based Access (RBAC)
└─ Audit Logging               DEVELOPMENT
                               ├─ Claude AI (Portal Dev)
                               └─ Git (Version Control)
```

---

## 📚 Documentation

- 📄 [Semantic Architecture](semantic-architecture.md) — Data model design and implementation
- 📄 [Refresh Strategy](refresh-strategy.md) — Two-tier refresh approach and optimization  
- 📄 [Portal Architecture](portal-architecture.md) — Portal design and access control implementation

---

## 📧 Contact

**saineeraj.kumar@samunnati.com**

---

<div align="center">

**Status:** ✅ Production | **Version:** 2.0 | **Last Updated:** May 2026

</div>