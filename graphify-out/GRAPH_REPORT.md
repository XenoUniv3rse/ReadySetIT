# Graph Report - .  (2026-08-02)

## Corpus Check
- Corpus is ~1,413 words - fits in a single context window. You may not need a graph.

## Summary
- 20 nodes · 29 edges · 4 communities
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Strategy & Operations
- Azure Infrastructure
- Data & Migration
- Microsoft Identity & Email

## God Nodes (most connected - your core abstractions)
1. `Cloud Infrastructure Setup & Management` - 7 edges
2. `Ready Set IT` - 5 edges
3. `Identity & Access (Entra ID)` - 4 edges
4. `Email & Collaboration (Exchange Online)` - 4 edges
5. `Cloud Migration` - 4 edges
6. `Strategic Advisory` - 4 edges
7. `Microsoft Cloud Ecosystem` - 4 edges
8. `Entra ID & Exchange Migration` - 3 edges
9. `Azure` - 3 edges
10. `Network & VPN` - 2 edges

## Surprising Connections (you probably didn't know these)
- `Security Audits` --conceptually_related_to--> `Identity & Access (Entra ID)`  [INFERRED]
  index.html → index.html  _Bridges community 3 → community 0_
- `Email Data Transition (POP/IMAP)` --semantically_similar_to--> `Email & Collaboration (Exchange Online)`  [INFERRED] [semantically similar]
  index.html → index.html  _Bridges community 3 → community 2_
- `Ready Set IT` --references--> `Cloud Infrastructure Setup & Management`  [EXTRACTED]
  index.html → index.html  _Bridges community 0 → community 1_
- `Ready Set IT` --references--> `Cloud Migration`  [EXTRACTED]
  index.html → index.html  _Bridges community 0 → community 2_
- `Cloud Infrastructure Setup & Management` --references--> `Data Protection (3-2-1 Backup)`  [EXTRACTED]
  index.html → index.html  _Bridges community 1 → community 2_

## Hyperedges (group relationships)
- **Microsoft Cloud Service Bundle** — index_identity_access, index_email_collaboration, index_endpoint_management, index_entra_exchange_migration [INFERRED 0.85]

## Communities (4 total, 0 thin omitted)

### Community 0 - "Strategy & Operations"
Cohesion: 0.33
Nodes (7): Documentation & Training, Endpoint Management (Intune), 4-Step Process (Consultation-Scoping-Deployment-Handover), Ready Set IT, Security Audits, SME Target Market, Strategic Advisory

### Community 1 - "Azure Infrastructure"
Cohesion: 0.50
Nodes (5): Azure, Cloud Infrastructure Setup & Management, Domain & DNS, Network & VPN, Website Hosting (Azure)

### Community 2 - "Data & Migration"
Cohesion: 0.50
Nodes (4): Cloud Migration, Data Migration Planning, Data Protection (3-2-1 Backup), Email Data Transition (POP/IMAP)

### Community 3 - "Microsoft Identity & Email"
Cohesion: 0.67
Nodes (4): Email & Collaboration (Exchange Online), Entra ID & Exchange Migration, Identity & Access (Entra ID), Microsoft Cloud Ecosystem

## Knowledge Gaps
- **1 isolated node(s):** `Domain & DNS`
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Cloud Infrastructure Setup & Management` connect `Azure Infrastructure` to `Strategy & Operations`, `Data & Migration`, `Microsoft Identity & Email`?**
  _High betweenness centrality (0.425) - this node is a cross-community bridge._
- **Why does `Ready Set IT` connect `Strategy & Operations` to `Azure Infrastructure`, `Data & Migration`?**
  _High betweenness centrality (0.345) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Identity & Access (Entra ID)` (e.g. with `Entra ID & Exchange Migration` and `Security Audits`) actually correct?**
  _`Identity & Access (Entra ID)` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Email & Collaboration (Exchange Online)` (e.g. with `Email Data Transition (POP/IMAP)` and `Entra ID & Exchange Migration`) actually correct?**
  _`Email & Collaboration (Exchange Online)` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Domain & DNS` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._