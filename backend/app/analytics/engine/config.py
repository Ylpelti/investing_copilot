from dataclasses import dataclass

@dataclass(frozen=True)
class EngineConfig:
    periods_per_year: int = 252
    rf_annual: float = 0.02
    rolling_vol_window: int = 21
    rolling_sharpe_window: int = 61
