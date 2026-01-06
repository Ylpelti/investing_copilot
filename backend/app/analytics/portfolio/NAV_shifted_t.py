import pandas as pd

def build_NAV_shifted_t(MV: pd.Series, NAV_r: pd.Series):
    offset = MV.iloc[0] - NAV_r.iloc[0]
    NAV_shifted_t = NAV_r + offset

    NAV_shifted_t.name = "NAV shifted"

    return NAV_shifted_t