from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.agents.utils.agent_utils import (
    build_instrument_context,
    get_indicators,
    get_stock_data,
)


def create_market_analyst(llm):
    def market_analyst_node(state):
        current_date = state["trade_date"]
        instrument_context = build_instrument_context(state["company_of_interest"])

        tools = [get_stock_data, get_indicators]

        system_message = """You are a trading assistant tasked with analyzing financial markets. Your role is to select the most relevant indicators for a given market condition or trading strategy. Focus on up to 5-8 indicators that provide complementary insights.

Moving Averages:
- sma_50: 50-day SMA - medium-term trend indicator
- sma_200: 200-day SMA - long-term trend benchmark

MACD Related:
- macd: MACD line - momentum indicator
- macd_signal: MACD signal line
- macd_histogram: MACD histogram

Momentum Indicators:
- rsi: RSI - overbought/oversold conditions

Volatility Indicators:
- bollinger: Bollinger Bands
- atr: ATR - average true range

Select indicators that provide diverse and complementary information. First call get_stock_data to retrieve historical data, then use get_indicators with specific indicator names. Write a detailed report of the trends you observe with supporting evidence."""

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant collaborating with other assistants. "
                    "Use the provided tools to progress towards answering the question. "
                    "If you are unable to fully answer, that's OK; another assistant with different tools will help where you left off. "
                    "If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL**, prefix your response with FINAL TRANSACTION PROPOSAL. "
                    "You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. {instrument_context}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(instrument_context=instrument_context)

        chain = prompt | llm.bind_tools(tools)
        result = chain.invoke(state["messages"])

        report = ""
        if len(result.tool_calls) == 0:
            report = result.content

        return {
            "messages": [result],
            "market_report": report,
        }

    return market_analyst_node