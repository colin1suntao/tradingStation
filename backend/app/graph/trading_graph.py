import logging
import os
from pathlib import Path
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, List, Optional

import yfinance as yf

logger = logging.getLogger(__name__)

from langgraph.prebuilt import ToolNode

from app.agents import *
from app.default_config import DEFAULT_CONFIG
from app.agents.utils.agent_utils import (
    get_stock_data,
    get_indicators,
    get_fundamentals,
    get_balance_sheet,
    get_cashflow,
    get_income_statement,
    get_news,
    get_insider_transactions,
    get_global_news
)
from app.agents.utils.agent_states import AgentState

from .setup import GraphSetup
from .conditional_logic import ConditionalLogic
from .propagation import Propagator


class TradingAgentsGraph:
    def __init__(
        self,
        selected_analysts=["market", "social", "news", "fundamentals"],
        debug=False,
        config: Dict[str, Any] = None,
        callbacks: Optional[List] = None,
    ):
        self.debug = debug
        self.config = config or DEFAULT_CONFIG
        self.callbacks = callbacks or []

        os.makedirs(self.config["data_cache_dir"], exist_ok=True)
        os.makedirs(self.config["results_dir"], exist_ok=True)

        self._init_llms()

        self.tool_nodes = self._create_tool_nodes()

        self.conditional_logic = ConditionalLogic(
            max_debate_rounds=self.config["max_debate_rounds"],
            max_risk_discuss_rounds=self.config["max_risk_discuss_rounds"],
        )
        self.graph_setup = GraphSetup(
            self.quick_thinking_llm,
            self.deep_thinking_llm,
            self.tool_nodes,
            self.conditional_logic,
        )

        self.propagator = Propagator()
        self.curr_state = None
        self.ticker = None
        self.log_states_dict = {}

        self.workflow = self.graph_setup.setup_graph(selected_analysts)
        self.graph = self.workflow.compile()

    def _init_llms(self):
        try:
            from langchain_openai import ChatOpenAI
            from openai import OpenAIError
            try:
                self.deep_thinking_llm = ChatOpenAI(
                    model=self.config["deep_think_llm"],
                    temperature=0.1
                )
                self.quick_thinking_llm = ChatOpenAI(
                    model=self.config["quick_think_llm"],
                    temperature=0.3
                )
                print("Using OpenAI LLMs")
            except (OpenAIError, ValueError):
                raise ImportError("OpenAI credentials not available")
        except ImportError:
            from langchain_core.messages import AIMessage
            from langchain_core.runnables import Runnable
            
            class MockAIMessage(AIMessage):
                def __init__(self, content):
                    super().__init__(content=content)
                    self.tool_calls = []
            
            class MockLLM(Runnable):
                def invoke(self, input, config=None):
                    if isinstance(input, list):
                        content = "\n".join(str(m) for m in input)
                    else:
                        content = str(input)
                    return MockAIMessage(content=f"Mock response for: {content[:100]}...")
                
                def bind_tools(self, tools):
                    return self
                
                def stream(self, input, config=None):
                    result = self.invoke(input, config)
                    yield result
            
            self.deep_thinking_llm = MockLLM()
            self.quick_thinking_llm = MockLLM()
            print("Using Mock LLM (no OpenAI credentials)")

    def _create_tool_nodes(self) -> Dict[str, ToolNode]:
        return {
            "market": ToolNode([get_stock_data, get_indicators]),
            "social": ToolNode([get_news]),
            "news": ToolNode([get_news, get_global_news, get_insider_transactions]),
            "fundamentals": ToolNode([get_fundamentals, get_balance_sheet, get_cashflow, get_income_statement]),
        }

    def propagate(self, company_name, trade_date):
        self.ticker = company_name
        return self._run_graph(company_name, trade_date)

    def _run_graph(self, company_name, trade_date):
        init_agent_state = self.propagator.create_initial_state(company_name, trade_date)
        args = self.propagator.get_graph_args()

        if self.debug:
            trace = []
            for chunk in self.graph.stream(init_agent_state, **args):
                if len(chunk["messages"]) > 0:
                    chunk["messages"][-1].pretty_print()
                    trace.append(chunk)
            final_state = trace[-1]
        else:
            final_state = self.graph.invoke(init_agent_state, **args)

        self.curr_state = final_state
        self._log_state(trade_date, final_state)

        return final_state, final_state.get("final_trade_decision", "")

    def _log_state(self, trade_date, final_state):
        self.log_states_dict[str(trade_date)] = {
            "company_of_interest": final_state["company_of_interest"],
            "trade_date": final_state["trade_date"],
            "market_report": final_state["market_report"],
            "sentiment_report": final_state["sentiment_report"],
            "news_report": final_state["news_report"],
            "fundamentals_report": final_state["fundamentals_report"],
            "investment_debate_state": {
                "bull_history": final_state["investment_debate_state"]["bull_history"],
                "bear_history": final_state["investment_debate_state"]["bear_history"],
                "history": final_state["investment_debate_state"]["history"],
                "current_response": final_state["investment_debate_state"]["current_response"],
                "judge_decision": final_state["investment_debate_state"]["judge_decision"],
            },
            "trader_investment_plan": final_state["trader_investment_plan"],
            "risk_debate_state": {
                "aggressive_history": final_state["risk_debate_state"]["aggressive_history"],
                "conservative_history": final_state["risk_debate_state"]["conservative_history"],
                "neutral_history": final_state["risk_debate_state"]["neutral_history"],
                "history": final_state["risk_debate_state"]["history"],
                "judge_decision": final_state["risk_debate_state"]["judge_decision"],
            },
            "investment_plan": final_state["investment_plan"],
            "final_trade_decision": final_state["final_trade_decision"],
        }

        safe_ticker = self.ticker.replace('/', '_').replace('\\', '_')
        directory = Path(self.config["results_dir"]) / safe_ticker / "TradingAgentsStrategy_logs"
        directory.mkdir(parents=True, exist_ok=True)

        log_path = directory / f"full_states_log_{trade_date}.json"
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(self.log_states_dict[str(trade_date)], f, indent=4)