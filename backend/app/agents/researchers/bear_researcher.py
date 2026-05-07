def create_bear_researcher(llm):
    def bear_node(state) -> dict:
        investment_debate_state = state["investment_debate_state"]
        history = investment_debate_state.get("history", "")
        bear_history = investment_debate_state.get("bear_history", "")
        current_response = investment_debate_state.get("current_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        prompt = f"""You are a Bear Analyst advocating against investing in the stock. Your task is to build a strong, evidence-based case emphasizing risks, weaknesses, and negative market indicators.

Key points to focus on:
- Potential Risks: Highlight market risks, competitive threats, and economic headwinds
- Valuation Concerns: Identify overvaluation based on P/E ratios, market cap, and industry comparisons
- Negative Indicators: Use declining fundamentals, negative news, and bearish sentiment as evidence
- Bull Counterpoints: Critically analyze the bull argument with specific data and sound reasoning

Resources available:
Market research report: {market_research_report}
Social media sentiment report: {sentiment_report}
Latest news: {news_report}
Company fundamentals report: {fundamentals_report}
Conversation history: {history}
Last bull argument: {current_response}

Deliver a compelling bear argument that directly addresses any bull concerns."""

        response = llm.invoke(prompt)
        argument = f"Bear Analyst: {response.content}"

        new_investment_debate_state = {
            "history": history + "\n" + argument,
            "bull_history": investment_debate_state.get("bull_history", ""),
            "bear_history": bear_history + "\n" + argument,
            "current_response": argument,
            "count": investment_debate_state["count"] + 1,
        }

        return {"investment_debate_state": new_investment_debate_state}

    return bear_node