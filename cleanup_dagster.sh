#!/bin/bash
# Complete cleanup script for Dagster cache and history

echo "🧹 Starting complete Dagster cleanup..."

# 1. Kill all Dagster processes
echo "1. Killing all Dagster processes..."
pkill -f dagster
pkill -f "dagster-webserver"
pkill -f "dagster-daemon" 
sleep 2

# 2. Remove ALL Python cache files
echo "2. Removing Python cache files..."
cd /home/jparep/proj/dbt/ecids-test/
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null

# 3. Remove Poetry cache
echo "3. Clearing Poetry cache..."
poetry cache clear pypi --all -n
poetry env info  # Just to see current env

# 4. Remove any old dagster_home directories
echo "4. Removing old dagster_home directories..."
rm -rf /tmp/dagster_home 2>/dev/null
rm -rf /tmp/dagster* 2>/dev/null
sudo rm -rf /tmp/dagster* 2>/dev/null

# 5. Remove user-level Dagster cache
echo "5. Removing user-level Dagster cache..."
rm -rf ~/.dagster 2>/dev/null
rm -rf ~/.cache/dagster 2>/dev/null

# 6. Clear system-level temp files
echo "6. Clearing system temp files..."
sudo find /tmp -name "*dagster*" -delete 2>/dev/null
sudo find /var/tmp -name "*dagster*" -delete 2>/dev/null

# 7. Remove any compiled extensions
echo "7. Removing compiled extensions..."
find . -name "*.so" -path "*dagster*" -delete 2>/dev/null

# 8. Create fresh dagster_home
echo "8. Creating fresh dagster_home directory..."
rm -rf ./dagster_home
mkdir -p ./dagster_home
chmod 755 ./dagster_home

# 9. Clear environment and reimport
echo "9. Clearing Python module cache..."
python3 -c "
import sys
import os
# Remove all Dagster-related modules from cache
modules_to_remove = [m for m in list(sys.modules.keys()) if any(x in m.lower() for x in ['dagster', 'hhs_platform'])]
for module in modules_to_remove:
    if module in sys.modules:
        print(f'Removing cached module: {module}')
        del sys.modules[module]
print('Python module cache cleared!')
"

# 10. Set environment variables
echo "10. Setting environment variables..."
export DAGSTER_HOME="/home/jparep/proj/dbt/ecids-test/dagster_home"
export PYTHONDONTWRITEBYTECODE=1  # Prevent .pyc files
unset DAGSTER_CONFIG_FILE  # Remove any config file references

echo "✅ Cleanup complete!"
echo "DAGSTER_HOME is now: $DAGSTER_HOME"
echo ""
echo "🚀 Ready to start fresh Dagster instance!"
echo "Run: poetry run dagster dev -m hhs_platform.definitions"
