#!/bin/bash
set -e

echo "Creating KinD cluster..."
kind create cluster --config k8s/kind/cluster.yaml

echo "Installing NGINX ingress controller..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.0/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=180s

echo "Installing ArgoCD..."
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl wait --namespace argocd \
  --for=condition=available deployment/argocd-server \
  --timeout=120s

echo "Installing kube-prometheus-stack..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set grafana.adminPassword=nimbus-local \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false

echo "Installing Kyverno..."
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update
helm install kyverno kyverno/kyverno \
  --namespace kyverno \
  --create-namespace

echo "Deploying local infra (postgres, redis, localstack)..."
kubectl apply -k k8s/local-infra/

echo "Building and loading images..."
bash scripts/load-images.sh

echo "Deploying Nimbus platform..."
kubectl apply -k k8s/overlays/local
kubectl apply -f k8s/security/kyverno/policies/
kubectl apply -f k8s/argocd/applications/nimbus-local.yaml
kubectl apply -f k8s/observability/opentelemetry/collector.yaml

echo ""
echo "Nimbus Platform is running!"
echo "  App:     http://localhost"
echo "  ArgoCD:  https://localhost:8080  (admin / $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d))"
echo "  Grafana: http://localhost:3000   (admin / nimbus-local)"
