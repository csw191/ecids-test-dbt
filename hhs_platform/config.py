# FILE: hhs_platform/config.py
"""EMERGENCY FIX - Force correct DAGSTER_HOME"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Force load .env file
env_file_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_file_path)

# DEBUG: Print what we're loading
print(f"Loading .env from: {env_file_path}")
print(f"DAGSTER_HOME from env: {os.getenv('DAGSTER_HOME')}")

class HHSConfig(BaseSettings):
    """Configuration with forced DAGSTER_HOME"""
    
    # Environment
    environment: str = Field(default="dev", env="HHS_ENV")
    
    # Snowflake Configuration
    snowflake_account: str = Field(..., env="SNOWFLAKE_ACCOUNT")
    snowflake_user: str = Field(..., env="SNOWFLAKE_USER") 
    snowflake_password: Optional[str] = Field(None, env="SNOWFLAKE_PASSWORD")
    snowflake_role: str = Field(..., env="SNOWFLAKE_ROLE")
    snowflake_warehouse: str = Field(..., env="SNOWFLAKE_WAREHOUSE")
    snowflake_database: str = Field(..., env="SNOWFLAKE_DATABASE")
    
    # RSA Key Authentication
    snowflake_private_key_path: Optional[str] = Field(None, env="SNOWFLAKE_PRIVATE_KEY_PATH")
    snowflake_private_key_passphrase: Optional[str] = Field(None, env="SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")
    
    # dbt Configuration
    dbt_project_dir: Path = Field(default=Path(__file__).parent.parent / "ecids_test")
    dbt_profiles_dir: Path = Field(default=Path.home() / ".dbt")
    dbt_target: str = Field(default="dev", env="DBT_TARGET")
    
    # EMERGENCY FIX: Force the correct DAGSTER_HOME path
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Override DAGSTER_HOME environment variable
        correct_dagster_home = "/home/jparep/proj/dbt/ecids-test/dagster_home"
        os.environ["DAGSTER_HOME"] = correct_dagster_home
        print(f"FORCED DAGSTER_HOME to: {correct_dagster_home}")
    
    @property
    def dagster_home(self) -> str:
        return "/home/jparep/proj/dbt/ecids-test/dagster_home"
    
    @property
    def data_sources(self) -> Dict[str, str]:
        """Data sources for monitoring"""
        return {
            "snap": "SNAP",
            "wic": "WIC"
        }
    
    def get_private_key(self) -> Optional[str]:
        """Load RSA private key from file"""
        if self.snowflake_private_key_path and os.path.exists(self.snowflake_private_key_path):
            with open(self.snowflake_private_key_path, 'r') as key_file:
                return key_file.read()
        return None
    
    def get_snowflake_connection_params(self) -> Dict[str, Any]:
        """Get Snowflake connection parameters"""
        params = {
            "account": self.snowflake_account,
            "user": self.snowflake_user,
            "role": self.snowflake_role,
            "warehouse": self.snowflake_warehouse,
            "database": self.snowflake_database,
        }
        
        # Prefer RSA key over password
        private_key = self.get_private_key()
        if private_key:
            params["private_key"] = private_key
            if self.snowflake_private_key_passphrase:
                params["private_key_passphrase"] = self.snowflake_private_key_passphrase
        elif self.snowflake_password:
            params["password"] = self.snowflake_password
        
        return params

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }

# Global config instance - this will force set DAGSTER_HOME
config = HHSConfig()

# Additional safety check - force override the environment variable at module level
os.environ["DAGSTER_HOME"] = "/home/jparep/proj/dbt/ecids-test/dagster_home"
print(f"Final DAGSTER_HOME: {os.environ.get('DAGSTER_HOME')}")
