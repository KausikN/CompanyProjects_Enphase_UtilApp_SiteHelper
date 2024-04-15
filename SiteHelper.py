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
                    "options": ["profile", "battery", "storm-guard"]
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
                "type": "selection",
                "params": {
                    "options": ["enho", "itk"]
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
            "elu": {
                "name": "ELU",
                "type": "constant",
                "value": 0
            }
        }
    }
}

ADMIN_SITE_DATA = {
    "environments": {
        "Production": {
            "domain": "https://enlighten.enphaseenergy.com/"
        },
        "Pre-Production": {
            "domain": "https://enlighten-preprod.enphaseenergy.com/"
        },
        "Stage - QA2": {
            "domain": "https://qa2.enphaseenergy.com/"
        },
        "Release": {
            "domain": "https://enlighten-rel.enphaseenergy.com/"
        }
    },
    "links": {
        "Manager - Dashboard": "manager/dashboard",
        "Manager - Systems": "manager/dashboard/systems",
        "System - Dashboard": "systems/{site_id}",
        "System - Devices": "systems/{site_id}/devices",
        "System - Details": "systems/{site_id}/details",
        "Admin - Dashboard": "admin/sites/{site_id}",
        "Admin - Devices": "admin/sites/{site_id}/devices",
        "Admin - Events": "admin/sites/{site_id}/events",
        "Admin - Access": "admin/sites/{site_id}/access",
        "Admin - System Log": "admin/sites/{site_id}/log",
        "Admin - Email Log": "admin/sites/{site_id}/email_log",
        "Admin - Gateway / EMU Reports": "admin/sites/{site_id}/emu_reports",
        "Admin - Rollup": "admin/sites/{site_id}/rollup",
        "EEAdmin - Dashboard": "eeadmin/sites/{site_id}",
        "EEAdmin - Tasks": "eeadmin/task/show_task/{site_id}",
        "EEAdmin - Command History": "eeadmin/sites/{site_id}/command_history",
        "EEAdmin - Analytics": "eeadmin/analytics/{site_id}"
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