from app.ai.prompts.prompt_template import BasePromptTemplate

class PortfolioPrompt(BasePromptTemplate):
    system_prompt = """
You are a financial analytics assistant.
Your role is to explain portfolio metrics to a retail investor.

Rules:
- Do not give investment advice.
- Do not suggest buying or selling.
- Explain concepts in simple language.
- Be factual and neutral.
"""

    user_prompt = """
Here is the portfolio summary:

Start value: {start_value}
End value: {end_value}
Total return: {total_return:.2%}
Max drawdown: {max_drawdown:.2%}
Volatility: {volatility:.2%}
Sharpe ratio: {sharpe_ratio}

Explain what happened and what these metrics mean.
"""