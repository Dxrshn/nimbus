#!/bin/bash
set -e

BASE_URL="http://localhost"

echo "=== Nimbus Platform Demo ==="
echo ""

echo "1. Shortening a URL..."
RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/dxrshn/nimbus"}')
echo "   Response: $RESPONSE"

SHORT_CODE=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['short_code'])")
SHORT_URL="$BASE_URL/r/$SHORT_CODE"
echo ""

echo "2. Testing redirect..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SHORT_URL")
echo "   $SHORT_URL → HTTP $HTTP_CODE (expect 301)"
echo ""

echo "3. Listing all URLs..."
curl -s "$BASE_URL/api/v1/urls" | python3 -m json.tool
echo ""

echo "4. Cluster status..."
kubectl get pods
echo ""

echo "=== Demo complete ==="
echo "   Dashboard: $BASE_URL"
echo "   ArgoCD:    https://localhost:8080"
echo "   Grafana:   http://localhost:3000"
