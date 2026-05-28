"""
Power BI Embed Token & Embed URL Generation

This module generates secure embed tokens for Power BI reports with
Row-Level Security (RLS) context applied. Used in the Insights 2.0
Analytics Portal to embed reports with department-level and user-level
data access control.

Author: Sai Neeraj Kumar
Project: Insights 2.0 - Enterprise Analytics Platform
"""

import msal
import requests
import json

# ==========================================
# CONFIGURATION
# ==========================================

TENANT_ID     = "YOUR_TENANT_ID"          # Azure AD Tenant
CLIENT_ID     = "YOUR_CLIENT_ID"          # Service Principal ID
CLIENT_SECRET = "YOUR_CLIENT_SECRET"      # Service Principal Secret

WORKSPACE_ID  = "YOUR_WORKSPACE_ID"       # Power BI Workspace
REPORT_ID     = "YOUR_REPORT_ID"          # Report to embed

CORE_DATASET  = "YOUR_CORE_DATASET_ID"    # Shared semantic model
PROXY_DATASET = ""                        # Optional proxy dataset

RLS_USERNAME  = "user@example.com"        # User identity for RLS
RLS_ROLES     = ["RoleName"]              # RLS roles (department, access level)

# ==========================================
# STEP 1: AUTHENTICATE TO POWER BI
# ==========================================

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE     = ["https://analysis.windows.net/powerbi/api/.default"]

# Create confidential client for service principal authentication
app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

# Acquire access token for Power BI API
token_result = app.acquire_token_for_client(scopes=SCOPE)

if "access_token" not in token_result:
    raise Exception(f"Failed to authenticate with Power BI:\n{token_result}")

access_token = token_result["access_token"]

# Set up request headers with authentication
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# ==========================================
# STEP 2: FETCH REPORT DETAILS
# ==========================================

# Get report metadata (name, embed URL)
report_url = (
    f"https://api.powerbi.com/v1.0/myorg/groups/"
    f"{WORKSPACE_ID}/reports/{REPORT_ID}"
)

report_response = requests.get(report_url, headers=headers)

if report_response.status_code != 200:
    raise Exception(
        f"Failed to fetch report details:\n{report_response.text}"
    )

report_data = report_response.json()

embed_url = report_data["embedUrl"]      # URL to embed in iframe
report_name = report_data["name"]        # Report display name

# ==========================================
# STEP 3: BUILD DATASET LIST WITH PERMISSIONS
# ==========================================

# Core dataset always included (shared semantic model)
datasets = [
    {
        "id": CORE_DATASET,
        "xmlaPermissions": "ReadOnly"    # Read-only access
    }
]

# Add optional proxy dataset if configured
if PROXY_DATASET and PROXY_DATASET.strip():
    datasets.append({
        "id": PROXY_DATASET,
        "xmlaPermissions": "ReadOnly"
    })

# ==========================================
# STEP 4: GENERATE EMBED TOKEN WITH RLS
# ==========================================

# Build token request payload
payload = {
    # Datasets the token has access to
    "datasets": datasets,

    # Reports to embed
    "reports": [
        {
            "id": REPORT_ID
        }
    ],

    # Target workspace
    "targetWorkspaces": [
        {
            "id": WORKSPACE_ID
        }
    ],

    # Access level (View = read-only)
    "accessLevel": "View",

    # RLS CONTEXT: Define user identity and roles
    # Power BI applies RLS rules based on username and roles
    "identities": [
        {
            "username": RLS_USERNAME,           # User email/ID
            "roles": RLS_ROLES,                 # RLS roles from semantic model
            "datasets": [CORE_DATASET]          # Datasets RLS applies to
        }
    ]
}

# Call Power BI API to generate token
token_url = "https://api.powerbi.com/v1.0/myorg/GenerateToken"

token_response = requests.post(
    token_url,
    headers=headers,
    json=payload
)

if token_response.status_code != 200:
    raise Exception(
        f"Failed to generate embed token:\n{token_response.text}"
    )

token_data = token_response.json()

embed_token = token_data["token"]         # Secure token for embedding
token_expiry = token_data.get("expiration")  # Token expiration time

# ==========================================
# STEP 5: RETURN EMBED DETAILS
# ==========================================

# These values are sent to portal frontend for embedding

embed_details = {
    "reportName": report_name,
    "embedUrl": embed_url,
    "embedToken": embed_token,
    "tokenExpiry": token_expiry,
    "workspace_id": WORKSPACE_ID,
    "report_id": REPORT_ID
}

print("\n" + "="*50)
print("POWER BI EMBED TOKEN GENERATED")
print("="*50 + "\n")

print(f"Report Name     : {embed_details['reportName']}")
print(f"Embed URL       : {embed_details['embedUrl']}")
print(f"Token (preview) : {embed_token[:50]}...")
print(f"Token Expiry    : {embed_details['tokenExpiry']}")
print(f"RLS Applied     : {RLS_USERNAME}")
print(f"RLS Roles       : {', '.join(RLS_ROLES)}")

print("\n" + "="*50 + "\n")

# ==========================================
# HOW THIS WORKS IN THE PORTAL:
# ==========================================

"""
1. User logs into Insights 2.0 Analytics Portal (Azure AD SSO)

2. Portal determines user's:
   - Department (Sales, Finance, Operations, etc.)
   - Role (Executive, Manager, Analyst, User)
   - Access Level (0-4)

3. Portal calls this script with:
   RLS_USERNAME = "user@company.com"
   RLS_ROLES = ["Sales", "Manager"]

4. This script:
   - Authenticates as service principal
   - Fetches report metadata
   - Generates embed token with RLS context
   - Returns embed_url + embed_token

5. Portal embeds report in iframe:
   <iframe src="{embed_url}">
   powerbi.embed(container, {
     embedUrl: embed_url,
     accessToken: embed_token,
     reportId: report_id
   })

6. Power BI applies RLS rules automatically:
   - RLS rule: [Department] = "Sales"
   - User can only see Sales data
   - Finance/HR data hidden
   - User-level and department-level filtering applied

7. Result: User sees filtered report with RLS applied ✓
"""

# ==========================================
# SECURITY NOTES:
# ==========================================

"""
- Service Principal credentials stored securely (Azure Key Vault)
- Token has limited lifetime (expires automatically)
- RLS context passed for each user
- Tokens are single-use and time-limited
- Access level is read-only (View)
- Audit logging tracks who accessed what report
"""

# Return for portal to use
print("\n[Portal would use these values to embed the report]\n")
print(json.dumps(embed_details, indent=2))