#!/bin/bash
echo "🧪 Starting Wellness Solutions Test Flow..."
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Check all containers are running
echo -e "\n✅ Checking Docker containers..."
docker ps --format "table {{.Names}}\t{{.Status}}" | grep jpf_stretch

# 2. Test home page
echo -e "\n✅ Testing home page..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200"; then
    echo -e "${GREEN}Home page: OK ✓${NC}"
else
    echo -e "${RED}Home page: FAILED ✗${NC}"
fi

# 3. Test admin page
echo -e "\n✅ Testing admin page..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/admin/ | grep -q "302\|200"; then
    echo -e "${GREEN}Admin page: OK ✓${NC}"
else
    echo -e "${RED}Admin page: FAILED ✗${NC}"
fi

# 4. Test API auth with correct field
echo -e "\n✅ Testing API authentication..."
# First, try to get CSRF token and test with username field (DRF default)
AUTH_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth-token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin@example.com", "password": "admin123"}' 2>/dev/null)

TOKEN=$(echo "$AUTH_RESPONSE" | python -c "import sys, json; data = json.load(sys.stdin) if sys.stdin.read().strip() else {}; print(data.get('token', ''))" 2>/dev/null || echo "")

if [ ! -z "$TOKEN" ]; then
    echo -e "${GREEN}API Auth: OK ✓ (Token retrieved)${NC}"
else
    echo -e "${RED}API Auth: FAILED ✗${NC}"
    echo "Response: $AUTH_RESPONSE"
fi

# 5. Test authenticated API endpoint
echo -e "\n✅ Testing authenticated API access..."
if [ ! -z "$TOKEN" ]; then
    API_RESPONSE=$(curl -s -w "\n%{http_code}" -H "Authorization: Token $TOKEN" http://localhost:8000/api/users/me/)
    HTTP_CODE=$(echo "$API_RESPONSE" | tail -n 1)
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}API Access: OK ✓${NC}"
        echo "User data retrieved successfully"
    else
        echo -e "${RED}API Access: FAILED ✗ (HTTP $HTTP_CODE)${NC}"
    fi
else
    echo "Skipping - no auth token available"
fi

# 6. Check Mailpit
echo -e "\n✅ Testing email service (Mailpit)..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8025 | grep -q "200"; then
    echo -e "${GREEN}Mailpit: OK ✓${NC}"
else
    echo -e "${RED}Mailpit: FAILED ✗${NC}"
fi

# 7. Check Flower
echo -e "\n✅ Testing Celery monitoring (Flower)..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5555 | grep -q "200"; then
    echo -e "${GREEN}Flower: OK ✓${NC}"
else
    echo -e "${RED}Flower: FAILED ✗${NC}"
fi

# 8. Database check
echo -e "\n✅ Testing database connectivity..."
if docker exec wellness_solutions_local_django python -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT 1'); print('DB OK')" 2>/dev/null | grep -q "DB OK"; then
    echo -e "${GREEN}Database: OK ✓${NC}"
else
    echo -e "${RED}Database: FAILED ✗${NC}"
fi

# 9. Check static files
echo -e "\n✅ Testing static files..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/css/project.css | grep -q "200"; then
    echo -e "${GREEN}Static files: OK ✓${NC}"
else
    echo -e "${RED}Static files: FAILED ✗${NC}"
fi

echo -e "\n========================================"
echo "🎉 Test flow complete!"
echo ""
echo "📝 Manual verification URLs:"
echo "  - Main app: http://localhost:8000"
echo "  - Admin: http://localhost:8000/admin (admin@example.com/admin123)"
echo "  - API Docs: http://localhost:8000/api/docs/ (requires login)"
echo "  - Emails: http://localhost:8025"
echo "  - Celery: http://localhost:5555"
echo ""
echo "📖 Full test documentation: test_flow.md"
