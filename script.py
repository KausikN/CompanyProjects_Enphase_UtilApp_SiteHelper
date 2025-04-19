"""
Script Runner for Site Helper
"""

# Imports
import json
import argparse
from tqdm import tqdm
from SiteHelper import *

# Utils Classes
class PROGRESS_BAR:
    def __init__(self, total=1, increment_type="percent"):
        self.PROGRESS = tqdm(total)
        self.total = total
        self.increment_type = increment_type
    
    def progress(self, value, text=""):
        if self.increment_type == "percent":
            self.PROGRESS.update(int(round(value * self.total)))
        else:
            self.PROGRESS.update(value)


# Utils Functions
def Utils_ParseArgs():
    '''
    Utils - Parse Args
    '''
    PARSER = argparse.ArgumentParser(
        prog="Site Helper Scripts",
        description="Scripts for running Site Helper tools via Command Line"
    )
    PARSER.add_argument(
        "-t", "--type",
        help="Tool: Can be 'collect_api_responses', 'site_search'",
        default="collect_api_responses"
    )
    PARSER.add_argument(
        "-is", "--inp_sites",
        help="Sites Input JSON Path",
        default="Data/SCRIPT_DATA/SiteAPISearch_CollectAPIResponses/sites.json"
    )
    PARSER.add_argument(
        "-ip", "--inp_params",
        help="Input Parameters JSON Path",
        default="Data/SCRIPT_DATA/SiteAPISearch_CollectAPIResponses/input.json"
    )
    PARSER.add_argument(
        "-if", "--inp_search",
        help="Search Input JSON Path",
        default="Data/SCRIPT_DATA/SiteAPISearch_CollectAPIResponses/search_input.json"
    )
    PARSER.add_argument(
        "-o", "--out",
        help="Output JSON Path",
        default="Data/SCRIPT_DATA/SiteAPISearch_CollectAPIResponses/output.json"
    )
    ARGS = PARSER.parse_args()

    return ARGS

# Main Functions
def Script_SiteAPISearch_CollectAPIResponses(ARGS):
    '''
    Script - Site API Search - Collect API Responses
    '''
    # Sites
    SITES_JSON = json.load(open(ARGS.inp_sites, "r"))
    SITES = []
    if SITES_JSON["input_type"] == "admin_api":
        SITES = SiteHelper_AdminDataAPIDecoder(SITES_JSON["data"])
    else:
        SITES = SITES_JSON["data"]

    # Params
    PARAMS = json.load(open(ARGS.inp_params, "r"))
    USERINPUT_API = PARAMS["API"]
    USERINPUT_Env = PARAMS["Environment"]
    USERINPUT_URLReplaceParams = PARAMS["params"]["url_replace_params"]
    USERINPUT_URLParams = PARAMS["params"]["url_params"]
    USERINPUT_Cookies = PARAMS["params"]["cookies"]
    USERINPUT_Headers = PARAMS["params"]["headers"]

    # Run
    API_DATA = {
        "name": USERINPUT_API,
        "env": USERINPUT_Env
    }
    for i in tqdm(
        range(len(SITES)),
        desc="API Collection Progress"
    ):
        CUR_URLReplaceParams = dict(USERINPUT_URLReplaceParams)
        CUR_URLReplaceParams.update({
            "site": SITES[i]
        })
        RESPONSE = SITE_APIS_DATA[USERINPUT_API]["request_func"](
            SITE_APIS_DATA[USERINPUT_API]["env_url_map"][USERINPUT_Env],
            CUR_URLReplaceParams,
            USERINPUT_URLParams,
            USERINPUT_Cookies,
            USERINPUT_Headers
        )
        SITE_RESPONSE = {
            "site": SITES[i],
            "params": {
                "url_replace_params": dict(CUR_URLReplaceParams),
                "url_params": dict(USERINPUT_URLParams),
                "cookies": dict(USERINPUT_Cookies),
                "headers": dict(USERINPUT_Headers)
            },
            "status_code": RESPONSE.status_code,
            "response_json": RESPONSE.json()
        }
        SiteHelper_SaveSiteAPIResponses(API_DATA, SITE_RESPONSE)

def Script_SiteAPISearch_SearchSites(ARGS):
    '''
    Script - Site API Search - Search Sites
    '''
    # Search Params
    PARAMS = json.load(open(ARGS.inp_search, "r"))
    USERINPUT_API = PARAMS["API"]
    USERINPUT_Env = PARAMS["Environment"]
    USERINPUT_URLReplaceParams = PARAMS["params"]["url_replace_params"]
    USERINPUT_URLParams = PARAMS["params"]["url_params"]
    USERINPUT_Cookies = PARAMS["params"]["cookies"]
    USERINPUT_Headers = PARAMS["params"]["headers"]
    USERINPUT_MatchResponse = PARAMS["response_match"]

    # Run
    API_DATA = {
        "name": USERINPUT_API,
        "env": USERINPUT_Env
    }
    MATCH_PARAMS = {
        "url_replace_params": dict(USERINPUT_URLReplaceParams),
        "url_params": dict(USERINPUT_URLParams),
        "cookies": dict(USERINPUT_Cookies),
        "headers": dict(USERINPUT_Headers)
    }
    MATCHES = SiteHelper_SearchSiteAPIResponses(API_DATA, MATCH_PARAMS, USERINPUT_MatchResponse, show_tqdm=True)

    # Save
    json.dump(MATCHES, open(ARGS.out, "w"), indent=4)


# Run Code
ARGS = Utils_ParseArgs()

if ARGS.type == "collect_api_responses":
    Script_SiteAPISearch_CollectAPIResponses(ARGS)
else:
    Script_SiteAPISearch_SearchSites(ARGS)