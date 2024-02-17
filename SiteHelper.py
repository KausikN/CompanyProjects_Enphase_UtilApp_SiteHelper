"""
SiteHelper
"""

# Imports
import os

# Main Vars
SITE_DATA = {
    "ENHO App": {
        "repository": "https://bitbucket.org/enphaseembedded/e_mobile",
        "environments": {
            "Production": {
                "domain": "https://enlighten.enphaseenergy.com/{ui_type}/{site_id}"
            },
            "Pre-Production": {
                "domain": "https://enlighten-preprod.enphaseenergy.com/{ui_type}/{site_id}"
            },
            "Stage - QA2": {
                "domain": "https://qa2.enphaseenergy.com/{ui_type}/{site_id}"
            },
            "Release": {
                "domain": "https://enlighten-rel.enphaseenergy.com/{ui_type}/{site_id}"
            },
            "Local": {
                "domain": "http://localhost:4000/{ui_type}/{site_id}"
            },
        },
        "params": {
            "ui_type": {
                "name": "UI Type",
                "type": "selection",
                "params": {
                    "options": ["mobile", "web"]
                }
            },
            "site_id": {
                "name": "Site ID",
                "type": "number",
                "datatype": lambda v: int(v),
                "params": {
                    "value": 53,
                    "min_value": 0
                }
            }
        },
        "session_params": {}
    },
    "Battery Profile": {
        "repository": "https://bitbucket.org/enphaseembedded/battery_profile_ui",
        "environments": {
            "Stage - QA2": {
                "domain": "https://battery-profile-ui-qa.enphaseenergy.com"
            },
            "Release": {
                "domain": "https://battery-profile-ui-rel.enphaseenergy.com"
            },
            "Local": {
                "domain": "http://localhost:3007"
            },
        },
        "params": {},
        "session_params": {
            "type": {
                "name": "Page",
                "type": "selection",
                "params": {
                    "options": ["profile", "battery"]
                }
            },
            "siteId": {
                "name": "Site ID",
                "type": "number",
                "datatype": lambda v: int(v),
                "params": {
                    "value": 53,
                    "min_value": 0
                }
            },
            "source": {
                "name": "Source",
                "type": "constant",
                "value": "enho"
            },
            "uiType": {
                "name": "UI Type",
                "type": "selection",
                "params": {
                    "options": ["mobile", "web"]
                }
            },
            "theme": {
                "name": "Theme",
                "type": "selection",
                "params": {
                    "options": ["light", "dark"]
                }
            },
            "elu": {
                "name": "ELU",
                "type": "constant",
                "value": 0
            },
            "locale": {
                "name": "Language",
                "type": "selection",
                "params": {
                    "options": ["en", "de", "es", "fr", "it", "nl", "pl", "pt"]
                }
            }
        }
    },
    "Tariff Editor": {
        "repository": "https://bitbucket.org/enphaseembedded/tariff-editor",
        "environments": {
            "Local": {
                "domain": "http://localhost:3005/tariff"
            },
        },
        "params": {},
        "session_params": {
            "siteId": {
                "name": "Site ID",
                "type": "number",
                "datatype": lambda v: int(v),
                "params": {
                    "value": 53,
                    "min_value": 0
                }
            },
            "uiType": {
                "name": "UI Type",
                "type": "selection",
                "params": {
                    "options": ["mobile", "web"]
                }
            },
            "theme": {
                "name": "Theme",
                "type": "selection",
                "params": {
                    "options": ["light", "dark"]
                }
            },
            "locale": {
                "name": "Language",
                "type": "selection",
                "params": {
                    "options": ["en", "de", "es", "fr", "it", "nl", "pl", "pt"]
                }
            },
            "origin": {
                "name": "Origin",
                "type": "selection",
                "params": {
                    "options": [
                        "https://qa2.enphaseenergy.com", 
                        "https://enlighten-rel.enphaseenergy.com"
                    ]
                }
            },
            "isAutoFillFeatureEnabled": {
                "name": "Is Auto Fill Feature Enabled?",
                "type": "selection",
                "params": {
                    "options": ["1", "0"]
                }
            },
            "isTariffMqttEnabled": {
                "name": "Is Tariff MQTT Enabled?",
                "type": "selection",
                "params": {
                    "options": ["1", "0"]
                }
            },
            "isManualUpdateEnabled": {
                "name": "Is Manual Update Enabled?",
                "type": "selection",
                "params": {
                    "options": ["1", "0"]
                }
            }
        }
    }
}

# Main Functions
def SiteHelper_FormSiteLink(domain, params, session_params):
    '''
    Site Helper - Form Site Link
    '''
    # Init
    LINK = ""
    # Form Link
    ## Substitute params to domain
    LINK = domain.format(**params)
    ## Add Session params
    if len(list(session_params.keys())) > 0:
        session_params_str = {}
        for p in session_params.keys():
            session_param_str = str(session_params[p]).replace(" ", "+") # Replace empty spaces with "+"
            session_params_str[p] = session_param_str
        LINK = LINK + "?" + "&".join([f"{p}={session_params_str[p]}" for p in session_params_str.keys()])

    return LINK

# Run Code