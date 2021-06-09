import streamlit as st
import requests
import logging
import pandas as pd

SEARCH_COLOR_API = "http://127.0.0.1:10086/paintcolor"
KW_SEARCH_COLOR_EP = f"{SEARCH_COLOR_API}/_search"
RGB_SEARCH_NN_COLOR_EP = f"{SEARCH_COLOR_API}/nearest_colors_by_rgb"

REQ_HEADERS = {
    'Content-type': 'application/json',
}


def write_table(df):
    st.write(df)


def write_header():
    st.title('Paint Color Search')
    st.markdown('''
        - A simple playground to search paint colors from Dulux or Nippon with code or name.
        - Hope it's useful when you on picking paint colors for the house. 
    ''')


def kw_search_colors():
    st.subheader(f"Search colors")
    kw_txt = st.text_input(
        'Enter keyword of name or code for Dulux / Nippon colors',
        value="input code/name..."
    )
    if not kw_txt:
        return
    query_data = {
        "color_keyword": str(kw_txt)
    }

    res = requests.post(KW_SEARCH_COLOR_EP, headers=REQ_HEADERS, json=query_data)
    if res.status_code == 200:
        colors_dict = res.json()
        if "data" in colors_dict:
            colors_df = pd.DataFrame(colors_dict["data"], columns=colors_dict["headers"])
            # return colors_df
            write_table(colors_df)
    else:
        logging.error(f"Error when query colors.")
        logging.error(res.status_code)
        return


def search_RGB_color():
    st.subheader(f"Search nearest colors from Dulux/Nippon")
    hex_code = st.color_picker('Pick A Color', '#00f900')
    # st.write('The current color is', hex_code)
    st.markdown(f"The current color is: {hex_code}。 The nearest colors of Dulux/Nippon are: ")
    r, g, b = tuple(int(hex_code.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    query_data = {
        "R": r,
        "G": g,
        "B": b
    }
    res = requests.post(RGB_SEARCH_NN_COLOR_EP, headers=REQ_HEADERS, json=query_data)
    if res.status_code == 200:
        colors_dict = res.json()
        if "data" in colors_dict:
            colors_df = pd.DataFrame(colors_dict["data"], columns=colors_dict["headers"])
            # return colors_df
            if not colors_df.empty:
                write_table(colors_df)
                nn_hex = f"#{colors_df.iloc[0]['hex_code']}"
                st.markdown(f"""The nearest color is look like: """)
                st.markdown(f'''
                <p style="background-color:{nn_hex};"><br><br><br><br><br><br></p>
                ''', unsafe_allow_html=True)
    else:
        logging.error(f"Error when query colors.")
        logging.error(res.status_code)
        return
    # st.markdown('<style>body{background-color: Blue;}This is a result box</style>', unsafe_allow_html=True)


def production_mode():
    # Src: discuss.streamlit.io/t/how-do-i-hide-remove-the-menu-in-production/362
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    return


if __name__ == '__main__':
    st.set_page_config(
        page_title='Paint Color Search',
        page_icon='️',
        # layout='wide'
    )
    # production_mode()
    write_header()
    kw_search_colors()
    search_RGB_color()
    # write_footer()

