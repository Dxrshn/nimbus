#!/bin/bash
set -e

echo "Building images..."
docker build -t nimbus/shortener-api:local apps/shortener-api
docker build -t nimbus/redirect-svc:local apps/redirect-svc
docker build -t nimbus/analytics-worker:local apps/analytics-worker
docker build -t nimbus/dashboard-ui:local apps/dashboard-ui

echo "Loading images into KinD..."
kind load docker-image nimbus/shortener-api:local --name nimbus
kind load docker-image nimbus/redirect-svc:local --name nimbus
kind load docker-image nimbus/analytics-worker:local --name nimbus
kind load docker-image nimbus/dashboard-ui:local --name nimbus

echo "Images loaded."
