#!/bin/bash
set -e

echo "Tearing down Nimbus Platform..."
kind delete cluster --name nimbus

echo "Stopping docker-compose services..."
docker compose down

echo "Done."
