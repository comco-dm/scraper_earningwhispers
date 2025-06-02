from __future__ import annotations

import os
import json
from typing import Optional, Dict

try:
    from google.cloud import secretmanager
    _has_secret_manager = True
except ImportError:
    _has_secret_manager = False


def get_proxy_from_secret() -> Optional[Dict[str, str]]:
    """Fetch proxy credentials from Google Cloud Secret Manager."""
    if not _has_secret_manager:
        return None
        
    # Get secret name from environment variable
    secret_name = os.getenv("PROXY_SECRET_NAME")
    if not secret_name:
        return None
        
    try:
        # Initialize the Secret Manager client
        client = secretmanager.SecretManagerServiceClient()
        
        # Get the project ID from environment (automatically set in Cloud Run)
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
        if not project_id:
            return None
            
        # Build the resource name of the secret version
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        
        # Access the secret version
        response = client.access_secret_version(request={"name": name})
        
        # Parse and return the secret data
        secret_data = response.payload.data.decode("UTF-8")
        return json.loads(secret_data)
        
    except Exception:
        # Silently fail and return None if anything goes wrong
        return None


def get_proxy_config() -> Optional[Dict[str, str]]:
    """Get proxy configuration from environment, secret, or disabled.
    
    Returns None if proxy should be disabled, otherwise returns proxy config dict.
    """
    # Check if proxy is disabled
    if os.getenv("DISABLE_PROXY", "").lower() in ("true", "1", "yes"):
        return None
    
    # Try to get from PROXY_CREDENTIALS env var (JSON string)
    proxy_creds = os.getenv("PROXY_CREDENTIALS")
    if proxy_creds:
        try:
            return json.loads(proxy_creds)
        except json.JSONDecodeError:
            pass
    
    # Try to get from Google Cloud Secret Manager
    secret_config = get_proxy_from_secret()
    if secret_config:
        return secret_config
    
    # Fall back to individual env vars (for local testing)
    endpoint = os.getenv("PROXY_ENDPOINT")
    user = os.getenv("PROXY_USER") 
    password = os.getenv("PROXY_PASS")
    
    if endpoint and user and password:
        return {
            "proxy_endpoint": endpoint,
            "proxy_user": user,
            "proxy_pass": password
        }
    
    return None


def get_aiohttp_proxy_config() -> Optional[str]:
    """Get proxy URL formatted for aiohttp.
    
    Returns proxy URL string or None if proxy disabled.
    """
    config = get_proxy_config()
    if not config:
        return None
    
    endpoint = config["proxy_endpoint"]
    user = config["proxy_user"]
    password = config["proxy_pass"]
    
    return f"http://{user}:{password}@{endpoint}" 