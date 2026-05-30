# ADR-003: Why Karpenter Over Cluster Autoscaler

## Status
Accepted

## Context
Nimbus needs a node autoscaling solution for EKS to handle variable traffic without over-provisioning.

## Decision
Use Karpenter.

## Reasons
- **Speed** — Karpenter provisions nodes in ~30 seconds vs ~3 minutes for Cluster Autoscaler.
- **Flexibility** — Karpenter selects instance types dynamically based on pod requirements. Cluster Autoscaler is tied to pre-defined node groups.
- **Cost** — Karpenter's consolidation policy bins pods tightly and terminates underutilized nodes automatically, reducing waste.
- **Spot handling** — Karpenter handles Spot interruptions and fallback to on-demand natively.

## Tradeoffs
Karpenter requires IRSA and an OIDC provider — more IAM setup upfront. It also only works on EKS (AWS-specific), whereas Cluster Autoscaler works across clouds. We accept this for the performance and cost benefits on AWS.
