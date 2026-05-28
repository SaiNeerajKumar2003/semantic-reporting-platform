# Code Samples - What You'll Add

## 📁 Repository Will Have This Structure:

```
/code-samples/
├─ 1-embed-token-generation.py
├─ 2-table-by-table-refresh-api.py
├─ 3-dax-time-intelligence-offset.dax
├─ 4-incremental-refresh-config.md
└─ README.md
```

---

## 1️⃣ **embed-token-generation.py**

### What it shows:
- How you authenticate to Power BI Service
- How you generate embed tokens
- How you pass RLS context (Department, UserID, Role)
- How you get Embed URL
- How you secure the token for portal

### Size: ~100-150 lines
### Impact: **PROVES you built the portal** ✅

### Example structure:
```python
# Authentication
# Generate embed token with RLS context
# Pass Department/UserID/Role
# Return embed_url + embed_token
```

---

## 2️⃣ **table-by-table-refresh-api.py**

### What it shows:
- How you call Power BI Enhanced Refresh API
- How you refresh tables one-by-one
- How you detect which tables changed
- How you monitor refresh progress
- How you handle errors per table

### Size: ~150-200 lines
### Impact: **PROVES you optimized refresh to 92%** ✅

### Example structure:
```python
# Authenticate to Power BI
# Get list of tables to refresh
# Loop: For each table
#   Call Enhanced Refresh API
#   Monitor progress
#   Track duration
#   Handle failures
# Return results
```

---

## 3️⃣ **dax-time-intelligence-offset.dax**

### What it shows:
- Your custom DAX approach (NOT built-in functions)
- How you use Date calendar with offsets
- Time intelligence calculations (YoY, MoM, etc.)
- How offset method works
- Why you chose this instead of DATEADD/DATEADD

### Size: ~50-100 lines
### Impact: **PROVES advanced DAX knowledge** ✅

### Example structure:
```dax
// Date Calendar with Offset approach
// [YoY Growth] = Using offset method
// [MoM Comparison] = Using offset method
// [QoQ Analysis] = Using offset method
```

---

## 4️⃣ **incremental-refresh-config.md**

### What it shows:
- How you configured Power BI Incremental Refresh Policy
- Partition strategy (dates, ranges)
- Historical vs Incremental settings
- How Power BI handles partitioning automatically
- Results: 4 hours → 20 minutes
- Sample configuration with dummy values

### Size: ~50-100 lines
### Impact: **PROVES optimization strategy** ✅

### Example structure:
```
POWER BI INCREMENTAL REFRESH CONFIGURATION:

Historical Partition:
├─ Start: 2024-01-01
├─ End: 2 years back
└─ Refresh: NO

Incremental Partition:
├─ Start: Today - 30 days
├─ End: Today
└─ Refresh: DAILY

Results:
├─ Before: 4 hours 15 minutes
├─ After: 20 minutes
└─ Improvement: 92% faster
```

---

## 📄 **README.md in /code-samples/**

Explains:
- What each file does
- Why you wrote it
- How it connects to your project
- How to understand the code

---

## 🎯 **TOTAL ARTIFACTS:**

| File | Lines | What It Proves |
|------|-------|----------------|
| embed-token-generation.py | 100-150 | Portal development |
| table-by-table-refresh-api.py | 150-200 | 92% refresh improvement |
| dax-time-intelligence-offset.dax | 50-100 | Advanced DAX knowledge |
| incremental-refresh-config.md | 50-100 | Optimization strategy |
| **TOTAL** | **350-550** | **Complete technical depth** |

---

## 📊 **EXPECTED SCORE:**

```
With these 4 artifacts:
✅ Real code (not generic)
✅ Proven implementation
✅ Advanced technical knowledge
✅ Complete proof of work

SCORE: 85-90/100 ✓✓✓
```

---

## 🚀 **NEXT STEPS:**

1. **Get your actual code files ready:**
   - embed-token-generation.py (your actual code)
   - table-by-table-refresh-api.py (your actual code)
   - dax-time-intelligence-offset.dax (your actual code)
   - incremental-refresh-config.md (your actual config)

2. **Anonymize sensitive data:**
   - Real server names → dummy names
   - Real API keys → SAMPLE_KEY
   - Real user IDs → sample_user_123
   - Real credentials → dummy_credentials

3. **Add professional comments:**
   - Explain what each section does
   - Why you chose this approach
   - How it connects to 92% improvement

4. **I'll integrate into repository:**
   - Create /code-samples/ folder
   - Add all files
   - Create README explaining each
   - Update main README to showcase these

---

## ✨ **This Will Make Your Repository:**

✅ **NOT generic** - Real code, not templates  
✅ **Credible** - Actual implementation  
✅ **Impressive** - Advanced techniques  
✅ **Provable** - Shows what you did  
✅ **Portfolio-ready** - 85+/100 score  

---

**Ready to provide these 4 files?** 

Once you give me:
1. embed-token-generation.py
2. table-by-table-refresh-api.py
3. dax-time-intelligence-offset.dax
4. incremental-refresh-config.md

I'll create the professional repository structure that will get you 85-90/100 🎯
