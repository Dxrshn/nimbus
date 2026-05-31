# Cost Analysis

## Local Development: $0/month

| Component | Local Solution | AWS Equivalent | Monthly Savings |
|-----------|---------------|----------------|-----------------|
| Kubernetes | KinD (Docker) | EKS control plane | $73 |
| Worker nodes | KinD nodes (local CPU) | 2x t3.medium EC2 | $60 |
| PostgreSQL | In-cluster pod | RDS t3.micro | $15 |
| Redis | In-cluster pod | ElastiCache t3.micro | $13 |
| SQS | LocalStack | AWS SQS | ~$1 |
| NAT Gateway | Not needed locally | NAT Gateway | $32 |
| Load Balancer | NGINX ingress (local) | ALB | $16 |
| Container Registry | Local images | ECR | $1 |
| **Total** | **$0/month** | | **~$211/month** |

## What Actually Runs on AWS (Free Tier)

| Service | Usage | Free Tier Limit | Cost |
|---------|-------|-----------------|------|
| S3 | Terraform state (~1KB) | 5GB free | $0 |
| DynamoDB | State lock table | 25GB free | $0 |
| **Total** | | | **$0** |

## Production Cost Estimate (if deployed)

| Component | Size | Monthly Cost |
|-----------|------|-------------|
| EKS control plane | - | $73 |
| EC2 nodes | 2x t3.medium | $60 |
| RDS PostgreSQL | db.t3.micro | $15 |
| ElastiCache Redis | cache.t3.micro | $13 |
| NAT Gateway | 1x | $32 |
| ALB | 1x | $16 |
| ECR | 4 repos | $1 |
| **Total** | | **~$210/month** |

## Why This Approach Is Valid

Every serious engineering team maintains local development environments that mirror production. KinD + LocalStack is the same pattern used by teams at Airbnb, Spotify, and Shopify — the difference is they run it on more powerful machines.

The Terraform code, Kubernetes manifests, CI pipelines, and application code are production-identical. Running `terraform plan` against a real AWS account proves the IaC works. The only thing missing is the AWS bill.
