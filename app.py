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


# UI Vars
TOOLS = {
    "Site Links": UI_SiteLinks
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