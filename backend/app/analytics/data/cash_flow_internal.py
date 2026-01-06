import pandas as pd

def build_C_t(tx_df:pd.DataFrame, prices_df:pd.DataFrame) -> pd.Series:
    s = pd.Series()
    
        
    df = tx_df.copy()
    df["trade_cash"] = (df["quantity"] * df["price"])
    df.loc[df["type"] == "BUY", "trade_cash"] *= -1

    daily_trade_cash = (df
        .groupby(df["date"].dt.normalize())["trade_cash"] # type: ignore[attr-defined]
        .sum())
    
    full_dates = prices_df.index.normalize() # type: ignore[attr-defined]

    daily_trade_cash = daily_trade_cash.reindex(full_dates, fill_value = 0)
    internal_cash_raw = daily_trade_cash.cumsum()

    internal_cash, external_cf = build_internal_and_external_flows(daily_trade_cash) #type: ignore
    internal_cash = pd.Series(internal_cash, index=full_dates)
    external_cf = pd.Series(external_cf, index=full_dates)

    print("-" * 12)
    print("daily trade cash")
    print(internal_cash_raw)

    print("-" * 12)
    print("internal cash")
    print(internal_cash)

    print("-" * 12)
    print("external cashflow")
    print(external_cf)
    
    return s

def build_internal_and_external_flows(daily_trade_cash:pd.Series):
    internal_cash = []
    external_CF = []

    cash = 0.0

    for delta in daily_trade_cash:
        print(delta)
        cash_raw = cash + delta

        if cash_raw < 0:
            external_CF.append(-cash_raw)
            cash = 0.0
        else:
            external_CF.append(0.0)
            cash = cash_raw

        internal_cash.append(cash)

        

    return internal_cash, external_CF