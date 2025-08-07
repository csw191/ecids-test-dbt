# ================================================================
# FILE: hhs_platform/sensors.py
# LOCATION: ~/proj/dbt/ecids-test/hhs_platform/sensors.py
# ================================================================
"""Sensor definitions for HHS data platform"""
from dagster import (
    sensor,
    SensorEvaluationContext,
    RunRequest,
    SkipReason,
    DefaultSensorStatus
)
from .jobs import full_pipeline_job

@sensor(
    job=full_pipeline_job,
    default_status=DefaultSensorStatus.STOPPED
)
def data_arrival_sensor(context: SensorEvaluationContext):
    """Trigger pipeline when new data arrives"""
    # Example: Check for new files or database changes
    # This is a placeholder - implement actual data arrival detection
    
    # For now, skip to avoid constant triggering
    return SkipReason("Data arrival detection not implemented yet")
