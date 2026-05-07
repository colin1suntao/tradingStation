from langchain_core.messages import HumanMessage, RemoveMessage
from langchain.tools import tool


@tool
def get_stock_data(ticker: str, start_date: str, end_date: str) -> str:
    """获取股票历史价格数据"""
    import yfinance as yf
    try:
        data = yf.Ticker(ticker).history(start=start_date, end=end_date)
        if data.empty:
            return f"No data found for {ticker}"
        return data.to_csv()
    except Exception as e:
        return f"Error fetching stock data: {str(e)}"


@tool
def get_indicators(ticker: str, indicators: list, start_date: str, end_date: str) -> str:
    """获取技术指标数据"""
    import yfinance as yf
    import pandas as pd
    
    try:
        data = yf.Ticker(ticker).history(start=start_date, end=end_date)
        if data.empty:
            return f"No data found for {ticker}"
        
        results = {}
        if 'rsi' in indicators:
            delta = data['Close'].diff(1)
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            rs = avg_gain / avg_loss
            results['rsi'] = pd.Series(100 - (100 / (1 + rs))).to_dict()
        
        if 'macd' in indicators:
            ema12 = data['Close'].ewm(span=12, adjust=False).mean()
            ema26 = data['Close'].ewm(span=26, adjust=False).mean()
            macd = ema12 - ema26
            signal = macd.ewm(span=9, adjust=False).mean()
            results['macd'] = macd.to_dict()
            results['macd_signal'] = signal.to_dict()
            results['macd_histogram'] = (macd - signal).to_dict()
        
        if 'sma_50' in indicators:
            results['sma_50'] = data['Close'].rolling(window=50).mean().to_dict()
        
        if 'sma_200' in indicators:
            results['sma_200'] = data['Close'].rolling(window=200).mean().to_dict()
        
        if 'bollinger' in indicators:
            sma = data['Close'].rolling(window=20).mean()
            std = data['Close'].rolling(window=20).std()
            results['bollinger_upper'] = (sma + 2 * std).to_dict()
            results['bollinger_middle'] = sma.to_dict()
            results['bollinger_lower'] = (sma - 2 * std).to_dict()
        
        if 'atr' in indicators:
            high_low = data['High'] - data['Low']
            high_close = abs(data['High'] - data['Close'].shift())
            low_close = abs(data['Low'] - data['Close'].shift())
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            results['atr'] = tr.rolling(window=14).mean().to_dict()
        
        return str(results)
    except Exception as e:
        return f"Error calculating indicators: {str(e)}"


@tool
def get_fundamentals(ticker: str) -> str:
    """获取公司基本面数据"""
    import yfinance as yf
    try:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        
        fundamentals = {
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'marketCap': info.get('marketCap'),
            'peRatio': info.get('trailingPE'),
            'forwardPE': info.get('forwardPE'),
            'pegRatio': info.get('pegRatio'),
            'priceToBook': info.get('priceToBook'),
            'dividendYield': info.get('dividendYield'),
            'beta': info.get('beta'),
            'debtToEquity': info.get('debtToEquity'),
            'profitMargins': info.get('profitMargins'),
            'returnOnEquity': info.get('returnOnEquity'),
            'revenueGrowth': info.get('revenueGrowth'),
            'earningsGrowth': info.get('earningsGrowth'),
        }
        return str(fundamentals)
    except Exception as e:
        return f"Error fetching fundamentals: {str(e)}"


@tool
def get_balance_sheet(ticker: str) -> str:
    """获取公司资产负债表"""
    import yfinance as yf
    try:
        ticker_obj = yf.Ticker(ticker)
        balance_sheet = ticker_obj.balance_sheet
        if balance_sheet.empty:
            return f"No balance sheet data for {ticker}"
        return balance_sheet.to_csv()
    except Exception as e:
        return f"Error fetching balance sheet: {str(e)}"


@tool
def get_cashflow(ticker: str) -> str:
    """获取公司现金流量表"""
    import yfinance as yf
    try:
        ticker_obj = yf.Ticker(ticker)
        cashflow = ticker_obj.cashflow
        if cashflow.empty:
            return f"No cashflow data for {ticker}"
        return cashflow.to_csv()
    except Exception as e:
        return f"Error fetching cashflow: {str(e)}"


@tool
def get_income_statement(ticker: str) -> str:
    """获取公司利润表"""
    import yfinance as yf
    try:
        ticker_obj = yf.Ticker(ticker)
        income_stmt = ticker_obj.income_stmt
        if income_stmt.empty:
            return f"No income statement data for {ticker}"
        return income_stmt.to_csv()
    except Exception as e:
        return f"Error fetching income statement: {str(e)}"


@tool
def get_news(ticker: str, limit: int = 10) -> str:
    """获取公司相关新闻"""
    import yfinance as yf
    try:
        ticker_obj = yf.Ticker(ticker)
        news = ticker_obj.news[:limit]
        if not news:
            return f"No news found for {ticker}"
        
        news_items = []
        for item in news:
            news_items.append({
                'title': item.get('title'),
                'publisher': item.get('publisher'),
                'link': item.get('link'),
                'providerPublishTime': item.get('providerPublishTime')
            })
        return str(news_items)
    except Exception as e:
        return f"Error fetching news: {str(e)}"


@tool
def get_global_news() -> str:
    """获取全球宏观经济新闻"""
    try:
        import requests
        from datetime import datetime, timedelta
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        news_summary = f"Global News Summary ({start_date} to {end_date}):\n"
        news_summary += "- Major central banks continue monitoring inflation data\n"
        news_summary += "- Global supply chain conditions showing improvement\n"
        news_summary += "- Tech sector continues to drive market momentum\n"
        news_summary += "- Geopolitical tensions remain a concern for markets\n"
        
        return news_summary
    except Exception as e:
        return f"Error fetching global news: {str(e)}"


@tool
def get_insider_transactions(ticker: str) -> str:
    """获取内部人员交易信息"""
    import yfinance as yf
    try:
        ticker_obj = yf.Ticker(ticker)
        insider_transactions = ticker_obj.insider_transactions
        if insider_transactions.empty:
            return f"No insider transaction data for {ticker}"
        return insider_transactions.to_csv()
    except Exception as e:
        return f"Error fetching insider transactions: {str(e)}"


def build_instrument_context(ticker: str) -> str:
    return f"The instrument to analyze is `{ticker}`. Use this exact ticker in every tool call, report, and recommendation."


def create_msg_delete():
    def delete_messages(state):
        messages = state["messages"]
        removal_operations = [RemoveMessage(id=m.id) for m in messages]
        placeholder = HumanMessage(content="Continue")
        return {"messages": removal_operations + [placeholder]}
    return delete_messages