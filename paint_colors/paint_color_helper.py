import sys
import os
import importlib
import logging
import datetime
import pandas as pd
from sqlalchemy import types
from . import color_util

CUSTOM_MODULE_PATH = os.path.realpath("/Users/ccuulinay/github_proj/py_public_modules")
sys.path.append(CUSTOM_MODULE_PATH)

from tj_hub.db import mysql_helper


def get_db_engine():
    global db_engine
    db_engine = mysql_helper.get_tjhub_mysql_engine()
    return db_engine


def save_paint_color_api_audit_log(msg):
    if "db_engine" not in globals():
        get_db_engine()
    msg_df = pd.DataFrame([msg])
    msg_df["DATA_DATE"] = datetime.datetime.now()
    print(msg_df)

    db_types = {
        "app_name": types.VARCHAR(100),
        "req_method": types.VARCHAR(20),
        "req_json_data": types.JSON,
        "req_args": types.JSON,
        "res_status_code": types.NUMERIC,
        # "resp_content": types.VARCHAR(100),
        "res_json_data": types.JSON,
    }

    try:

        msg_df.to_sql(
            "PAINT_COLORS_API_AUDIT",
            db_engine,
            index=False,
            if_exists="append",
            dtype=db_types
        )
    except Exception as e:
        logging.error(e)
        logging.warning(f"Write audit log failed.")


def get_color_by_id(color_id):

    with mysql_helper.get_tjhub_mysql_connection() as conn:
        sq = f"""
        SELECT * FROM PAINT_COLORS
        WHERE code = '{str(color_id)}'
        """
        df = mysql_helper.execute_sql(conn, sq)

    return {
        "headers": df.columns.values.tolist(),
        "data": df.values.tolist()
    }


def get_all_paint_colors_df():
    with mysql_helper.get_tjhub_mysql_connection() as conn:
        sq = f"""
        SELECT * FROM PAINT_COLORS
        """
        df = mysql_helper.execute_sql(conn, sq)
    return df


def get_all_paint_colors():
    df = get_full_colors()
    return {
        "headers": df.columns.values.tolist(),
        "data": df.values.tolist()
    }


def get_full_colors():
    global paint_colors
    paint_colors = get_all_paint_colors_df()
    logging.info(f"Total {paint_colors.shape[0]} is found.")
    return paint_colors


def get_nearest_colors_by_id(color_id: str, top_k=3):
    if "paint_colors" not in globals():
        get_full_colors()

    c = paint_colors[
        (paint_colors["code"] == color_id)
    ].copy()

    if c.empty:
        r_msg = {
            "message": "Color Not Found."
        }
    else:
        c_details = c.to_dict(orient="records")[0]
        c_rgb = (c_details["R"], c_details["G"], c_details["B"])
        c_brand = c_details["brand"]
        target_paint_colors = paint_colors[
            paint_colors["brand"] != c_brand
        ].reset_index(drop=True)
        if top_k > target_paint_colors.shape[0]:
            top_k = target_paint_colors.shape[0]

        target_paint_colors["cdist"] = target_paint_colors.apply(
            lambda x: color_util.get_rgb_distance(c_rgb, (x["R"], x["G"], x["B"])), axis=1
        )

        nn_colors = target_paint_colors.iloc[
            target_paint_colors["cdist"].nsmallest(top_k).index
        ].sort_values(by=["cdist"])

        r_msg = {
            "query_color": c_details,
            "nearest_colors": nn_colors.to_dict(orient="records")
        }

    return r_msg


def get_nearest_colors_by_rgb(r, g, b, top_k=3):
    if "paint_colors" not in globals():
        get_full_colors()

    c_rgb = (r, g, b)
    target_paint_colors = paint_colors.reset_index(drop=True)
    if top_k > target_paint_colors.shape[0]:
        top_k = target_paint_colors.shape[0]

    target_paint_colors["cdist"] = target_paint_colors.apply(
        lambda x: color_util.get_rgb_distance(c_rgb, (x["R"], x["G"], x["B"])), axis=1
    )

    nn_colors = target_paint_colors.iloc[
        target_paint_colors["cdist"].nsmallest(top_k).index
    ].sort_values(by=["cdist"])

    r_msg = {
        "query_color": {"R": r, "G": g, "B": b},
        "nearest_colors": nn_colors.to_dict(orient="records")
    }

    return r_msg
