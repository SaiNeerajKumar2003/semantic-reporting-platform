# Power BI Embed Token Generation: Portal Security Implementation

**Insights 2.0 — Enterprise Analytics Platform Modernization**

Author: Sai Neeraj Kumar | Project: Insights 2.0 | Focus: Portal RLS Security

---

## Executive Summary

The Insights 2.0 Analytics Portal uses Power BI embed tokens to securely display reports with Row-Level Security (RLS). This implementation:

- Generates secure, time-limited tokens for Power BI embedding
- Applies department and user-level RLS context
- Manages 1000+ concurrent users with per-user filtering
- Integrates with Azure AD for user authentication
- Maintains complete audit trail for compliance

**Key Achievement:** Built enterprise-grade analytics portal serving 1000+ users with automatic RLS-based access control.

---

## Problem Statement

### Portal Security Requirements

| Requirement | Challenge | Solution |
|-------------|-----------|----------|
| **User Authentication** | Authenticate users to Power BI API | Service principal with MSAL |
| **RLS Application** | Filter data per user/department | Pass RLS context in embed token |
| **Report Embedding** | Embed Power BI in portal | Generate embed tokens via API |
| **Token Security** | Prevent token reuse/expiry | Time-limited tokens (60 min) |
| **Scalability** | 1000+ concurrent users | Efficient token generation |
| **Audit Trail** | Track who accessed what | Centralized audit logging |

### Before: Manual Access Control

| Aspect | Limitation |
|--------|-----------|
| **Access Management** | Manual per-user configuration |
| **RLS Application** | User manually applies filters |
| **Scalability** | Limited to ~50-100 users |
| **Consistency** | Different users see different data even in same department |
| **Maintenance** | High overhead as users change departments |
| **Security** | Manual approach prone to errors |

### After: Automated Embed Token RLS

| Aspect | Improvement |
|--------|------------|
| **Access Management** | Automatic based on Azure AD |
| **RLS Application** | Applied automatically via token |
| **Scalability** | 1000+ concurrent users |
| **Consistency** | All users in department see same data |
| **Maintenance** | Automatic with Azure AD sync |
| **Security** | No manual steps; audit trail complete |

---

## Technical Architecture

### Portal Authentication Flow

```
USER JOURNEY:
───────────────────────────────────────────────────────────────

1. User Logs Into Portal
   ├─ Portal redirects to Azure AD login
   ├─ User enters credentials (company SSO)
   └─ Azure AD returns identity token

2. Portal Determines User Context
   ├─ Look up user in Active Directory
   ├─ Get user's department (Sales, Finance, HR, etc.)
   ├─ Get user's role (Executive, Manager, Analyst, etc.)
   └─ Determine access level (0-4)

3. Portal Requests Embed Token
   ├─ Call token generation endpoint
   ├─ Pass: user_email, department, role, access_level
   └─ Token generation authenticates as service principal

4. Service Principal Authenticates to Power BI
   ├─ Uses MSAL library
   ├─ Authenticates using service principal credentials
   ├─ Receives Power BI API access token
   └─ Token valid for 60 minutes

5. Service Principal Calls Power BI GenerateToken API
   ├─ Requests embed token for specific report
   ├─ Passes RLS context (username, roles, datasets)
   └─ Receives secure embed token

6. Portal Embeds Report in Frontend
   ├─ JavaScript receives embed_url and embed_token
   ├─ Creates iframe with report URL
   ├─ Calls powerbi.embed() with token
   └─ Report loads in portal

7. Power BI Applies RLS Automatically
   ├─ RLS rule: [Department] = "Sales"
   ├─ User can only see Sales data
   ├─ Finance/HR data hidden automatically
   └─ User-level filtering applied

8. Report Displays with User's Data
   ├─ Sales user sees: Sales KPIs, Sales revenue, Sales metrics
   ├─ Finance user sees: Finance KPIs, Budget variance, Cost analysis
   └─ Each user sees only authorized data
```

---

## Implementation Components

### Service Principal Credentials

| Component | Purpose | Security |
|-----------|---------|----------|
| **Tenant ID** | Azure AD organization identifier | Publicly known |
| **Client ID** | Service principal application ID | Publicly known |
| **Client Secret** | Service principal credential | SENSITIVE — store in Azure Key Vault |

**Security Best Practice:** Never hardcode credentials. Store in:
- Azure Key Vault (recommended)
- Environment variables
- Secure configuration management

### Authentication Libraries

**MSAL (Microsoft Authentication Library)**

| Purpose | Function |
|---------|----------|
| **Token Acquisition** | Acquire access token using service principal |
| **Token Caching** | Cache tokens to reduce API calls |
| **Token Refresh** | Auto-refresh expired tokens |
| **Error Handling** | Consistent error handling |

**Implementation Pattern:**

```
Create MSAL ConfidentialClientApplication
├─ ClientID: Service principal app ID
├─ Authority: Azure AD tenant URL
└─ ClientSecret: Service principal password

Acquire token:
├─ Try cached token first (if not expired)
├─ If expired, request new token
└─ Return access token for Power BI API
```

---

## Embed Token Request Structure

### Report Metadata Retrieval

**Step 1: Fetch Report Details**

| API Endpoint | Purpose |
|-------------|---------|
| `GET /groups/{WORKSPACE_ID}/reports/{REPORT_ID}` | Get report name and embed URL |

**Response Includes:**
- Report name (display name)
- Embed URL (iframe URL)
- Dataset associations
- Created/Modified dates

### Dataset Permission Configuration

**Step 2: Define Dataset Access**

| Dataset | Permission | Rationale |
|---------|-----------|-----------|
| **Core Dataset** | ReadOnly | Users see reports; cannot modify |
| **Proxy Dataset** | ReadOnly (optional) | Alternative data source if needed |

**Access Level Options:**

| Level | Capability | Use Case |
|-------|-----------|----------|
| **View** | Read reports | Standard user |
| **Edit** | Edit reports | Report developer |
| **Create** | Create reports | Power BI developer |

---

## RLS Context Implementation

### RLS Identity Structure

**Identity Component**

| Field | Purpose | Example |
|-------|---------|---------|
| **username** | User identifier | user@company.com |
| **roles** | RLS roles | ["Sales", "Manager"] |
| **datasets** | Associated datasets | [core_dataset_id] |

**How RLS Works:**

```
RLS Rules in Semantic Model:
───────────────────────────────────────

Rule 1: Department Filter
├─ If [Department] in roles
└─ User sees only matching department data

Rule 2: Access Level Filter
├─ If AccessLevel >= [UserAccessLevel]
└─ User sees data for their access level

Rule 3: Manager Visibility
├─ If Manager = TRUE and role = "Manager"
└─ User sees team data in addition to own
```

### Multi-Role Support

Users can have multiple RLS roles:

**Example: Manager User**

```
User: John@company.com
Roles: ["Sales", "Manager", "Executive"]

Results:
├─ "Sales" role → sees Sales department data
├─ "Manager" role → sees team's detailed data
└─ "Executive" role → sees executive summary
```

**RLS Rules Apply:**
- All matching roles evaluated
- User sees union of all role-filtered data
- Most permissive role wins

---

## Token Generation Process

### Complete Token Generation Workflow

| Step | Action | Output |
|------|--------|--------|
| 1 | Authenticate as service principal | Access token |
| 2 | Fetch report metadata | Embed URL, report name |
| 3 | Build dataset list | Datasets with permissions |
| 4 | Build RLS context | User identity and roles |
| 5 | Create token request | Complete payload |
| 6 | Call Power BI API | Embed token |
| 7 | Return to portal | Embed token and URL |

### API Request Payload

**Payload Structure**

| Section | Elements | Purpose |
|---------|----------|---------|
| **datasets** | List of dataset IDs with permissions | Define what data user can access |
| **reports** | List of report IDs | Define what reports to embed |
| **targetWorkspaces** | Workspace ID | Target workspace for embedding |
| **accessLevel** | View/Edit/Create | Define user capability |
| **identities** | Username, roles, datasets | RLS context |

**Identities Section (Key for RLS)**

| Field | Value | Purpose |
|-------|-------|---------|
| **username** | user@company.com | User identifier for RLS |
| **roles** | ["Sales", "Manager"] | RLS roles to apply |
| **datasets** | [dataset_id] | Datasets RLS applies to |

---

## Token Security

### Token Characteristics

| Property | Value | Purpose |
|----------|-------|---------|
| **Format** | JWT (JSON Web Token) | Standard security token |
| **Lifetime** | 60 minutes | Time-limited for security |
| **Scope** | Specific report + RLS context | Token can't be reused for different user |
| **Usage** | Single-use per session | Fresh token per browser session |

### Token Validation

**Power BI validates each token:**

```
Validation Steps:
├─ 1. Verify signature (issued by Power BI)
├─ 2. Check expiration (not older than 60 min)
├─ 3. Validate username format
├─ 4. Verify RLS roles exist in model
├─ 5. Confirm datasets are accessible
└─ 6. Apply RLS rules using identity
```

### Refresh Token Strategy

**Token Lifecycle**

| Time | Action | Status |
|------|--------|--------|
| 0 min | Token generated | Active |
| 55 min | Portal detects expiry approaching | Refresh needed |
| 58 min | Portal requests new token | Token refreshed |
| 60 min | Old token expires | Not used (already refreshed) |

**User Experience:** Seamless — user never sees token expiry

---

## Portal Integration

### Frontend Embedding

**JavaScript Implementation Pattern**

```
1. Receive embed_url and embed_token from backend
2. Select target container element
3. Call powerbi.embed() with:
   ├─ embedUrl: Report URL
   ├─ accessToken: Embed token
   ├─ reportId: Report ID
   ├─ type: "report"
   └─ tokenExpiry: Token expiration time
4. Power BI loads report in iframe
5. RLS rules apply automatically
6. Report displays user's filtered data
```

**User See Different Data Based on Role:**

```
Sales User:
├─ Department filter: Sales ✓
├─ Revenue: $2.3M ✓
├─ Orders: 450 ✓
└─ Finance data: HIDDEN ✗

Finance User:
├─ Department filter: Finance ✓
├─ Budget: $5M ✓
├─ Variance: 3% ✓
└─ Sales data: HIDDEN ✗
```

---

## Operational Procedures

### Portal Operations Checklist

**Daily Verification**

- [ ] Portal accessible to users
- [ ] Token generation working (no errors)
- [ ] Report embeds successfully
- [ ] RLS filtering applied correctly
- [ ] No failed token requests in logs

**Monthly Review**

- [ ] Token generation success rate > 99%
- [ ] Average response time < 2 seconds
- [ ] No security violations
- [ ] User access audit trail complete
- [ ] No expired token issues

### Troubleshooting

| Issue | Diagnostic | Resolution |
|-------|-----------|-----------|
| **Report doesn't load** | Check browser console | Verify token not expired; check network logs |
| **Wrong data showing** | Verify RLS roles in token | Check roles match semantic model RLS rules |
| **Token generation fails** | Check API response code | Verify service principal permissions |
| **User can't log in** | Check Azure AD integration | Verify user in Active Directory |
| **Slow token generation** | Check API latency | Power BI API latency — temporary |

---

## Scaling Considerations

### Performance at Scale

| Metric | Typical Value | At 1000 Users |
|--------|---------------|--------------|
| **Token generation per user** | 0.5-2 seconds | 500-2000 seconds total (parallel) |
| **Concurrent embeddings** | 100+ | Platform tested to 1000+ |
| **Memory per token** | ~1 KB | ~1 MB for 1000 tokens |
| **Token cache** | 100-500 tokens | Prevents regeneration |

### Optimization Strategies

| Strategy | Benefit |
|----------|---------|
| **Token caching** | Reuse token for same user in same session |
| **Batch token generation** | Generate multiple tokens in parallel |
| **Async token generation** | Don't block page load on token request |
| **CDN for static assets** | Faster report load times |

---

## Compliance & Audit

### Audit Trail

**What's Logged**

| Event | Information | Storage |
|-------|-----------|---------|
| **Token generation** | User, timestamp, report, RLS roles | Application log |
| **Report access** | User, timestamp, duration, data accessed | Power BI audit log |
| **Failed attempts** | User, timestamp, error reason | Security log |
| **Permission changes** | Who changed, when, old vs new roles | Azure AD audit log |

**Retention:** 90 days minimum (enterprise standard)

### Data Protection

| Control | Implementation |
|---------|---|
| **In Transit** | TLS 1.2+ encryption |
| **At Rest** | Credentials stored in Key Vault |
| **Access Control** | Service principal has minimal permissions |
| **Audit Trail** | Complete logging of token generation |

---

## Related Components

### Integration Points

| Component | Integration | Purpose |
|-----------|-----------|---------|
| **Incremental Refresh Policy** | Provides partitioned data | Data available for embedding |
| **Enhanced Refresh API** | Ensures fresh data | Keeps embedded reports current |
| **RLS Rules** | Enforced via token identity | Filters data per user |
| **DAX Offset Method** | Measures use offset logic | Consistent calculations |

### Complete Portal Architecture

```
User logs in
    ↓
Azure AD authenticates user
    ↓
Portal determines department/role
    ↓
Portal calls token generation
    ↓
Service principal calls Power BI API
    ↓
Power BI generates embed token with RLS
    ↓
Portal receives token + embed URL
    ↓
Frontend embeds report
    ↓
Power BI applies RLS rules
    ↓
User sees filtered data
```

---

## Key Learnings

### What Embed Token RLS Enables

| Capability | Benefit |
|-----------|---------|
| **Automatic Filtering** | No manual user configuration needed |
| **Scalability** | 1000+ users with consistent security |
| **Compliance** | Complete audit trail |
| **Flexibility** | Multi-role support |
| **Performance** | Token generation < 2 seconds |
| **Maintenance** | Sync with Azure AD automatic |

### Security Best Practices

| Practice | Implementation |
|----------|---|
| **Never hardcode credentials** | Store in Azure Key Vault |
| **Token time limit** | 60-minute expiry |
| **RLS context validation** | Verify roles exist in model |
| **Audit logging** | Log all token generation |
| **Service principal isolation** | Minimal required permissions |
| **Network security** | TLS 1.2+ for all communication |

---

## Conclusion

The embed token generation approach provides a secure, scalable foundation for the Insights 2.0 Analytics Portal. By:

- Authenticating users via Azure AD
- Generating secure, time-limited tokens
- Passing RLS context (department, role, access level)
- Applying filtering automatically in Power BI
- Maintaining complete audit trail

This implementation enables:
- 1000+ concurrent users with per-user security
- Automatic access control (no manual configuration)
- Complete compliance audit trail
- Sub-2-second token generation
- Non-blocking report embedding

Combined with Incremental Refresh and Enhanced Refresh API, this creates an enterprise-grade analytics platform with security, scalability, and performance.

**Implementation Status:** Production, serving 1000+ users, 99.9% uptime

---

**Last Updated:** May 28, 2025 | **Status:** Active Production