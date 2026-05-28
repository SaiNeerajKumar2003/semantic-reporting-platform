# Portal Architecture

## Overview

Designed and implemented a centralized embedded analytics portal providing 1000+ user capacity with department-level and user-level access control. The portal integrates Power BI reports with automated RLS application and centralized permission management.

## Portal Requirements

**User Management**
- Single sign-on via Azure AD
- Automatic user attribute provisioning
- Department and role association
- Access level management

**Report Access Control**
- Department-level report filtering
- User-level report visibility
- Role-based access restrictions
- Automated permission enforcement

**Report Distribution**
- Centralized report catalog
- Report discovery by department and role
- Embedded Power BI reports
- Secure embed token generation

## Architecture

### Authentication Layer
- Azure AD integration for single sign-on
- User context retrieval from directory
- Session management and auto-logout
- Compliance-ready authentication

### Authorization Layer
- Department-based access rules
- Role-based permission matrix
- User-level access assignment
- Dynamic permission checking

### Report Access Layer
- Report catalog management
- Department and user filtering
- Access verification before rendering
- Audit logging of report access

### Embedding Layer
- Power BI Service API integration
- Embed URL retrieval
- Embed token generation with RLS context
- Secure report rendering

## Access Control Implementation

### Department-Level Filtering
- Automatic department assignment from Azure AD
- Report visibility filtered by department
- User sees only relevant departmental reports
- Managers see department + roll-up data

### User-Level Filtering
- Individual user permission assignment
- User-specific report availability
- Role-based access levels (Analyst, Manager, Executive)
- Access denied for unauthorized reports

### RLS Context
- Department identifier passed to Power BI
- User ID included in embed context
- Role information for context-aware calculations
- Automatic filtering at report level

## Technical Implementation

### Backend
- Flask application framework
- Azure AD OAuth integration
- Database for user permissions and report metadata
- API endpoints for report discovery and access

### Frontend
- Report list view with filtering
- Report selection interface
- Embedded Power BI viewer
- User profile and preferences

### Database
- User and department mapping
- Report and permission relationships
- Access audit trails
- Refresh and monitoring metadata

### Security
- HTTPS/TLS encryption
- Secure token exchange
- Session management
- Audit logging and compliance tracking

## User Journey

1. User accesses portal
2. Azure AD authentication
3. User context retrieved (department, role, access level)
4. Portal queries available reports filtered by user context
5. User selects report
6. Portal verifies access permission
7. Embed token generated with RLS context
8. Power BI report embedded with secure token
9. Report applies RLS filtering automatically
10. User sees filtered data for their context

## Scalability

**Capacity**
- 1000+ concurrent users supported
- Multiple container instances with load balancing
- Database connection pooling
- Efficient caching of report metadata

**Performance**
- Sub-second report discovery
- Fast embed token generation
- Quick report rendering
- Minimal latency in permission checking

## Deployment

- Azure Container Apps for application hosting
- Azure SQL Database for persistent storage
- Azure Front Door for CDN and DDoS protection
- Azure Backup for data protection

## Development Approach

Portal designed and architected through requirements analysis:
- Identified necessary features and access control logic
- Designed system flows and data structures
- Specified API contracts and embedding strategy
- Validated enterprise security requirements

Implementation built using Claude AI:
- Prompt engineering for architecture translation
- Code generation for backend and frontend
- Integration implementation (Azure AD, Power BI)
- Testing and validation of enterprise requirements

## Access Control Matrix

| Role | Reports | Data | Access Level |
|------|---------|------|--------------|
| Analyst | Department | Own assignments | Limited |
| Manager | Department + Team | Department + Team | Manager |
| Executive | All | All company data | Executive |
| Admin | All + System | All + Settings | Administrator |

## Audit and Compliance

- Complete access logging
- Report access tracking with timestamps
- User activity monitoring
- Compliance-ready audit trails
- Data protection and encryption

## Results

- Centralized report access for 1000+ users
- Automated department-level data segregation
- User-level permission enforcement
- Reduced administrative overhead
- Enterprise-grade security and compliance
