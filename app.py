"""
Streamlit GUI for Site Helper
"""

# Imports
import json
import streamlit as st
from SiteHelper import *

# Main Vars

# Main Functions
def UI_GetParams(PARAMS_DATA):
    '''
    UI - Get Params
    '''
    # Init
    USERINPUT_Params = {}
    # Load Params
    for k in PARAMS_DATA.keys():
        p = PARAMS_DATA[k]
        if p["type"] == "selection":
            USERINPUT_Params[k] = st.selectbox(p["name"], **p["params"])
        elif p["type"] == "number":
            USERINPUT_Params[k] = p["datatype"](st.number_input(p["name"], **p["params"]))
        elif p["type"] == "json":
            USERINPUT_Params[k] = json.loads(st.text_area(p["name"], **p["params"]))
        elif p["type"] == "constant":
            st.text_input(p["name"], value=str(p["value"]), disabled=True)
            USERINPUT_Params[k] = p["value"]
        else:
            USERINPUT_Params[k] = None

    return USERINPUT_Params


# UI Functions
def UI_SiteLinks():
    '''
    UI - Site Links
    '''
    # Title
    st.markdown("# Site Links")

    # Load Prereq Inputs

    # Load Inputs
    ## Project
    st.markdown("## Project")
    USERINPUT_Project = st.selectbox("Select Project", list(SITE_DATA.keys()))
    USERINPUT_Env = st.selectbox("Select Environment", list(SITE_DATA[USERINPUT_Project]["environments"].keys()))
    ## Parameters
    st.markdown("### Parameters")
    USERINPUT_Params = UI_GetParams(SITE_DATA[USERINPUT_Project]["params"])
    ## Session Parameters
    USERINPUT_SessionParams = {}
    if len(list(SITE_DATA[USERINPUT_Project]["session_params"].keys())):
        st.markdown("### Session Parameters")
        USERINPUT_SessionParams = UI_GetParams(SITE_DATA[USERINPUT_Project]["session_params"])
    ## Custom Parameters
    st.markdown("### Custom Parameters")
    USERINPUT_CustomParams = json.loads(st.text_area(
        "Custom Parameters",
        value="{}"
    ))
    USERINPUT_SessionParams.update(USERINPUT_CustomParams)

    # Process Inputs
    LINK = SiteHelper_FormSiteLink(
        SITE_DATA[USERINPUT_Project]["environments"][USERINPUT_Env]["domain"], 
        USERINPUT_Params, USERINPUT_SessionParams
    )

    # Display Outputs
    st.markdown("## Links")
    cols = st.columns((1, 3))
    cols[0].markdown("Link")
    cols[1].markdown(LINK)
    cols = st.columns((1, 3))
    cols[0].markdown("Text")
    cols[1].markdown("```shell\n" + LINK + "\n```")
    cols = st.columns((1, 3))
    cols[0].markdown("JSON")
    cols[1].json([LINK])

def UI_SiteAdminLinks():
    '''
    UI - Site Admin Links
    '''
    # Title
    st.markdown("# Site Admin Links")

    # Load Prereq Inputs

    # Load Inputs
    ## Parameters
    st.markdown("## Parameters")
    USERINPUT_Env = st.selectbox("Select Environment", list(ADMIN_SITE_DATA["environments"].keys()))
    USERINPUT_SiteID = st.number_input("Site ID", value=53)
    USERINPUT_Params = {
        "site_id": USERINPUT_SiteID
    }

    # Process Inputs
    LINKS = {
        k: ADMIN_SITE_DATA["environments"][USERINPUT_Env]["domain"] + ADMIN_SITE_DATA["links"][k].format(**USERINPUT_Params)
        for k in ADMIN_SITE_DATA["links"].keys()
    }

    # Display Outputs
    st.markdown("## Links")
    st.json(LINKS)

def UI_SiteAPISearch():
    '''
    UI - Site Admin Links
    '''
    # Title
    st.markdown("# Site API Search")

    # Operations
    OPERATIONS = {
        "Collect API Responses": UI_SiteAPISearch_CollectAPIResponses,
        "Search Sites": UI_SiteAPISearch_SearchSites,

    }
    USERINPUT_Operation = st.sidebar.selectbox(
        "Select Operation",
        list(OPERATIONS.keys())
    )

    # Execute Operation
    OPERATIONS[USERINPUT_Operation]()

def UI_SiteAPISearch_CollectAPIResponses():
    '''
    UI - Site API Search - Collect API Responses
    '''
    # Title
    st.markdown("# Collect API Responses")

    # Load Prereq Inputs

    # Load Inputs
    ## API
    st.markdown("## API")
    USERINPUT_API = st.selectbox("Select API", list(SITE_APIS_DATA.keys()))

    ## Env
    USERINPUT_Env = st.selectbox("Select Environment", list(SITE_APIS_DATA[USERINPUT_API]["env_url_map"].keys()))
    USERINPUT_APIURL = SITE_APIS_DATA[USERINPUT_API]["env_url_map"][USERINPUT_Env]
    st.markdown(f"```\n{USERINPUT_APIURL}\n```")

    ## Sites
    st.markdown("## Sites")
    USERINPUT_Sites = []
    USERINPUT_SiteInputType = st.selectbox("Select Sites Input Type", ["Enlighten Admin Data API Format", "JSON Array"])
    if USERINPUT_SiteInputType == "Enlighten Admin Data API Format":
        USERINPUT_Sites = json.loads(st.text_area(
            "Sites in Admin Data API Format",
            value="[]"
        ))
        USERINPUT_Sites = SiteHelper_AdminDataAPIDecoder(USERINPUT_Sites) 
    elif USERINPUT_SiteInputType == "JSON Array":
        USERINPUT_Sites = json.loads(st.text_area(
            "Sites JSON Array",
            value="[]"
        ))

    ## Parameters
    st.markdown("## Parameters")
    USERINPUT_URLReplaceParams = json.loads(st.text_area(
        "URL Replace Parameters",
        value=json.dumps(SITE_APIS_DATA[USERINPUT_API]["default_params"]["url_replace_params"], indent=8)
    ))
    USERINPUT_URLParams = json.loads(st.text_area(
        "URL Parameters",
        value=json.dumps(SITE_APIS_DATA[USERINPUT_API]["default_params"]["url_params"], indent=8)
    ))
    USERINPUT_Cookies = json.loads(st.text_area(
        "Cookies",
        value=json.dumps(SITE_APIS_DATA[USERINPUT_API]["default_params"]["cookies"], indent=8)
    ))
    USERINPUT_Headers = json.loads(st.text_area(
        "Headers",
        value=json.dumps(SITE_APIS_DATA[USERINPUT_API]["default_params"]["headers"], indent=8)
    ))

    # Process Inputs
    st.markdown("## Process")
    USERINPUT_Process = st.button("Process")
    if not USERINPUT_Process: return
    
    API_DATA = {
        "name": USERINPUT_API,
        "env": USERINPUT_Env
    }
    PROGRESS_BAR = st.progress(0.0, f"0/{len(USERINPUT_Sites)}")
    for i in range(len(USERINPUT_Sites)):
        CUR_URLReplaceParams = dict(USERINPUT_URLReplaceParams)
        CUR_URLReplaceParams.update({
            "site": USERINPUT_Sites[i]
        })
        RESPONSE = SITE_APIS_DATA[USERINPUT_API]["request_func"](
            USERINPUT_APIURL,
            CUR_URLReplaceParams,
            USERINPUT_URLParams,
            USERINPUT_Cookies,
            USERINPUT_Headers
        )
        SITE_RESPONSE = {
            "site": USERINPUT_Sites[i],
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
        PROGRESS_BAR.progress(round((i+1)/len(USERINPUT_Sites), 2), f"{i+1}/{len(USERINPUT_Sites)}")

    # Display Outputs
    st.markdown("Collection Completed ✅")

def UI_SiteAPISearch_SearchSites():
    '''
    UI - Site API Search - Search Sites
    '''
    # Title
    st.markdown("# Search Sites")

    # Load Prereq Inputs

    # Load Inputs
    ## API
    st.markdown("## API")
    USERINPUT_API = st.selectbox("Select API", list(SITE_APIS_DATA.keys()))

    ## Env
    USERINPUT_Env = st.selectbox("Select Environment", list(SITE_APIS_DATA[USERINPUT_API]["env_url_map"].keys()))
    USERINPUT_APIURL = SITE_APIS_DATA[USERINPUT_API]["env_url_map"][USERINPUT_Env]
    st.markdown(f"```\n{USERINPUT_APIURL}\n```")

    ## Parameters
    st.markdown("## Parameters")
    USERINPUT_URLReplaceParams = json.loads(st.text_area(
        "Match URL Replace Parameters",
        value=json.dumps(SITE_APIS_DATA[USERINPUT_API]["default_params"]["url_replace_params"], indent=8)
    ))
    USERINPUT_URLParams = json.loads(st.text_area(
        "Match URL Parameters",
        value=json.dumps(SITE_APIS_DATA[USERINPUT_API]["default_params"]["url_params"], indent=8)
    ))
    USERINPUT_Cookies = json.loads(st.text_area(
        "Match Cookies",
        value=json.dumps(SITE_APIS_DATA[USERINPUT_API]["default_params"]["cookies"], indent=8)
    ))
    USERINPUT_Headers = json.loads(st.text_area(
        "Match Headers",
        value=json.dumps(SITE_APIS_DATA[USERINPUT_API]["default_params"]["headers"], indent=8)
    ))

    ## Match Response
    st.markdown("## Response Match")
    USERINPUT_MatchResponse = json.loads(st.text_area(
        "Match Response",
        value="{}"
    ))

    # Process Inputs
    st.markdown("## Process")
    USERINPUT_Process = st.button("Process")
    if not USERINPUT_Process: return
    
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
    PROGRESS_BAR = st.progress(0.0)
    MATCHES = SiteHelper_SearchSiteAPIResponses(API_DATA, MATCH_PARAMS, USERINPUT_MatchResponse, PROGRESS_BAR=PROGRESS_BAR)

    st.json(MATCHES)



# UI Vars
TOOLS = {
    "Site Links": UI_SiteLinks,
    "Site Admin Links": UI_SiteAdminLinks,
    "Site API Search": UI_SiteAPISearch,
}

# App Functions
def app_main():
    '''
    App - Main
    '''
    # Title
    # st.markdown("# Site Helper")
    # Tool
    USERINPUT_Tool = st.sidebar.selectbox(
        "Select Tool",
        list(TOOLS.keys())
    )
    TOOLS[USERINPUT_Tool]()

# Run Code
if __name__ == "__main__":
    # Assign Objects

    # Run App
    app_main()