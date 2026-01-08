from app.ai.context.base_context_builder import BaseContext
from typing import Dict, Any

class PortfolioContextBuilder(BaseContext):

    def build(self, analytic_result: Dict[str, Any]):
        nav = analytic_result["data"]["NAV"]
        returns = analytic_result["returns"]["simple return"]

        return {
            "start_value": float(nav.iloc[0]),
            "end_value": float(nav.iloc[-1]),
            "total_return": float((nav.iloc[-1] / nav.iloc[0]) - 1),
            "max_drawdown": float(
                analytic_result["risk"]["max drawdown"]
            ),
            "volatility": float(
                analytic_result["risk"]["volatility"]
            ),
            "sharpe_ratio": float(analytic_result["risk"]["sharpe ratio"]),
            "period_days": int(len(nav)),
        }