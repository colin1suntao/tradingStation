from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.agents.utils.agent_utils import (
    build_instrument_context,
    get_news,
)


def create_social_media_analyst(llm):
    def social_media_analyst_node(state):
        current_date = state["trade_date"]
        instrument_context = build_instrument_context(state["company_of_interest"])

        tools = [get_news]

        system_message = """You are a social media and sentiment analyst. Your role is to analyze market sentiment and social media buzz around the target company. Focus on:
1. Overall sentiment (positive, negative, neutral)
2. Key themes and topics being discussed
3. Influencer opinions
4. Volume of discussion
5. Any viral trends or significant social media events

Provide insights on how market sentiment might impact the stock's future performance."""

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
            "sentiment_report": report,
        }

    return social_media_analyst_node