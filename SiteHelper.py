"""
SiteHelper
"""

# Imports
import os
import json
import time
from tqdm import tqdm

from APIHelpers.API_DataJSON import APIS_DATA as APIS_DATA_DataJSON

# Main Vars
SITE_DATA = {
    "ENHO App": {
        "repository": "https://bitbucket.org/enphaseembedded/e_mobile",
        "environments": {
            "Production": {
                "domain": "https://enlighten.enphaseenergy.com/{ui_type}/{site_id}"
            },
            "Pre-production": {
                "domain": "https://enlighten-preprod.enphaseenergy.com/{ui_type}/{site_id}"
            },
            "Stage (QA2)": {
                "domain": "https://qa2.enphaseenergy.com/{ui_type}/{site_id}"
            },
            "Release": {
                "domain": "https://enlighten-rel.enphaseenergy.com/{ui_type}/{site_id}"
            },
            "Integration": {
                "domain": "https://enlighten-intg.qa-enphaseenergy.com/{ui_type}/{site_id}"
            },
            "Development": {
                "domain": "https://enlighten-dev.qa-enphaseenergy.com/{ui_type}/{site_id}"
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
            "Production": {
                "domain": "https://battery-profile-ui.enphaseenergy.com"
            },
            "Pre-production": {
                "domain": "https://battery-profile-ui-preprod.enphaseenergy.com"
            },
            "Stage (QA2)": {
                "domain": "https://battery-profile-ui-qa.enphaseenergy.com"
            },
            "Integration": {
                "domain": "https://battery-profile-ui-intg.qa-enphaseenergy.comm"
            },
            "Development": {
                "domain": "https://battery-profile-ui-dev.qa-enphaseenergy.com"
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
        "Pre-production": {
            "domain": "https://enlighten-preprod.enphaseenergy.com/"
        },
        "Stage (QA2)": {
            "domain": "https://qa2.enphaseenergy.com/"
        },
        "Integration": {
            "domain": "https://enlighten-intg.qa-enphaseenergy.com/"
        },
        "Development": {
            "domain": "https://enlighten-dev.qa-enphaseenergy.com/"
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

SITE_APIS_DATA = {
    **APIS_DATA_DataJSON
}

# Util Vars
RESPONSE_MATCHER_DATA = {
    "keys": {
        "match_type": "__MATCH_TYPE__",
        # Type of matching for the selected field
        ## Possible values,
        ## "exact" - Value of the selected field must match EXACTLY as the provided data under "match_value" key
        ## "present" - Selected field must exist in the response under the current hierarchy and can have any value

        "match_value": "__MATCH_VALUE__",
        # Value to be compared with the value of the selected field
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

def SiteHelper_AdminDataAPIDecoder(sites_data):
    '''
    Site Helper - Convert sites in admin data API format to list
    '''
    SITES = [
        str(site["id"]["text"]) for site in sites_data
    ]

    return SITES

def SiteHelper_SaveSiteAPIResponses(api_data, site_api_response, save_dir="Data/API_DATA/"):
    '''
    Site Helper - Save site API responses
    '''
    CUR_EPOCH_TIME = time.time()
    API_SAVE_PATH = os.path.join(save_dir, api_data["name"], api_data["env"])
    os.makedirs(API_SAVE_PATH, exist_ok=True)

    site = site_api_response["site"]
    params = site_api_response["params"]
    status_code = site_api_response["status_code"]
    response_json = site_api_response["response_json"]

    SITE_RESPONSES_PATH = os.path.join(API_SAVE_PATH, f"{site}.json")

    CUR_RESPONSE = {
        "generated_time": CUR_EPOCH_TIME,
        "params": params,
        "status_code": status_code,
        "response_json": response_json
    }

    PREV_RESPONSES = []
    if os.path.exists(SITE_RESPONSES_PATH):
        PREV_RESPONSES = json.load(open(SITE_RESPONSES_PATH, "r"))
    
    responseFound = False
    for i in range(len(PREV_RESPONSES)):
        if len(list(CUR_RESPONSE["params"].keys())) == len(list(PREV_RESPONSES[i]["params"].keys())):
            if all(k in CUR_RESPONSE["params"] and v == PREV_RESPONSES[i]["params"][k] for k, v in CUR_RESPONSE["params"].items()):
                responseFound = True
                PREV_RESPONSES[i] = dict(CUR_RESPONSE)
                break
    
    if not responseFound:
        PREV_RESPONSES.append(CUR_RESPONSE)

    with open(SITE_RESPONSES_PATH, "w") as f: json.dump(PREV_RESPONSES, f, indent=4)

def SiteHelper_MatchSiteResponse(cur_match_field=None, match_response=None, response=None):
    '''
    Site Helper - Match site response - Recursive
    '''
    if RESPONSE_MATCHER_DATA["keys"]["match_type"] in match_response.keys():
        MATCH_TYPE = match_response[RESPONSE_MATCHER_DATA["keys"]["match_type"]]
        if MATCH_TYPE == "exact":
            if response == match_response[RESPONSE_MATCHER_DATA["keys"]["match_value"]]:
                return True
            return False
        else:
            # Default MATCH_TYPE is "present"
            return True

    for mk in match_response.keys():
        if not (mk in response.keys()):
            return False
        if not SiteHelper_MatchSiteResponse(mk, match_response[mk], response[mk]):
            return False
    
    return True


def SiteHelper_SearchSiteAPIResponses(api_data, match_params, match_response, data_dir="Data/API_DATA/", PROGRESS_BAR=None, show_tqdm=False):
    '''
    Site Helper - Save site API responses
    '''
    API_DATA_PATH = os.path.join(data_dir, api_data["name"], api_data["env"])

    SITES = [p.rstrip(".json") for p in os.listdir(API_DATA_PATH) if p.endswith(".json")]

    MATCHES = {}
    if PROGRESS_BAR is not None: PROGRESS_BAR.progress(0.0, f"0/{len(SITES)}")
    for i in tqdm(range(len(SITES)), disable=(not show_tqdm)):
        site = SITES[i]
        site_responses = json.load(open(os.path.join(API_DATA_PATH, f"{site}.json"), "r"))
        MATCHES_SITE = []
        for response in site_responses:
            matched = True
            for pk in match_params.keys():
                if pk not in response["params"].keys(): continue
                for k in match_params[pk].keys():
                    if not (k in response["params"][pk].keys() and response["params"][pk][k] == match_params[pk][k]):
                        matched = False
                        break
            if matched:
                if SiteHelper_MatchSiteResponse(None, match_response, response["response_json"]):
                    MATCHES_SITE.append(dict(response))
        if len(MATCHES_SITE) > 0:
            MATCHES[site] = MATCHES_SITE

        if PROGRESS_BAR is not None: PROGRESS_BAR.progress(round((i+1) / len(SITES), 2), f"{i+1}/{len(SITES)}")

    OUT = {
        "n_sites_total": len(SITES),
        "n_matches": len(list(MATCHES.keys())),
        "matches": MATCHES
    }
    
    return OUT
            
    


# Run Code