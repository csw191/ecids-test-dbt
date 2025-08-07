# ================================================================
# FILE: hhs_platform/schedules.py
# LOCATION: ~/proj/dbt/ecids-test/hhs_platform/schedules.py  
# ================================================================
"""Schedule definitions for HHS data platform"""
from dagster import schedule, ScheduleEvaluationContext, RunRequest
from .jobs import full_pipeline_job, monitoring_job
from .config import config

@schedule(
    job=full_pipeline_job,
    cron_schedule="0 6 * * *",  # Daily at 6 AM
    execution_timezone="America/New_York"
)
def daily_hhs_pipeline(context: ScheduleEvaluationContext):
    """Daily execution of complete HHS data pipeline"""
    return RunRequest(
        run_key=f"daily_run_{context.scheduled_execution_time.strftime('%Y%m%d')}",
        tags={
            "environment": config.environment,
            "pipeline_type": "daily_full",
            "scheduled": "true"
        }
    )

@schedule(
    job=monitoring_job,
    cron_schedule="0 */4 * * *",  # Every 4 hours  
    execution_timezone="America/New_York"
)
def monitoring_schedule(context: ScheduleEvaluationContext):
    """Regular monitoring and data quality checks"""
    return RunRequest(
        run_key=f"monitoring_{context.scheduled_execution_time.strftime('%Y%m%d_%H')}",
        tags={
            "environment": config.environment,
            "pipeline_type": "monitoring",
            "scheduled": "true"
        }
    )