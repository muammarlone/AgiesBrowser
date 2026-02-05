# GADOS V2 Architectural Patterns (Gold Standard)

> **Authority**: KIW & Genius
> **Status**: INJECTED

## 1. Feature Gate (Security Middleare)
*   **Purpose**: Enforce License-based Access Control via "Wavefunction Collapse".
*   **Location**: `src/middleware/feature_gate.py`
*   **Usage**: All API endpoints impacting "Business Value" must be wrapped in `FeatureGate.check_license()`.

## 2. Graph Audit (Governance Service)
*   **Purpose**: Track every "Deliverable Mutation" as a connected graph node.
*   **Location**: `src/services/audit_logger.py`
*   **Usage**: Create, Update, and Delete operations MUST emit an Audit Event.

## 3. Compliance
This repository is now compliant with GADOS V2 "Structure Upgrade".
