#!/bin/bash

# Cleanup Script - Remove Unused Files from Resume Screener Project
# Date: October 14, 2025

echo "🧹 Starting cleanup of unused files..."

# Navigate to project root
cd /Users/rajeevranjanpratapsingh/Downloads/RESUME_JD

# ============================================
# 1. REMOVE DUPLICATE/BACKUP DOCUMENTATION
# ============================================
echo "📄 Cleaning up duplicate documentation files..."

rm -f "ALL_ISSUES_RESOLVED.md"
rm -f "BEFORE_AFTER_COMPARISON.md"
rm -f "DASHBOARD_ERRORS_FIXED.md"
rm -f "ERROR_FIXES_COMPLETE.md"
rm -f "FINAL_RESOLUTION.md"
rm -f "HYDRATION_FIX_FINAL.md"
rm -f "HYDRATION_NUCLEAR_SOLUTION.md"
rm -f "HYDRATION_ULTIMATE_FIX.md"
rm -f "LANDING_PAGE_COMPLETE.md"
rm -f "PARSING_CHECKLIST.md"
rm -f "PARSING_COMPLETE.md"
rm -f "PARSING_SUCCESS.md"
rm -f "PROJECT_STATUS_COMPLETE.md"
rm -f "SHADCN_COMPLETE_GUIDE.md"

echo "[✓] Removed 14 duplicate documentation files"

# ============================================
# 2. REMOVE BACKUP FILES IN BACKEND
# ============================================
echo "[💾] Cleaning up backend backup files..."

rm -f "backend/app/services/gemini_service_improved.py"
rm -f "backend/app/services/gemini_service_old_backup.py"

echo "[✓] Removed 2 backend backup files"


# ============================================
# 4. REMOVE UNUSED FRONTEND PAGES
# ============================================
echo "[📱] Cleaning up unused frontend pages..."

# Remove auth page (using login/register instead)
rm -rf "frontend/src/app/auth"

echo "[✓] Removed 1 unused page directory"

# ============================================
# 5. REMOVE BUILD ARTIFACTS (OPTIONAL)
# ============================================
echo "[🏗️] Cleaning up build artifacts..."

# Remove frontend build cache (will be regenerated)
rm -rf "frontend/.next"
rm -f "frontend/tsconfig.tsbuildinfo"

# Remove Python cache
find backend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find backend -type f -name "*.pyc" -delete 2>/dev/null || true

echo "[✓] Removed build artifacts and cache"

# ============================================
# 6. SUMMARY
# ============================================
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║  [✓] CLEANUP COMPLETE!                                   ║"
echo "║                                                          ║"
echo "║  Removed:                                                ║"
echo "║    • 14 duplicate documentation files                    ║"
echo "║    • 2 backend backup files                              ║"
                
echo "║    • 1 unused page directory (/auth)                     ║"
echo "║    • Build artifacts and cache                           ║"
echo "║                                                          ║"
echo "║  Total: ~37 files/directories removed                    ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "[📊] Project is now cleaner and more maintainable!"
echo ""
echo "Next steps:"
echo "  1. Verify application still works"
echo "  2. Commit changes to git"
echo "  3. Test all features"
echo ""
