from __future__ import annotations

import os

ENV_API_KEY = "DATA_GOV_SG_API_KEY"
HEADER_API_KEY = "x-api-key"

DEFAULT_TIMEOUT = 30.0

# data.gov.sg hosts
CATALOG_BASE_URL = "https://api-production.data.gov.sg/v2/public/api"
CKAN_BASE_URL = "https://data.gov.sg"
REALTIME_BASE_URL = "https://api-open.data.gov.sg/v2/real-time/api"


def default_api_key() -> str | None:
    return os.environ.get(ENV_API_KEY)
