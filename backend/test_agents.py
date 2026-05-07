import sys
sys.path.insert(0, '/workspace/backend')

from app.graph.trading_graph import TradingAgentsGraph
from app.default_config import DEFAULT_CONFIG

def test_trading_agents():
    config = DEFAULT_CONFIG.copy()
    config["max_debate_rounds"] = 1
    config["max_risk_discuss_rounds"] = 1

    ta = TradingAgentsGraph(debug=True, config=config)
    
    print("Testing TradingAgentsGraph with AAPL (using Mock LLM)...")
    final_state, decision = ta.propagate("AAPL", "2024-01-15")
    
    print("\n=== Final Decision ===")
    print(decision)
    
    print("\n=== Full State Summary ===")
    print(f"Company: {final_state['company_of_interest']}")
    print(f"Date: {final_state['trade_date']}")
    print(f"Market Report: {final_state['market_report'][:200]}..." if final_state['market_report'] else "No market report")
    print(f"News Report: {final_state['news_report'][:200]}..." if final_state['news_report'] else "No news report")
    print(f"Sentiment Report: {final_state['sentiment_report'][:200]}..." if final_state['sentiment_report'] else "No sentiment report")
    print(f"Fundamentals Report: {final_state['fundamentals_report'][:200]}..." if final_state['fundamentals_report'] else "No fundamentals report")
    print(f"Investment Plan: {final_state['investment_plan'][:200]}..." if final_state['investment_plan'] else "No investment plan")
    print(f"Trader Plan: {final_state['trader_investment_plan'][:200]}..." if final_state['trader_investment_plan'] else "No trader plan")

if __name__ == "__main__":
    test_trading_agents()