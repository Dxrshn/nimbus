.PHONY: cluster-up cluster-down build deploy all clean

# === CLUSTER LIFECYCLE ===
cluster-up:
	@echo "🌩️  Starting Nimbus Platform..."
	bash scripts/cluster-up.sh

cluster-down:
	@echo "🔥 Tearing down Nimbus Platform..."
	bash scripts/cluster-down.sh

# === BUILD ===
build:
	@echo "🐳 Building all images..."
	bash scripts/load-images.sh

# === DEPLOY ===
deploy: build
	@echo "🚀 Deploying to KinD..."
	kubectl apply -k k8s/overlays/local

# === FULL LIFECYCLE ===
all: cluster-up deploy
	@echo "✅ Nimbus Platform is running!"
	@echo "   Dashboard: http://localhost:3000"
	@echo "   ArgoCD:    http://localhost:8080"
	@echo "   Grafana:   http://localhost:3001"

# === TERRAFORM (validate only, no apply) ===
tf-validate:
	cd terraform/environments/dev && terraform init -backend=false && terraform validate

tf-plan:
	cd terraform/environments/dev && terraform plan -out=tfplan

tf-scan:
	checkov -d terraform/ --framework terraform
	tfsec terraform/

# === CLEANUP ===
clean: cluster-down
	docker system prune -f