# FILE: hhs_platform/definitions.py
"""Main Dagster definitions for HHS data platform - FIXED IMPORTS"""
from dagster import Definitions

# CHANGE: From relative imports to absolute imports
from hhs_platform.assets import (
    hhs_staging_assets,
    hhs_integration_assets,
    hhs_presentation_assets,
    data_freshness_check,
    data_quality_tests
)
from hhs_platform.jobs import (
    staging_job,
    integration_job,
    presentation_job,
    full_pipeline_job,
    monitoring_job
)
from hhs_platform.schedules import daily_hhs_pipeline, monitoring_schedule
from hhs_platform.sensors import data_arrival_sensor
from hhs_platform.resources import dbt_resource, snowflake_resource

# Professional Dagster definitions
defs = Definitions(
    assets=[
        hhs_staging_assets,
        hhs_integration_assets, 
        hhs_presentation_assets,
        data_freshness_check,
        data_quality_tests
    ],
    jobs=[
        staging_job,
        integration_job,
        presentation_job,
        full_pipeline_job,
        monitoring_job
    ],
    schedules=[
        daily_hhs_pipeline,
        monitoring_schedule
    ],
    sensors=[
        data_arrival_sensor
    ],
    resources={
        "dbt": dbt_resource,
        "snowflake": snowflake_resource
    }
)
