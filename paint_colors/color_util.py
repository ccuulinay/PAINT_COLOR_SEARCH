import numpy as np


def get_rgb_distance(c1, c2):
    d = np.sqrt(((c2[0] - c1[0]) * 0.3) ** 2 + ((c2[1] - c1[1]) * 0.59) ** 2 + ((c2[2] - c1[2]) * 0.11) ** 2)
    return d


def get_n_nearest_color_by_rgb(c, mapping_df, topN=1):
    ops_df = mapping_df.copy()
    ops_df["d"] = ops_df.apply(lambda x: get_rgb_distance(c, (x["R"], x["G"], x["B"])), axis=1)
    # print(ops_df.shape)
    r_df = ops_df.iloc[ops_df["d"].nsmallest(topN).index].copy()
    return r_df
