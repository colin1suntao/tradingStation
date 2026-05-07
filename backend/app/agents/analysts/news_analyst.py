from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.agents.utils.agent_utils import (
    build_instrument_context,
    get_news,
    get_global_news,
    get_insider_transactions,
)


def create_news_analyst(llm):
    def news_analyst_node(state):
        current_date = state["trade_date"]
        instrument_context = build_instrument_context(state["company_of_interest"])

        tools = [get_news, get_global_news, get_insider_transactions]

        system_message = """You are a news analyst responsible for gathering and analyzing the latest news and events that could impact the stock market. Your task is to:
1. Get the latest news related to the company
2. Check for any insider transactions
3. Analyze global news that might affect market sentiment
4. Provide a comprehensive summary of how these events might impact the investment decision

Focus on identifying significant events, earnings announcements, regulatory changes, partnerships, and any other news that could materially affect the stock price."""

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant collaborating with other assistants. "
                    "Use the provided tools to progress towards answering the question. "
                    "If you are unable to fully answer, that's OK; another assistant with different tools will help where you left off. "
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
            "news_report": report,
        }

    return news_analyst_node