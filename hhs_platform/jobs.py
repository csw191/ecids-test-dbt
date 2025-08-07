# ================================================================
# FILE: hhs_platform/jobs.py
# LOCATION: ~/proj/dbt/ecids-test/hhs_platform/jobs.py
# ================================================================
"""Job definitions for HHS data platform"""
from dagster import (
    job, 
    op,
    AssetSelection,
    define_asset_job,
    DefaultSensorStatus,
    RunRequest,
    sensor,
    SkipReason
)
from .assets import (
    hhs_staging_assets,
    hhs_integration_assets, 
    hhs_presentation_assets,
    data_freshness_check,
    data_quality_tests
)

# Asset-based jobs (recommended approach)
staging_job = define_asset_job(
    name="hhs_staging_pipeline",
    selection=AssetSelection.groups("staging"),
    description="Process all staging layer models for child assistance programs"
)

integration_job = define_asset_job(
    name="hhs_integration_pipeline", 
    selection=AssetSelection.groups("intermediate"),
    description="Execute integration layer business logic"
)

presentation_job = define_asset_job(
    name="hhs_presentation_pipeline",
    selection=AssetSelection.groups("marts"),
    description="Generate final presentation layer tables"
)

full_pipeline_job = define_asset_job(
    name="hhs_full_pipeline",
    selection=AssetSelection.all(),
    description="Complete HHS data pipeline from staging to presentation"
)

monitoring_job = define_asset_job(
    name="hhs_monitoring_pipeline",
    selection=AssetSelection.groups("monitoring"),
    description="Data quality monitoring and freshness checks"
)