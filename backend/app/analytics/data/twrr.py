import pandas as pd
import numpy as np

def build_twrr_series(tx_df: pd.DataFrame, V:pd.Series):
    
    dates = V.index

    tx_dates = (
        tx_df["date"]
        .dt.normalize()
        .sort_values()
        .unique()
    )

    print("TX_date", tx_dates[0])
    
    if len(tx_dates) == 0:
        return float((V.iloc[-1] / V.iloc[0]) - 1)
    

    
    all_breaks = list(tx_dates) + [dates[-1]]
    print(all_breaks)
    subperiods = []

    for i in range(len(all_breaks) - 1):
        end_candidate = dates[dates < all_breaks[i + 1]]
        
        end = end_candidate[-1]
        start = all_breaks[i]

        print("Times \n")

        print(f"start {start} \n end: {end}")

        subperiods.append((start, end))

    subperiod_returns = []

    for (start, end) in subperiods:
        Vs = V[start:end]

        
        V_start = Vs.iloc[0]
        V_end = Vs.iloc[-1]


        R_i = (V_end / V_start) -1 
        print(R_i)
        subperiod_returns.append(R_i)

    