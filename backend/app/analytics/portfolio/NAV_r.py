import pandas as pd

def build_NAV_r(MV: pd.Series, cf:pd.Series) -> pd.Series:

    NAV_r = MV + cf

    NAV_r.name = "NAV raw"

    return NAV_r