# Nimbus Platform

A production-grade cloud-native URL shortener built on Kubernetes, demonstrating modern DevOps practices end-to-end. Runs entirely locally on KinD at $0/month, with Terraform modules validated and ready for AWS EKS.

## What this demonstrates

| Practice | Implementation |
| -------- | -------------- |
| **Infrastructure as Code** | Terraform modules for VPC, EKS, RDS, ElastiCache, SQS — validated and security-scanned in CI |
| **Container orchestration** | Kubernetes with Helm charts, Kustomize overlays, RBAC, NetworkPolicies |
| **CI/CD** | GitHub Actions with reusable workflows, path-based matrix builds, GHCR |
| **GitOps** | ArgoCD app-of-apps with auto-sync and self-healing |
| **Observability** | Prometheus + Grafana + Loki + OpenTelemetry tracing |
| **Security** | Kyverno policies, Trivy scanning, External Secrets Operator, Gitleaks |
| **Autoscaling** | HPA for pods, Karpenter node pool configs for EKS |
| **Local development** | KinD multi-node cluster with LocalStack (SQS, Secrets Manager) |

## Architecture

```text
                        ┌─────────────────────────────────┐
                        │         KinD Cluster             │
                        │                                  │
  Browser / curl ──────▶│  NGINX Ingress                  │
                        │    /api  ──▶  shortener-api      │
                        │    /r    ──▶  redirect-svc       │
                        │    /     ──▶  dashboard-ui       │
                        │                                  │
                        │  shortener-api ──▶ PostgreSQL    │
                        │                ──▶ Redis         │
                        │                ──▶ LocalStack    │
                        │                    (SQS)         │
                        │                                  │
                        │  analytics-worker ◀── SQS        │
                        │                  ──▶ PostgreSQL  │
                        └─────────────────────────────────┘
```

## Quick start

```bash
# Prerequisites: Docker, kind, kubectl, helm
git clone https://github.com/dxrshn/nimbus.git
cd nimbus
bash scripts/cluster-up.sh
```

Once running:

| Service | URL | Credentials |
| ------- | --- | ----------- |
| App | `http://localhost` | — |
| ArgoCD | `https://localhost:8080` | admin / (see below) |
| Grafana | `http://localhost:3000` | admin / nimbus-local |

```bash
# Get ArgoCD password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath='{.data.password}' | base64 -d
```

## Try it

```bash
# Shorten a URL
curl -X POST http://localhost/api/v1/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/dxrshn/nimbus"}'
# {"short_code": "abc123", "short_url": "http://localhost/r/abc123"}

# Follow the redirect
curl -L http://localhost/r/abc123
# → https://github.com/dxrshn/nimbus
```

## Repository structure

```text
nimbus/
├── apps/
│   ├── shortener-api/      # Python/FastAPI — URL creation and storage
│   ├── redirect-svc/       # Go — high-performance redirect with Redis cache
│   ├── analytics-worker/   # Python — SQS consumer for click aggregation
│   └── dashboard-ui/       # React — URL management and analytics dashboard
├── k8s/
│   ├── base/               # Kustomize base manifests
│   ├── overlays/local/     # KinD-specific patches
│   ├── local-infra/        # PostgreSQL, Redis, LocalStack
│   ├── argocd/             # ArgoCD app-of-apps
│   ├── observability/      # Prometheus, Grafana, Loki, OTel
│   └── security/           # Kyverno policies, External Secrets
├── terraform/
│   ├── modules/            # vpc, eks, ecr, iam, rds, elasticache, sqs, secrets
│   └── environments/dev/   # Wires modules together
├── scripts/
│   ├── cluster-up.sh       # Full cluster bootstrap
│   └── demo.sh             # End-to-end demo
├── .github/workflows/      # CI pipelines (apps, terraform, security)
└── docs/
    ├── adr/                # Architecture Decision Records
    ├── runbooks/           # Operational runbooks
    └── cost-analysis.md    # AWS cost breakdown and optimization
```

## Cloud architecture (AWS)

All Terraform modules are written, validated, and security-scanned via CI — but not applied (cost = $0). The platform is designed to run on EKS with:

- **VPC** — 3 AZs, public/private subnets, NAT gateway
- **EKS** — managed node group + Karpenter for spot autoscaling
- **RDS** — PostgreSQL with automated backups
- **ElastiCache** — Redis replication group with encryption
- **SQS** — Click events queue with DLQ
- **Secrets Manager** — App secrets surfaced via External Secrets Operator

See [docs/cost-analysis.md](docs/cost-analysis.md) for the full breakdown (~$165/month dev, ~$375/month prod).

## Architecture Decision Records

- [ADR-001: Why EKS over ECS](docs/adr/001-why-eks-over-ecs.md)
- [ADR-002: Why ArgoCD over Flux](docs/adr/002-why-argocd-over-flux.md)
- [ADR-003: Why Karpenter over Cluster Autoscaler](docs/adr/003-why-karpenter.md)
- [ADR-004: Local-first development strategy](docs/adr/004-local-vs-cloud-strategy.md)

## Services

| Service | Language | Key tech |
| ------- | -------- | -------- |
| shortener-api | Python 3.12 / FastAPI | asyncpg, Redis, SQS, OpenTelemetry |
| redirect-svc | Go 1.24 | Redis cache-first, distroless image |
| analytics-worker | Python 3.12 | SQS long-polling, asyncpg |
| dashboard-ui | React 18 | Vite, Tailwind CSS |
