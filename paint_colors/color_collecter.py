import pandas as pd
import numpy as np
import pathlib
import lxml
from lxml import html
import requests
import pickle


def get_cn_dulux_cmap(seed_url=f"https://www.dulux.com.cn/zh/colour-palettes/h_gold", save_to_local="./"):
    dulux_base_url = "https://www.dulux.com.cn"
    dulux_seed_res = requests.get(seed_url)
    dulux_seed_content = html.fromstring(dulux_seed_res.content)

    # Parse the html and get all categories.
    dulux_available_colors_xpath = f'//*[@id="block-system-main"]//a[contains(@class,"product-available")]'
    dulux_color_urls = [
        (a.get("title").strip(), dulux_base_url + a.get("href")) for a in
        dulux_seed_content.xpath(dulux_available_colors_xpath)
    ]

    target_attrs = [
        "data-title",
        "data-id",
        "data-colorid",
        "data-cccid",
    ]

    _dulux_colors = []
    for cat0_cn, dulux_c in dulux_color_urls:
        dulux_detail_res = requests.get(dulux_c)
        dulux_detail_content = html.fromstring(dulux_detail_res.content)
        dulux_dtl_a_list = dulux_detail_content.xpath(
            '//*[@id="block-system-main"]//a[contains(@class,"color-box-child")]')

        for a in dulux_dtl_a_list:
            _dulux_color = {}

            for col in target_attrs:
                _dulux_color[col.replace("data-", "")] = a.get(col)
            _dulux_color.update({"cat0_cn": cat0_cn})

            r_dec = int(_dulux_color["id"][:2], 16)
            g_dec = int(_dulux_color["id"][2:4], 16)
            b_dec = int(_dulux_color["id"][4:], 16)

            _dulux_color["R"] = r_dec
            _dulux_color["G"] = g_dec
            _dulux_color["B"] = b_dec

            _dulux_colors.append(_dulux_color)

    dulux_df = pd.DataFrame(_dulux_colors)
    dulux_df.rename(columns={"title": "code", "id": "hex_code"}, inplace=True)

    if save_to_local:
        save_folder = pathlib.Path(save_to_local)
        # if not save_folder.exists():
        #     save_folder.mkdir(parents=True, exist_ok=True)
        save_folder.mkdir(parents=True, exist_ok=True)
        with open(save_folder / "cn_dulux_color_df.pk", "wb") as f:
            pickle.dump(dulux_df, f)
    return dulux_df


def get_cn_nippon_cmap(seed_url=f"http://www.nipponpaint.com.cn/baidase/data_final.json", save_to_local="./"):
    nippon_res = requests.get(seed_url)
    nippon_json = nippon_res.json()
    nippon_data = nippon_json["data"]

    nippon_response_cols = [
        "index"
        , "cat0_en"
        , "cat0_cn"
        , "unk0"
        , "unk1"
        , "code"
        , "unk2"
        , "name"
        , "unk3"
        , "R"
        , "G"
        , "B"
    ]
    nippon_df = pd.DataFrame(nippon_data, columns=nippon_response_cols)
    nippon_df = nippon_df.drop(["index", "unk0", "unk1", "unk2", "unk3"], axis=1)

    def _get_hex_rgb(r, g, b):
        _h = [(hex(round(x))[2:].zfill(2)).upper() for x in [r, g, b]]
        hr = "".join(_h)
        return hr

    nippon_df["hex_code"] = nippon_df[["R", "G", "B"]].apply(lambda x: _get_hex_rgb(*x.values), axis=1)

    if save_to_local:
        save_folder = pathlib.Path(save_to_local)
        # if not save_folder.exists():
        #     save_folder.mkdir(parents=True, exist_ok=True)
        save_folder.mkdir(parents=True, exist_ok=True)
        with open(save_folder / "cn_nippon_color_df.pk", "wb") as f:
            pickle.dump(nippon_df, f)
    return nippon_df

