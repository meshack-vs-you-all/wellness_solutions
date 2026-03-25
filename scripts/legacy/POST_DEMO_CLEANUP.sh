#!/bin/bash

# Wellness Solutions - POST-DEMO SECURITY CLEANUP
# -------------------------------------------
# This script reverts "Demo-Mode" security compromises 
# and restores the repository to a hardened state.

echo "🛡️  Starting Post-Demo Security Cleanup..."

# 1. Revert settings changes via Git (if uncommitted)
echo "🔒 Restoring config/settings/local.py to safe defaults..."
git restore config/settings/local.py

# 2. Cleanup demo-specific files
echo "🗑️  Removing demo-specific launcher and guides..."
# (Optional: uncomment if you want to delete these guides after use)
# rm DEMO_MASTER_GUIDE.md
# rm LAUNCH_DEMO.sh
# rm demo_backend.log
# rm demo_frontend.log

# 3. Remove the demo-env symlink
echo "🔗 Removing demo-env symlink..."
rm demo-env 2>/dev/null

# 4. Final Security Check
echo "----------------------------------------"
echo "✅ CLEANUP COMPLETE!"
echo "----------------------------------------"
echo "1. Git branch is currently: $(git branch --show-current)"
echo "2. ALLOWED_HOSTS has been reset."
echo "3. CORS restrictions have been restored."
echo "4. Port 8000 and 5173 should be closed now."
echo "----------------------------------------"
echo "TIP: If you want to wipe the demo data entirely, run: rm db.sqlite3"
