# FILE: hhs_platform/assets.py - FIXED IMPORTS
"""Asset definitions for HHS data platform"""
import os
from pathlib import Path
from typing import Any, Dict
from dagster import (
    AssetExecutionContext, 
    asset, 
    AssetMaterialization,
    MetadataValue,
    Output
)
from dagster_dbt import DbtCliResource, dbt_assets

# CHANGE: From relative imports to absolute imports
from hhs_platform.config import config
from hhs_platform.resources import dbt_resource

# dbt manifest path
DBT_MANIFEST_PATH = config.dbt_project_dir / "target" / "manifest.json"

@dbt_assets(
    manifest=DBT_MANIFEST_PATH,
    select="staging",
    name="hhs_staging_models"
)
def hhs_staging_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    """HHS staging layer - SNAP, WIC, and other child assistance programs"""
    yield from dbt.cli(["build", "--select", "staging"], context=context).stream()

@dbt_assets(
    manifest=DBT_MANIFEST_PATH,
    select="intermediate", 
    name="hhs_integration_models"
)
def hhs_integration_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    """HHS integration layer - cross-program business logic"""
    yield from dbt.cli(["build", "--select", "intermediate"], context=context).stream()

@dbt_assets(
    manifest=DBT_MANIFEST_PATH,
    select="marts",
    name="hhs_presentation_models"
)
def hhs_presentation_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    """HHS presentation layer - final analytical tables"""
    yield from dbt.cli(["build", "--select", "marts"], context=context).stream()

# Data quality monitoring assets
@asset(
    group_name="monitoring",
    description="Monitor data freshness across all HHS sources"
)
def data_freshness_check(context: AssetExecutionContext, dbt: DbtCliResource) -> Dict[str, Any]:
    """Check data freshness for all source systems"""
    result = dbt.cli(["source", "freshness"], context=context)
    
    # Parse freshness results and create metadata
    freshness_metadata = {
        "freshness_check_time": MetadataValue.timestamp(context.run_id),
        "sources_checked": MetadataValue.int(len(config.data_sources))
    }
    
    context.add_output_metadata(freshness_metadata)
    return {"status": "completed", "sources": list(config.data_sources.keys())}

@asset(
    group_name="monitoring", 
    description="Run data quality tests across all layers"
)
def data_quality_tests(context: AssetExecutionContext, dbt: DbtCliResource) -> Dict[str, Any]:
    """Execute data quality tests"""
    result = dbt.cli(["test"], context=context)
    
    test_metadata = {
        "test_run_time": MetadataValue.timestamp(context.run_id),
        "test_command": MetadataValue.text("dbt test")
    }
    
    context.add_output_metadata(test_metadata)
    return {"status": "completed", "tests_run": True}
