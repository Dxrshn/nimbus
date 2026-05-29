# Nimbus Platform — Architecture

## Overview

Nimbus is a URL shortener deployed as microservices on Kubernetes. The application layer is intentionally simple; the infrastructure, CI/CD, observability, and security around it represent the platform's value.

## Services

| Service | Language | Responsibility |
|---------|----------|---------------|
| `shortener-api` | Python (FastAPI) | URL creation, listing, stats — primary REST API |
| `redirect-svc` | Go | High-throughput redirects via Redis cache-first pattern |
| `analytics-worker` | Python | SQS consumer; aggregates click events into PostgreSQL |
| `dashboard-ui` | React (Vite) | Frontend served via nginx |

## Data Flow

```
User → NGINX Ingress
         ├── /api/**    → shortener-api → PostgreSQL (write) + Redis (cache)
         ├── /r/**      → redirect-svc  → Redis (read) → PostgreSQL (fallback)
         │                                └── SQS (publish click event)
         └── /**        → dashboard-ui
                              └── shortener-api (stats)

SQS (click-events) → analytics-worker → PostgreSQL
```

## Infrastructure

### Local (KinD)

- **Cluster**: KinD, 1 control-plane + 2 worker nodes
- **Registry**: Local Docker registry at `localhost:5001`
- **Databases**: PostgreSQL and Redis run as K8s Deployments with PVCs
- **AWS emulation**: LocalStack handles SQS and Secrets Manager

### Cloud (Terraform — validated, not applied)

- **Compute**: EKS managed node group + Karpenter for autoscaling
- **Network**: VPC with public/private subnets across 3 AZs, single NAT (dev) / multi-NAT (prod)
- **Storage**: RDS PostgreSQL, ElastiCache Redis, S3 for Terraform state
- **Messaging**: SQS with dead-letter queue
- **Images**: GHCR in CI; ECR module written for production
- **Secrets**: Secrets Manager via External Secrets Operator

## Security Posture

- All pods run as non-root with read-only root filesystem
- NetworkPolicies enforce default-deny with explicit per-service allowlists
- Kyverno policies block privileged containers, `:latest` tags, and unapproved registries
- Trivy Operator scans running workloads continuously
- Gitleaks runs on every commit via pre-commit and CI

## Observability

- **Metrics**: Prometheus scrapes all services; Grafana dashboards for RED metrics and business KPIs
- **Logs**: Loki aggregates logs from all pods
- **Traces**: OpenTelemetry instrumentation on `shortener-api` and `redirect-svc`
- **Alerts**: PrometheusRule for high error rate, high P99 latency, and pod crash-looping

## Local Ports

| Service | URL |
|---------|-----|
| Platform | http://localhost:80 |
| ArgoCD | http://localhost:8080 |
| Grafana | http://localhost:3001 |
