# ADR-002: Why ArgoCD Over Flux

## Status
Accepted

## Context
Nimbus needs a GitOps controller to sync Kubernetes state from the Git repository.

## Decision
Use ArgoCD.

## Reasons
- **UI** — ArgoCD has a built-in web UI showing sync status, resource health, and diff. Flux is CLI-only.
- **Multi-app management** — ArgoCD's Application CRD makes it easy to manage multiple services independently.
- **Visibility** — The sync status, health, and history are all visible without kubectl access.
- **Adoption** — ArgoCD has broader adoption and more community resources.

## Tradeoffs
Flux is lighter and more Kubernetes-native (uses standard controllers). ArgoCD runs its own application controller and repo server which consumes more cluster resources — noticeable on a KinD cluster. Flux also handles image update automation better out of the box. We accept the resource overhead for the operational visibility ArgoCD provides.
