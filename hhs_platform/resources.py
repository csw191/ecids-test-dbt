# FILE: hhs_platform/resources.py
"""Resources updated with missing dbt_resource definition"""
import os
from dagster import ConfigurableResource
from dagster_dbt import DbtCliResource
from hhs_platform.config import config

class SnowflakeRSAResource(ConfigurableResource):
    """Snowflake resource with RSA key authentication only"""
    
    def get_connection(self):
        """Get Snowflake connection using RSA key"""
        try:
            import snowflake.connector
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.serialization import load_pem_private_key
            from cryptography.hazmat.backends import default_backend
            
            # Get connection params (no password reference)
            conn_params = config.get_snowflake_connection_params()
            
            # Handle private key if present
            if "private_key" in conn_params:
                private_key_str = conn_params["private_key"]
                
                # Parse the private key
                passphrase = conn_params.get("private_key_passphrase")
                if passphrase:
                    private_key = load_pem_private_key(
                        private_key_str.encode(),
                        password=passphrase.encode(),
                        backend=default_backend()
                    )
                else:
                    private_key = load_pem_private_key(
                        private_key_str.encode(),
                        password=None,
                        backend=default_backend()
                    )
                
                # Convert to DER format for Snowflake
                pkb = private_key.private_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                
                # Update connection params
                conn_params["private_key"] = pkb
            
            return snowflake.connector.connect(**conn_params)
            
        except Exception as e:
            raise Exception(f"Failed to connect to Snowflake: {e}")

# ADD THIS MISSING RESOURCE
dbt_resource = DbtCliResource(
    project_dir=str(config.dbt_project_dir),
    profiles_dir=str(config.dbt_profiles_dir),
    target=config.dbt_target
)

# Resource instances
snowflake_resource = SnowflakeRSAResource()
