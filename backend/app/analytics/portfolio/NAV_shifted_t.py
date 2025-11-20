import pandas as pd

def build_NAV_shifted_t(MV: pd.Series, NAV_r: pd.Series):
    NAV_shifted_t = NAV_r + MV[0]
    return NAV_shifted_t