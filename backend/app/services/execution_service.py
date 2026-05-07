from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

from app.services.trading_agents_service import TradingAgentsGraph
from app.risk.risk_manager import risk_manager, RiskCalculator
from app.trading.trading_service import trading_service
from app.trading.exchange_manager import exchange_manager
from app.schemas.trading import OrderSide, OrderType
from app.schemas.risk import PositionSide, RiskCheckRequest


class AgentExecutionService:
    def __init__(self):
        self.execution_history: List[Dict[str, Any]] = []

    def analyze_and_execute(
        self,
        ticker: str,
        trade_date: str,
        action: str,
        llm_provider: str = "openai",
        deep_think_model: str = "gpt-4o",
        quick_think_model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        risk_check: bool = True,
        auto_trade: bool = False,
        exchange_name: str = "default",
    ) -> Dict[str, Any]:
        execution_id = str(uuid.uuid4())
        
        ta = TradingAgentsGraph(
            llm_provider=llm_provider,
            deep_think_model=deep_think_model,
            quick_think_model=quick_think_model,
            api_key=api_key,
        )
        
        final_state, decision = ta.propagate(ticker, trade_date)
        
        parsed_action = self._parse_decision(decision, action)
        
        result = {
            "execution_id": execution_id,
            "ticker": ticker,
            "trade_date": trade_date,
            "decision": decision,
            "parsed_action": parsed_action,
            "analysis": {
                "market_report": final_state.get("market_report", ""),
                "news_report": final_state.get("news_report", ""),
                "fundamentals_report": final_state.get("fundamentals_report", ""),
                "sentiment_report": final_state.get("sentiment_report", ""),
                "investment_plan": final_state.get("investment_plan", ""),
                "bull_history": final_state.get("investment_debate_state", {}).get("bull_history", ""),
                "bear_history": final_state.get("investment_debate_state", {}).get("bear_history", ""),
            },
            "risk_check": None,
            "execution": None,
            "timestamp": datetime.now(),
        }
        
        if risk_check:
            quantity = 0.1
            entry_price = 0
            
            exchange = exchange_manager.get_exchange(exchange_name)
            if exchange:
                try:
                    ticker_data = exchange.fetch_ticker(ticker)
                    entry_price = ticker_data.get("last", 0)
                except Exception:
                    pass
            
            risk_check_request = RiskCheckRequest(
                symbol=ticker,
                side=PositionSide.LONG if parsed_action["side"] == "long" else PositionSide.SHORT,
                quantity=quantity,
                entry_price=entry_price,
                stop_loss_price=parsed_action.get("stop_loss"),
                take_profit_price=parsed_action.get("take_profit"),
            )
            
            risk_result = risk_manager.check_risk(risk_check_request)
            result["risk_check"] = risk_result.model_dump()
            
            if not risk_result.approved and auto_trade:
                result["execution"] = {
                    "success": False,
                    "error": f"Risk check failed: {'; '.join(risk_result.reasons)}",
                }
                self.execution_history.append(result)
                return result
        
        if auto_trade and (result.get("risk_check") is None or result["risk_check"].get("approved", False)):
            if parsed_action["action"] in ["buy", "sell"]:
                side = OrderSide.BUY if parsed_action["action"] == "buy" else OrderSide.SELL
                
                entry_price = 0
                exchange = exchange_manager.get_exchange(exchange_name)
                if exchange:
                    try:
                        ticker_data = exchange.fetch_ticker(ticker)
                        entry_price = ticker_data.get("last", 0)
                    except Exception:
                        pass
                
                position_result = RiskCalculator.calculate_position_size(
                    PositionSizeRequest(
                        account_balance=100000,
                        entry_price=entry_price or 100,
                        stop_loss_price=parsed_action.get("stop_loss", entry_price * 0.98 if entry_price else 98),
                        risk_pct=0.01,
                    )
                )
                
                exec_result = trading_service.place_order_with_protection(
                    symbol=ticker,
                    side=side,
                    quantity=position_result.quantity,
                    entry_price=entry_price,
                    stop_loss_pct=0.02,
                    take_profit_pct=0.05,
                    exchange_name=exchange_name,
                    risk_check=False,
                )
                
                result["execution"] = exec_result
                result["position_size"] = position_result.model_dump()
        
        self.execution_history.append(result)
        return result

    def _parse_decision(self, decision: str, action: str) -> Dict[str, Any]:
        action_lower = action.lower()
        
        if action_lower in ["buy", "long", "overweight"]:
            parsed = {
                "action": "buy",
                "side": "long",
                "confidence": self._extract_confidence(decision),
            }
        elif action_lower in ["sell", "short", "underweight"]:
            parsed = {
                "action": "sell",
                "side": "short",
                "confidence": self._extract_confidence(decision),
            }
        else:
            parsed = {
                "action": "hold",
                "side": "neutral",
                "confidence": 0.5,
            }
        
        if "stop loss" in decision.lower():
            sl_idx = decision.lower().find("stop loss")
            try:
                sl_part = decision[sl_idx:sl_idx+30]
                sl_price = float(''.join(filter(lambda x: x.isdigit() or x == '.', sl_part.split()[2:4] if len(sl_part.split()) > 2 else "0")))
                if sl_price > 0:
                    parsed["stop_loss"] = sl_price
            except Exception:
                pass
        
        if "take profit" in decision.lower() or "target" in decision.lower():
            tp_idx = decision.lower().find("take profit")
            if tp_idx == -1:
                tp_idx = decision.lower().find("target")
            if tp_idx != -1:
                try:
                    tp_part = decision[tp_idx:tp_idx+30]
                    tp_price = float(''.join(filter(lambda x: x.isdigit() or x == '.', tp_part.split()[2:4] if len(tp_part.split()) > 2 else "0")))
                    if tp_price > 0:
                        parsed["take_profit"] = tp_price
                except Exception:
                    pass
        
        return parsed

    def _extract_confidence(self, decision: str) -> float:
        if "strong buy" in decision.lower():
            return 0.95
        elif "buy" in decision.lower() and "overweight" in decision.lower():
            return 0.85
        elif "overweight" in decision.lower():
            return 0.75
        elif "hold" in decision.lower():
            return 0.5
        elif "underweight" in decision.lower():
            return 0.3
        elif "sell" in decision.lower() or "strong sell" in decision.lower():
            return 0.15
        return 0.5

    def get_execution_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.execution_history[-limit:]

    def get_performance_summary(self) -> Dict[str, Any]:
        if not self.execution_history:
            return {
                "total_executions": 0,
                "successful": 0,
                "failed": 0,
                "pending": 0,
            }
        
        successful = sum(1 for e in self.execution_history if e.get("execution", {}).get("success", False))
        failed = sum(1 for e in self.execution_history if e.get("execution", {}).get("success") == False)
        
        return {
            "total_executions": len(self.execution_history),
            "successful": successful,
            "failed": failed,
            "pending": len(self.execution_history) - successful - failed,
            "success_rate": successful / len(self.execution_history) if self.execution_history else 0,
        }


agent_execution_service = AgentExecutionService()
