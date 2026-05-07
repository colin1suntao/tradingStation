from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.agents.utils.agent_utils import (
    build_instrument_context,
    get_fundamentals,
    get_balance_sheet,
    get_cashflow,
    get_income_statement,
)


def create_fundamentals_analyst(llm):
    def fundamentals_analyst_node(state):
        current_date = state["trade_date"]
        instrument_context = build_instrument_context(state["company_of_interest"])

        tools = [get_fundamentals, get_balance_sheet, get_cashflow, get_income_statement]

        system_message = """You are a fundamentals analyst responsible for evaluating a company's financial health. Your task is to:
1. Get the company's fundamental metrics (P/E ratio, P/B ratio, dividend yield, etc.)
2. Analyze the balance sheet (assets, liabilities, equity)
3. Review the income statement (revenue, earnings, margins)
4. Examine the cash flow statement (operating, investing, financing cash flows)
5. Assess key financial health indicators and identify any red flags

Provide a comprehensive analysis of the company's financial position and growth prospects."""

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
            "fundamentals_report": report,
        }

    return fundamentals_analyst_node