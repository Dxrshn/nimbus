# ADR-004: Local-First Development Strategy (KinD over real EKS)

**Date:** 2026-05-29
**Status:** Accepted

## Context

Building a production-grade Kubernetes platform requires a running cluster, databases, and AWS services. Provisioning real AWS infrastructure (EKS, RDS, ElastiCache, SQS) costs ~$165/month for a dev environment and requires active AWS account management. The goal is a portfolio-quality project, not a live production system.

The question: how do we run the full platform stack at zero cost while keeping the code, configs, and architecture identical to what a real AWS deployment would use?

## Decision

Run the platform locally on a KinD (Kubernetes IN Docker) multi-node cluster. Emulate AWS services with LocalStack. Run PostgreSQL and Redis as in-cluster Kubernetes Deployments. Write all Terraform modules for production AWS infrastructure, but only run `terraform validate`, `terraform plan`, and security scans — never `terraform apply`.

The only real AWS resources provisioned are an S3 bucket and DynamoDB table for Terraform state, both within the AWS free tier.

## Consequences

**Positive:**
- Zero monthly cost for the duration of development
- Full Kubernetes cluster running locally — Helm, ArgoCD, Prometheus, Kyverno all work identically to production
- Terraform modules are complete, validated, and security-scanned — the code is production-ready even if not applied
- `terraform plan` output proves the IaC works and shows the full resource graph
- Local development loop is faster with no AWS API round-trips

**Negative:**
- KinD does not support Karpenter node autoscaling (Karpenter configs are written but not deployed locally)
- LocalStack free tier covers SQS and Secrets Manager but not every AWS service
- Cannot demonstrate a live cloud deployment — must document the local-vs-cloud equivalence clearly in the README

**Why this doesn't reduce impressiveness:**
Every company uses KinD or minikube for local development. Demonstrating that the platform runs locally *and* is architected for cloud shows understanding of the abstraction layer — which is more valuable than a running cloud bill.
