#!/usr/bin#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.pr#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': '#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self,#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) <#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma =#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal':#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma >#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': '#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time,#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == '#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price =#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] *#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0,#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price =#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume =#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            '#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀 组合回测演示 - 多策略多资产")
    print("=" * 70)
    
    # 配置参数
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀 组合回测演示 - 多策略多资产")
    print("=" * 70)
    
    # 配置参数
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)
    
    symbols = ['BTC/US#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀 组合回测演示 - 多策略多资产")
    print("=" * 70)
    
    # 配置参数
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    print(f"#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀 组合回测演示 - 多策略多资产")
    print("=" * 70)
    
    # 配置参数
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    print(f"\n📊 回测配置:")
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀 组合回测演示 - 多策略多资产")
    print("=" * 70)
    
    # 配置参数
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    print(f"\n📊 回测配置:")
    print(f"   时间范围: {#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀 组合回测演示 - 多策略多资产")
    print("=" * 70)
    
    # 配置参数
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    print(f"\n📊 回测配置:")
    print(f"   时间范围: {start_time.date()} 至 {end_time.date()}")
    print(f"#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀 组合回测演示 - 多策略多资产")
    print("=" * 70)
    
    # 配置参数
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    print(f"\n📊 回测配置:")
    print(f"   时间范围: {start_time.date()} 至 {end_time.date()}")
    print(f"   交易标的: {', '.join(symbols)}")
    print(f"   初始资金#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀 组合回测演示 - 多策略多资产")
    print("=" * 70)
    
    # 配置参数
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    print(f"\n📊 回测配置:")
    print(f"   时间范围: {start_time.date()} 至 {end_time.date()}")
    print(f"   交易标的: {', '.join(symbols)}")
    print(f"   初始资金: $100,000")
    print(f"   策略数量: 3")
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀 组合回测演示 - 多策略多资产")
    print("=" * 70)
    
    # 配置参数
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    print(f"\n📊 回测配置:")
    print(f"   时间范围: {start_time.date()} 至 {end_time.date()}")
    print(f"   交易标的: {', '.join(symbols)}")
    print(f"   初始资金: $100,000")
    print(f"   策略数量: 3")
    
    # 生成模拟数据
    print(f"\n📈 生成市场数据...")
    data = {}
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀 组合回测演示 - 多策略多资产")
    print("=" * 70)
    
    # 配置参数
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    print(f"\n📊 回测配置:")
    print(f"   时间范围: {start_time.date()} 至 {end_time.date()}")
    print(f"   交易标的: {', '.join(symbols)}")
    print(f"   初始资金: $100,000")
    print(f"   策略数量: 3")
    
    # 生成模拟数据
    print(f"\n📈 生成市场数据...")
    data = {}
    trends = ['up', 'down', 'sid#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀 组合回测演示 - 多策略多资产")
    print("=" * 70)
    
    # 配置参数
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    print(f"\n📊 回测配置:")
    print(f"   时间范围: {start_time.date()} 至 {end_time.date()}")
    print(f"   交易标的: {', '.join(symbols)}")
    print(f"   初始资金: $100,000")
    print(f"   策略数量: 3")
    
    # 生成模拟数据
    print(f"\n📈 生成市场数据...")
    data = {}
    trends = ['up', 'down', 'sideways']
    for i, symbol in enumerate(symbols):
        data[symbol] = generate_mock_data(symbol, start_time, end_time#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀 组合回测演示 - 多策略多资产")
    print("=" * 70)
    
    # 配置参数
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    print(f"\n📊 回测配置:")
    print(f"   时间范围: {start_time.date()} 至 {end_time.date()}")
    print(f"   交易标的: {', '.join(symbols)}")
    print(f"   初始资金: $100,000")
    print(f"   策略数量: 3")
    
    # 生成模拟数据
    print(f"\n📈 生成市场数据...")
    data = {}
    trends = ['up', 'down', 'sideways']
    for i, symbol in enumerate(symbols):
        data[symbol] = generate_mock_data(symbol, start_time, end_time, trends[i % len(trends)])
#!/usr/bin/env python3
"""
组合回测演示 - 独立版本
"""
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 直接导入引擎
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

def generate_mock_data(symbol, start_time, end_time, trend='up'):
    """生成模拟数据"""
    dates = pd.date_range(start=start_time, end=end_time, freq='D')
    np.random.seed(42)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 70)
    print("🚀 组合回测演示 - 多策略多资产")
    print("=" * 70)
    
    # 配置参数
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    print(f"\n📊 回测配置:")
    print(f"   时间范围: {start_time.date()} 至 {end_time.date()}")
    print(f"   交易标的: {', '.join(symbols)}")
    print(f"   初始资金: $100,000")
    print(f"   策略数量: 3")
    
    # 生成模拟数据
    print(f"\n📈 生成市场数据...")
    data = {}
    trends = ['up', 'down', 'sideways']
    for i, symbol in enumerate(symbols):
        data[symbol] = generate_mock_data(symbol, start_time, end_time, trends[i % len(trends)])
        print(f"   {symbol}: {len