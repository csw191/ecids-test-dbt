# ================================================================
# FILE: Makefile
# LOCATION: ~/proj/dbt/ecids-test/Makefile
# ================================================================
.PHONY: install dev prod test clean docs

# Development setup
install:
	poetry install
	
dev:
	poetry run dbt parse --project-dir ecids_test
	poetry run dagster dev -f hhs_platform/definitions.py

# Production deployment
prod:
	docker-compose up -d

# Testing
test:
	poetry run pytest tests/
	poetry run dbt test --project-dir ecids_test

# Documentation
docs:
	poetry run dbt docs generate --project-dir ecids_test
	poetry run dbt docs serve --project-dir ecids_test

# Cleanup
clean:
	docker-compose down
poetry run dbt clean --project-dir ecids_test