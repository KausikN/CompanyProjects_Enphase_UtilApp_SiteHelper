"""
API Helper - Data.json
"""

# Imports
import os
import requests

# Main Functions
def APIRequest_DataJSON(url, url_replace_params={}, url_params={}, cookies={}, headers={}):
    COOKIES = {}
    COOKIES.update(cookies)

    HEADERS = {}
    HEADERS.update(headers)

    PARAMS = {
        "app": "1",
        "device_status": "non_retired",
        "is_mobile": "1",
    }
    PARAMS.update(url_params)

    URL_REPLACE_PARAMS = {
        "site": 53
    }
    URL_REPLACE_PARAMS.update(url_replace_params)

    URL = url # "https://qa2.enphaseenergy.com/app-api/{site}/data.json"
    URL = URL.format(**URL_REPLACE_PARAMS)

    RESPONSE = requests.get(
        URL,
        params=PARAMS,
        cookies=COOKIES,
        headers=HEADERS,
    )

    return RESPONSE

# Main Vars
APIS_DATA = {
    "DataJSON": {
        "request_func": APIRequest_DataJSON,
        "default_params": {
            "url_replace_params": {
                "site": "53"
            },
            "url_params": {
                "app": "1",
                "device_status": "non_retired",
                "is_mobile": "1",
            },
            "cookies": {},
            "headers": {}
        },
        "env_url_map": {
            "Production": "https://enlighten.enphaseenergy.com/app-api/{site}/data.json",
            "Pre-production": "https://enlighten-preprod.enphaseenergy.com/app-api/{site}/data.json",
            "Stage (QA2)": "https://qa2.enphaseenergy.com/app-api/{site}/data.json",
            "Integration": "https://enlighten-intg.qa-enphaseenergy.com/app-api/{site}/data.json",
            "Development": "https://enlighten-dev.qa-enphaseenergy.com/app-api/{site}/data.json",
            "Release": "https://enlighten-rel.enphaseenergy.com/app-api/{site}/data.json"
        }
    }
}

# Main Functions

# Run Code