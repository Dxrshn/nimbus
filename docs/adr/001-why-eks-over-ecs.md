# ADR-001: Why EKS Over ECS

## Status
Accepted

## Context
Nimbus requires a container orchestration platform. The two main AWS-native options are ECS (Elastic Container Service) and EKS (Elastic Kubernetes Service).

## Decision
Use EKS.

## Reasons
- **Portability** — Kubernetes manifests work on any cloud or locally (KinD). ECS configs are AWS-only.
- **Ecosystem** — Helm, ArgoCD, Kyverno, Karpenter, Prometheus Operator all target Kubernetes natively.
- **Industry standard** — Kubernetes is the de facto standard. ECS knowledge doesn't transfer.
- **Local parity** — KinD lets us run the exact same manifests locally at $0. ECS has no local equivalent.

## Tradeoffs
EKS is operationally heavier than ECS. The control plane is managed by AWS but node management, networking (VPC CNI), and add-ons require more configuration. For a small team this overhead is real — ECS would ship faster. We accept this tradeoff for portability and ecosystem depth.
