// API 基础配置
const API_BASE = 'http://localhost:8001/api/v1';

// 应用状态
let state = {
    instruments: [],
    strategies: [],
    backtests: [],
    exchanges: [
        { id: 1, name: 'Binance', code: 'binance', country: 'Global' },
        { id: 2, name: 'NYSE', code: 'nyse', country: 'USA' },
        { id: 3, name: 'NASDAQ', code: 'nasdaq', country: 'USA' }
    ],
    activeSection: 'dashboard',
    currentStrategy: null,
    currentBacktest: null,
    codeEditor: null,
    equityChart: null,
    drawdownChart: null
};

// 模拟数据（用于演示）
const mockInstruments = [
    { id: 1, symbol: 'BTC/USDT', name: 'Bitcoin', exchange_id: 1, asset_class: 'crypto', instrument_type: 'spot' },
    { id: 2, symbol: 'ETH/USDT', name: 'Ethereum', exchange_id: 1, asset_class: 'crypto', instrument_type: 'spot' },
    { id: 3, symbol: 'SOL/USDT', name: 'Solana', exchange_id: 1, asset_class: 'crypto', instrument_type: 'spot' },
    { id: 4, symbol: 'AAPL', name: 'Apple Inc.', exchange_id: 3, asset_class: 'equity', instrument_type: 'spot' },
    { id: 5, symbol: 'MSFT', name: 'Microsoft', exchange_id: 3, asset_class: 'equity', instrument_type: 'spot' },
    { id: 6, symbol: 'GOOGL', name: 'Alphabet', exchange_id: 3, asset_class: 'equity', instrument_type: 'spot' },
    { id: 7, symbol: 'TSLA', name: 'Tesla', exchange_id: 3, asset_class: 'equity', instrument_type: 'spot' },
    { id: 8, symbol: 'NVDA', name: 'NVIDIA', exchange_id: 3, asset_class: 'equity', instrument_type: 'spot' }
];

// 默认策略模板
const defaultStrategyTemplate = `class Strategy:
    """
    策略模板
    必须包含以下方法：
    - __init__(self, params): 初始化
    - initialize(self, context): 策略初始化
    - on_bar(self, data): 每根K线触发
    """
    
    def __init__(self, params=None):
        self.params = params or {}
        self.name = "My Strategy"
    
    def initialize(self, context):
        """
        策略初始化
        context: 包含账户信息、持仓等
        """
        self.context = context
        print(f"策略 {self.name} 初始化完成")
    
    def on_bar(self, data):
        """
        每根K线触发
        data: 包含 open, high, low, close, volume
        返回: dict with 'signal' key ('buy', 'sell', 'hold')
        """
        close = data['close']
        
        # 简单示例：价格突破100买入，跌破95卖出
        if close > 100:
            return {'signal': 'buy'}
        elif close < 95:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
`;

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

async function initApp() {
    await checkBackendStatus();
    await loadInstruments();
    await loadStrategies();
    await loadBacktests();
    setupEventListeners();
    initCodeEditor();
    updateDashboard();
}

// 初始化代码编辑器
function initCodeEditor() {
    const textarea = document.getElementById('strategy-code-editor');
    if (textarea && typeof CodeMirror !== 'undefined') {
        state.codeEditor = CodeMirror.fromTextArea(textarea, {
            mode: 'python',
            theme: 'default',
            lineNumbers: true,
            indentUnit: 4,
            lineWrapping: true
        });
        state.codeEditor.setValue(defaultStrategyTemplate);
    }
}

// 检查后端状态
async function checkBackendStatus() {
    try {
        const response = await fetch('http://localhost:8001/health');
        const data = await response.json();
        document.getElementById('backend-status').textContent = `已连接 - ${new Date(data.timestamp).toLocaleTimeString()}`;
        document.getElementById('backend-status').className = 'text-green-500 text-sm mt-1';
    } catch (error) {
        document.getElementById('backend-status').textContent = '连接失败 - 使用模拟数据';
        document.getElementById('backend-status').className = 'text-red-500 text-sm mt-1';
    }
}

// 设置事件监听器
function setupEventListeners() {
    document.getElementById('search-instruments')?.addEventListener('input', (e) => filterInstruments(e.target.value));
    document.getElementById('filter-asset-class')?.addEventListener('change', (e) => filterInstruments(null, e.target.value));
    document.getElementById('search-strategies')?.addEventListener('input', (e) => filterStrategies(e.target.value));
    document.getElementById('filter-strategy-status')?.addEventListener('change', (e) => filterStrategies(null, e.target.value));
    document.getElementById('search-backtests')?.addEventListener('input', (e) => filterBacktests(e.target.value));
    document.getElementById('filter-backtest-status')?.addEventListener('change', (e) => filterBacktests(null, e.target.value));
}

// 显示/隐藏部分
function showSection(sectionName) {
    document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
    document.getElementById(`section-${sectionName}`).classList.remove('hidden');
    
    document.querySelectorAll('nav a').forEach(a => a.classList.remove('bg-white/20', 'font-semibold'));
    document.getElementById(`nav-${sectionName}`)?.classList.add('bg-white/20', 'font-semibold');
    
    state.activeSection = sectionName;
    
    if (sectionName === 'instruments') {
        renderInstrumentsTable();
    } else if (sectionName === 'strategies') {
        renderStrategiesTable();
    } else if (sectionName === 'backtests') {
        renderBacktestsTable();
        updateBacktestStrategySelect();
    }
}

// ==================== 策略管理 ====================

// 加载策略数据
async function loadStrategies() {
    try {
        const response = await fetch(`${API_BASE}/strategies`);
        if (response.ok) {
            state.strategies = await response.json();
        }
    } catch (error) {
        console.log('使用模拟策略数据');
        state.strategies = [];
    }
}

// 渲染策略表格
function renderStrategiesTable() {
    const tbody = document.getElementById('strategies-table-body');
    if (!tbody) return;
    
    if (state.strategies.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="px-6 py-4 text-center text-gray-500">暂无策略，点击"新建策略"创建</td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = state.strategies.map(strategy => `
        <tr class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${strategy.name}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">${strategy.code}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getAssetClassStyle(strategy.asset_class)}">
                    ${getAssetClassLabel(strategy.asset_class)}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStrategyStatusStyle(strategy.status)}">
                    ${getStrategyStatusLabel(strategy.status)}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">v${strategy.version}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm space-x-2">
                <button onclick="editStrategy(${strategy.id})" class="text-indigo-600 hover:text-indigo-900">编辑</button>
                <button onclick="deleteStrategy(${strategy.id})" class="text-red-600 hover:text-red-900">删除</button>
            </td>
        </tr>
    `).join('');
}

// 显示策略编辑器
function showStrategyEditor() {
    document.getElementById('strategy-list-view').classList.add('hidden');
    document.getElementById('strategy-editor-view').classList.remove('hidden');
    state.currentStrategy = null;
    
    // 重置表单
    document.getElementById('strategy-name').value = '';
    document.getElementById('strategy-code').value = '';
    document.getElementById('strategy-description').value = '';
    document.getElementById('strategy-asset-class').value = 'crypto';
    document.getElementById('strategy-parameters').innerHTML = `
        <div class="flex items-center space-x-2">
            <input type="text" placeholder="参数名" class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm param-name">
            <input type="text" placeholder="默认值" class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm param-value">
            <button onclick="removeParam(this)" class="text-red-500 hover:text-red-700">×</button>
        </div>
    `;
    
    if (state.codeEditor) {
        state.codeEditor.setValue(defaultStrategyTemplate);
    }
}

// 显示策略列表
function showStrategyList() {
    document.getElementById('strategy-editor-view').classList.add('hidden');
    document.getElementById('strategy-list-view').classList.remove('hidden');
    document.getElementById('validation-result').classList.add('hidden');
    state.currentStrategy = null;
}

// 添加参数
function addParam() {
    const container = document.getElementById('strategy-parameters');
    const div = document.createElement('div');
    div.className = 'flex items-center space-x-2';
    div.innerHTML = `
        <input type="text" placeholder="参数名" class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm param-name">
        <input type="text" placeholder="默认值" class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm param-value">
        <button onclick="removeParam(this)" class="text-red-500 hover:text-red-700">×</button>
    `;
    container.appendChild(div);
}

// 移除参数
function removeParam(btn) {
    btn.parentElement.remove();
}

// 验证策略代码
async function validateStrategyCode() {
    const codeContent = state.codeEditor ? state.codeEditor.getValue() : '';
    
    try {
        const response = await fetch(`${API_BASE}/strategies/validate?code_content=${encodeURIComponent(codeContent)}`);
        const result = await response.json();
        
        const resultDiv = document.getElementById('validation-result');
        const contentDiv = document.getElementById('validation-content');
        
        resultDiv.classList.remove('hidden');
        
        if (result.valid) {
            contentDiv.innerHTML = `
                <div class="flex items-center text-green-600">
                    <span class="text-xl mr-2">✅</span>
                    <span class="font-medium">代码验证通过</span>
                </div>
            `;
        } else {
            contentDiv.innerHTML = `
                <div class="flex items-center text-red-600 mb-2">
                    <span class="text-xl mr-2">❌</span>
                    <span class="font-medium">代码验证失败</span>
                </div>
                <ul class="list-disc list-inside text-sm text-red-600">
                    ${result.errors.map(e => `<li>${e}</li>`).join('')}
                </ul>
            `;
        }
    } catch (error) {
        showNotification('验证失败: ' + error.message, 'error');
    }
}

// 保存策略
async function saveStrategy() {
    const name = document.getElementById('strategy-name').value;
    const code = document.getElementById('strategy-code').value;
    const description = document.getElementById('strategy-description').value;
    const assetClass = document.getElementById('strategy-asset-class').value;
    const codeContent = state.codeEditor ? state.codeEditor.getValue() : '';
    
    // 收集参数
    const parameters = {};
    document.querySelectorAll('#strategy-parameters > div').forEach(div => {
        const nameInput = div.querySelector('.param-name');
        const valueInput = div.querySelector('.param-value');
        if (nameInput.value) {
            parameters[nameInput.value] = valueInput.value;
        }
    });
    
    if (!name || !code) {
        showNotification('请填写策略名称和代码', 'error');
        return;
    }
    
    const strategyData = {
        name,
        code,
        description,
        code_content: codeContent,
        parameters,
        asset_class: assetClass
    };
    
    try {
        let response;
        if (state.currentStrategy) {
            response = await fetch(`${API_BASE}/strategies/${state.currentStrategy.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(strategyData)
            });
        } else {
            response = await fetch(`${API_BASE}/strategies`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(strategyData)
            });
        }
        
        if (response.ok) {
            showNotification(state.currentStrategy ? '策略更新成功' : '策略创建成功', 'success');
            await loadStrategies();
            showStrategyList();
            renderStrategiesTable();
            updateDashboard();
        } else {
            const error = await response.json();
            showNotification('保存失败: ' + (error.detail || '未知错误'), 'error');
        }
    } catch (error) {
        showNotification('保存失败: ' + error.message, 'error');
    }
}

// 编辑策略
async function editStrategy(strategyId) {
    const strategy = state.strategies.find(s => s.id === strategyId);
    if (!strategy) return;
    
    state.currentStrategy = strategy;
    showStrategyEditor();
    
    document.getElementById('strategy-name').value = strategy.name;
    document.getElementById('strategy-code').value = strategy.code;
    document.getElementById('strategy-description').value = strategy.description || '';
    document.getElementById('strategy-asset-class').value = strategy.asset_class;
    
    // 设置参数
    const paramsContainer = document.getElementById('strategy-parameters');
    paramsContainer.innerHTML = '';
    Object.entries(strategy.parameters || {}).forEach(([key, value]) => {
        const div = document.createElement('div');
        div.className = 'flex items-center space-x-2';
        div.innerHTML = `
            <input type="text" value="${key}" class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm param-name">
            <input type="text" value="${value}" class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm param-value">
            <button onclick="removeParam(this)" class="text-red-500 hover:text-red-700">×</button>
        `;
        paramsContainer.appendChild(div);
    });
    
    if (state.codeEditor) {
        state.codeEditor.setValue(strategy.code_content);
    }
}

// 删除策略
async function deleteStrategy(strategyId) {
    if (!confirm('确定要删除这个策略吗？')) return;
    
    try {
        const response = await fetch(`${API_BASE}/strategies/${strategyId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showNotification('策略删除成功', 'success');
            await loadStrategies();
            renderStrategiesTable();
            updateDashboard();
        }
    } catch (error) {
        showNotification('删除失败: ' + error.message, 'error');
    }
}

// 筛选策略
function filterStrategies(searchTerm, status) {
    const search = searchTerm || document.getElementById('search-strategies')?.value?.toLowerCase() || '';
    const filter = status || document.getElementById('filter-strategy-status')?.value || '';
    
    let filtered = [...state.strategies];
    
    if (search) {
        filtered = filtered.filter(s => 
            s.name.toLowerCase().includes(search) || 
            s.code.toLowerCase().includes(search)
        );
    }
    
    if (filter) {
        filtered = filtered.filter(s => s.status === filter);
    }
    
    const tbody = document.getElementById('strategies-table-body');
    if (filtered.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="px-6 py-4 text-center text-gray-500">没有找到匹配的策略</td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = filtered.map(strategy => `
        <tr class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${strategy.name}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">${strategy.code}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getAssetClassStyle(strategy.asset_class)}">
                    ${getAssetClassLabel(strategy.asset_class)}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStrategyStatusStyle(strategy.status)}">
                    ${getStrategyStatusLabel(strategy.status)}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">v${strategy.version}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm space-x-2">
                <button onclick="editStrategy(${strategy.id})" class="text-indigo-600 hover:text-indigo-900">编辑</button>
                <button onclick="deleteStrategy(${strategy.id})" class="text-red-600 hover:text-red-900">删除</button>
            </td>
        </tr>
    `).join('');
}

// ==================== 回测管理 ====================

// 加载回测数据
async function loadBacktests() {
    try {
        const response = await fetch(`${API_BASE}/backtests`);
        if (response.ok) {
            state.backtests = await response.json();
        }
    } catch (error) {
        console.log('使用模拟回测数据');
        state.backtests = [];
    }
}

// 渲染回测表格
function renderBacktestsTable() {
    const tbody = document.getElementById('backtests-table-body');
    if (!tbody) return;
    
    if (state.backtests.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="px-6 py-4 text-center text-gray-500">暂无回测任务，点击"新建回测"创建</td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = state.backtests.map(backtest => {
        const strategy = state.strategies.find(s => s.id === backtest.strategy_id);
        return `
            <tr class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${backtest.name}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${strategy ? strategy.name : '未知'}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    ${new Date(backtest.start_time).toLocaleDateString()} - ${new Date(backtest.end_time).toLocaleDateString()}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getBacktestStatusStyle(backtest.status)}">
                        ${getBacktestStatusLabel(backtest.status)}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <div class="w-full bg-gray-200 rounded-full h-2.5">
                        <div class="bg-indigo-600 h-2.5 rounded-full" style="width: ${backtest.progress}%"></div>
                    </div>
                    <span class="text-xs text-gray-500">${backtest.progress}%</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm space-x-2">
                    ${backtest.status === 'pending' ? `<button onclick="runBacktest(${backtest.id})" class="text-green-600 hover:text-green-900">运行</button>` : ''}
                    ${backtest.status === 'completed' ? `<button onclick="viewBacktestResult(${backtest.id})" class="text-indigo-600 hover:text-indigo-900">查看结果</button>` : ''}
                    <button onclick="deleteBacktest(${backtest.id})" class="text-red-600 hover:text-red-900">删除</button>
                </td>
            </tr>
        `;
    }).join('');
}

// 显示回测创建器
function showBacktestCreator() {
    document.getElementById('backtest-list-view').classList.add('hidden');
    document.getElementById('backtest-creator-view').classList.remove('hidden');
    document.getElementById('backtest-result-view').classList.add('hidden');
    
    // 设置默认日期
    const today = new Date();
    const sixMonthsAgo = new Date(today.getFullYear(), today.getMonth() - 6, today.getDate());
    document.getElementById('backtest-end-date').value = today.toISOString().split('T')[0];
    document.getElementById('backtest-start-date').value = sixMonthsAgo.toISOString().split('T')[0];
    
    updateBacktestStrategySelect();
    renderBacktestInstruments();
}

// 显示回测列表
function showBacktestList() {
    document.getElementById('backtest-creator-view').classList.add('hidden');
    document.getElementById('backtest-result-view').classList.add('hidden');
    document.getElementById('backtest-list-view').classList.remove('hidden');
}

// 更新回测策略选择
function updateBacktestStrategySelect() {
    const select = document.getElementById('backtest-strategy');
    if (!select) return;
    
    select.innerHTML = '<option value="">请选择策略</option>';
    state.strategies.forEach(strategy => {
        const option = document.createElement('option');
        option.value = strategy.id;
        option.textContent = strategy.name;
        select.appendChild(option);
    });
}

// 渲染回测标的列表
function renderBacktestInstruments() {
    const container = document.getElementById('backtest-instruments');
    if (!container) return;
    
    container.innerHTML = state.instruments.map(inst => `
        <div class="flex items-center mb-2">
            <input type="checkbox" id="inst-${inst.id}" value="${inst.id}" class="mr-2 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
            <label for="inst-${inst.id}" class="text-sm">
                <span class="font-medium">${inst.symbol}</span>
                <span class="text-gray-500 text-xs ml-1">(${getAssetClassLabel(inst.asset_class)})</span>
            </label>
        </div>
    `).join('');
}

// 创建回测
async function createBacktest() {
    const name = document.getElementById('backtest-name').value;
    const strategyId = document.getElementById('backtest-strategy').value;
    const timeframe = document.getElementById('backtest-timeframe').value;
    const startDate = document.getElementById('backtest-start-date').value;
    const endDate = document.getElementById('backtest-end-date').value;
    
    // 获取选中的标的
    const selectedInstruments = [];
    document.querySelectorAll('#backtest-instruments input:checked').forEach(cb => {
        selectedInstruments.push(parseInt(cb.value));
    });
    
    if (!name || !strategyId || selectedInstruments.length === 0) {
        showNotification('请填写完整信息并选择至少一个标的', 'error');
        return;
    }
    
    const backtestData = {
        name,
        strategy_id: parseInt(strategyId),
        instrument_ids: selectedInstruments,
        timeframe,
        start_time: new Date(startDate).toISOString(),
        end_time: new Date(endDate).toISOString()
    };
    
    try {
        const response = await fetch(`${API_BASE}/backtests`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(backtestData)
        });
        
        if (response.ok) {
            showNotification('回测任务创建成功', 'success');
            await loadBacktests();
            showBacktestList();
            renderBacktestsTable();
            updateDashboard();
        } else {
            const error = await response.json();
            showNotification('创建失败: ' + (error.detail || '未知错误'), 'error');
        }
    } catch (error) {
        showNotification('创建失败: ' + error.message, 'error');
    }
}

// 运行回测
async function runBacktest(backtestId) {
    showNotification('开始运行回测...', 'info');
    
    try {
        const response = await fetch(`${API_BASE}/backtests/${backtestId}/run`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const result = await response.json();
            showNotification('回测运行成功', 'success');
            await loadBacktests();
            renderBacktestsTable();
            viewBacktestResult(backtestId);
        } else {
            const error = await response.json();
            showNotification('运行失败: ' + (error.detail || '未知错误'), 'error');
        }
    } catch (error) {
        showNotification('运行失败: ' + error.message, 'error');
    }
}

// 查看回测结果
async function viewBacktestResult(backtestId) {
    const backtest = state.backtests.find(b => b.id === backtestId);
    if (!backtest) return;
    
    try {
        // 获取结果数据
        const response = await fetch(`${API_BASE}/backtests/${backtestId}`);
        if (!response.ok) return;
        
        // 获取最新的结果ID
        const resultResponse = await fetch(`${API_BASE}/analyze/1/summary`);
        const resultData = await resultResponse.json();
        
        // 获取指标
        const metricsResponse = await fetch(`${API_BASE}/analyze/1/metrics`);
        const metrics = await metricsResponse.json();
        
        // 获取图表数据
        const chartsResponse = await fetch(`${API_BASE}/analyze/1/charts`);
        const charts = await chartsResponse.json();
        
        // 显示结果页面
        document.getElementById('backtest-list-view').classList.add('hidden');
        document.getElementById('backtest-creator-view').classList.add('hidden');
        document.getElementById('backtest-result-view').classList.remove('hidden');
        
        // 更新指标卡片
        document.getElementById('result-total-return').textContent = (metrics.total_return * 100).toFixed(2) + '%';
        document.getElementById('result-annual-return').textContent = (metrics.annual_return * 100).toFixed(2) + '%';
        document.getElementById('result-sharpe').textContent = metrics.sharpe_ratio.toFixed(2);
        document.getElementById('result-max-drawdown').textContent = (metrics.max_drawdown * 100).toFixed(2) + '%';
        document.getElementById('result-win-rate').textContent = (metrics.win_rate * 100).toFixed(2) + '%';
        document.getElementById('result-trades').textContent = resultData.total_trades || 0;
        document.getElementById('result-profit-factor').textContent = metrics.profit_factor.toFixed(2);
        document.getElementById('result-volatility').textContent = (metrics.volatility * 100).toFixed(2) + '%';
        
        // 渲染图表
        renderEquityChart(charts.equity_curve);
        renderDrawdownChart(charts.drawdown);
        
        // 渲染交易记录
        renderTradesTable(charts.trades);
        
    } catch (error) {
        showNotification('加载结果失败: ' + error.message, 'error');
    }
}

// 渲染权益曲线图表
function renderEquityChart(equityData) {
    const ctx = document.getElementById('equity-chart');
    if (!ctx) return;
    
    if (state.equityChart) {
        state.equityChart.destroy();
    }
    
    const labels = Object.keys(equityData);
    const data = Object.values(equityData);
    
    state.equityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: '权益曲线',
                data: data,
                borderColor: 'rgb(99, 102, 241)',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { display: false },
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

// 渲染回撤图表
function renderDrawdownChart(drawdownData) {
    const ctx = document.getElementById('drawdown-chart');
    if (!ctx) return;
    
    if (state.drawdownChart) {
        state.drawdownChart.destroy();
    }
    
    const labels = Object.keys(drawdownData);
    const data = Object.values(drawdownData);
    
    state.drawdownChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: '回撤',
                data: data,
                borderColor: 'rgb(239, 68, 68)',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { display: false },
                y: {
                    ticks: {
                        callback: function(value) {
                            return (value * 100).toFixed(1) + '%';
                        }
                    }
                }
            }
        }
    });
}

// 渲染交易记录表格
function renderTradesTable(trades) {
    const tbody = document.getElementById('trades-table-body');
    if (!tbody) return;
    
    if (!trades || trades.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="px-4 py-4 text-center text-gray-500">暂无交易记录</td></tr>';
        return;
    }
    
    tbody.innerHTML = trades.slice(0, 20).map(trade => `
        <tr class="hover:bg-gray-50">
            <td class="px-4 py-2 text-sm text-gray-900">${new Date(trade.entry_time).toLocaleString()}</td>
            <td class="px-4 py-2 text-sm text-gray-900">${new Date(trade.exit_time).toLocaleString()}</td>
            <td class="px-4 py-2 text-sm text-gray-500">$${trade.entry_price.toFixed(2)}</td>
            <td class="px-4 py-2 text-sm text-gray-500">$${trade.exit_price.toFixed(2)}</td>
            <td class="px-4 py-2 text-sm ${trade.return >= 0 ? 'text-green-600' : 'text-red-600'}">
                ${(trade.return * 100).toFixed(2)}%
            </td>
        </tr>
    `).join('');
}

// 删除回测
async function deleteBacktest(backtestId) {
    if (!confirm('确定要删除这个回测任务吗？')) return;
    
    try {
        const response = await fetch(`${API_BASE}/backtests/${backtestId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showNotification('回测任务删除成功', 'success');
            await loadBacktests();
            renderBacktestsTable();
            updateDashboard();
        }
    } catch (error) {
        showNotification('删除失败: ' + error.message, 'error');
    }
}

// 筛选回测
function filterBacktests(searchTerm, status) {
    const search = searchTerm || document.getElementById('search-backtests')?.value?.toLowerCase() || '';
    const filter = status || document.getElementById('filter-backtest-status')?.value || '';
    
    let filtered = [...state.backtests];
    
    if (search) {
        filtered = filtered.filter(b => 
            b.name.toLowerCase().includes(search)
        );
    }
    
    if (filter) {
        filtered = filtered.filter(b => b.status === filter);
    }
    
    const tbody = document.getElementById('backtests-table-body');
    if (filtered.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="px-6 py-4 text-center text-gray-500">没有找到匹配的回测</td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = filtered.map(backtest => {
        const strategy = state.strategies.find(s => s.id === backtest.strategy_id);
        return `
            <tr class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${backtest.name}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${strategy ? strategy.name : '未知'}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    ${new Date(backtest.start_time).toLocaleDateString()} - ${new Date(backtest.end_time).toLocaleDateString()}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getBacktestStatusStyle(backtest.status)}">
                        ${getBacktestStatusLabel(backtest.status)}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <div class="w-full bg-gray-200 rounded-full h-2.5">
                        <div class="bg-indigo-600 h-2.5 rounded-full" style="width: ${backtest.progress}%"></div>
                    </div>
                    <span class="text-xs text-gray-500">${backtest.progress}%</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm space-x-2">
                    ${backtest.status === 'pending' ? `<button onclick="runBacktest(${backtest.id})" class="text-green-600 hover:text-green-900">运行</button>` : ''}
                    ${backtest.status === 'completed' ? `<button onclick="viewBacktestResult(${backtest.id})" class="text-indigo-600 hover:text-indigo-900">查看结果</button>` : ''}
                    <button onclick="deleteBacktest(${backtest.id})" class="text-red-600 hover:text-red-900">删除</button>
                </td>
            </tr>
        `;
    }).join('');
}

// 导出结果
function exportResults() {
    showNotification('导出功能开发中...', 'info');
}

// ==================== 标的管理 ====================

// 加载标的数据
async function loadInstruments() {
    try {
        const response = await fetch(`${API_BASE.replace('/strategies', '')}/master/instruments`);
        if (response.ok) {
            state.instruments = await response.json();
        } else {
            state.instruments = mockInstruments;
        }
    } catch (error) {
        state.instruments = mockInstruments;
    }
    
    renderInstrumentsTable();
}

// 渲染标的表格
function renderInstrumentsTable() {
    const tbody = document.getElementById('instruments-table-body');
    const instruments = state.instruments;
    
    if (instruments.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">暂无数据</td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = instruments.map(instrument => `
        <tr class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${instrument.symbol}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${instrument.name || instrument.symbol}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${getExchangeName(instrument.exchange_id)}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getAssetClassStyle(instrument.asset_class)}">
                    ${getAssetClassLabel(instrument.asset_class)}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${instrument.instrument_type}</td>
        </tr>
    `).join('');
}

// 筛选标的
function filterInstruments(searchTerm, assetClass) {
    const search = searchTerm || document.getElementById('search-instruments')?.value?.toLowerCase() || '';
    const filter = assetClass || document.getElementById('filter-asset-class')?.value || '';
    
    let filtered = [...state.instruments];
    
    if (search) {
        filtered = filtered.filter(i => 
            i.symbol.toLowerCase().includes(search) || 
            (i.name && i.name.toLowerCase().includes(search))
        );
    }
    
    if (filter) {
        filtered = filtered.filter(i => i.asset_class === filter);
    }
    
    const tbody = document.getElementById('instruments-table-body');
    if (filtered.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">没有找到匹配的标的</td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = filtered.map(instrument => `
        <tr class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${instrument.symbol}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${instrument.name || instrument.symbol}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${getExchangeName(instrument.exchange_id)}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getAssetClassStyle(instrument.asset_class)}">
                    ${getAssetClassLabel(instrument.asset_class)}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${instrument.instrument_type}</td>
        </tr>
    `).join('');
}

// 刷新标的
async function refreshInstruments() {
    addActivity('正在刷新标的数据...');
    await loadInstruments();
    addActivity('标的数据已刷新');
}

// 同步标的
async function syncInstruments(datasourceCode) {
    addActivity(`正在同步 ${datasourceCode} 标的数据...`);
    const syncStatus = document.getElementById('sync-status');
    syncStatus.innerHTML = `
        <div class="flex items-center p-4 bg-blue-50 rounded-lg">
            <div class="animate-pulse mr-3">
                <div class="h-4 w-4 bg-blue-500 rounded-full"></div>
            </div>
            <p class="font-medium text-blue-700">正在同步 ${datasourceCode} 数据...</p>
        </div>
    `;
    
    try {
        const response = await fetch(`http://localhost:8001/api/v1/datasources/sync-instruments?datasource_code=${datasourceCode}`);
        if (response.ok) {
            syncStatus.innerHTML = `
                <div class="flex items-center p-4 bg-green-50 rounded-lg">
                    <span class="text-green-500 mr-3">✅</span>
                    <p class="font-medium text-green-700">${datasourceCode} 数据同步成功!</p>
                </div>
            `;
            addActivity(`${datasourceCode} 标的数据已同步`);
        } else {
            syncStatus.innerHTML = `
                <div class="flex items-center p-4 bg-gray-50 rounded-lg">
                    <span class="text-gray-500 mr-3">ℹ️</span>
                    <p class="font-medium text-gray-700">演示模式: ${datasourceCode} 同步完成 (模拟)</p>
                </div>
            `;
            addActivity(`${datasourceCode} 标的数据已同步 (演示模式)`);
        }
    } catch (error) {
        syncStatus.innerHTML = `
            <div class="flex items-center p-4 bg-gray-50 rounded-lg">
                <span class="text-gray-500 mr-3">ℹ️</span>
                <p class="font-medium text-gray-700">演示模式: ${datasourceCode} 同步完成 (模拟)</p>
            </div>
        `;
        addActivity(`${datasourceCode} 标的数据已同步 (演示模式)`);
    }
}

// ==================== 工具函数 ====================

// 更新仪表盘
function updateDashboard() {
    document.getElementById('dashboard-strategy-count').textContent = state.strategies.length;
    document.getElementById('dashboard-backtest-count').textContent = state.backtests.filter(b => b.status === 'completed').length;
}

// 获取交易所名称
function getExchangeName(exchangeId) {
    const exchange = state.exchanges.find(e => e.id === exchangeId);
    return exchange ? exchange.name : '未知';
}

// 获取资产类型样式
function getAssetClassStyle(assetClass) {
    const styles = {
        'crypto': 'bg-yellow-100 text-yellow-800',
        'equity': 'bg-blue-100 text-blue-800',
        'future': 'bg-purple-100 text-purple-800',
        'option': 'bg-green-100 text-green-800',
        'fx': 'bg-pink-100 text-pink-800',
        'bond': 'bg-gray-100 text-gray-800'
    };
    return styles[assetClass] || 'bg-gray-100 text-gray-800';
}

// 获取资产类型标签
function getAssetClassLabel(assetClass) {
    const labels = {
        'crypto': '加密货币',
        'equity': '股票',
        'future': '期货',
        'option': '期权',
        'fx': '外汇',
        'bond': '债券'
    };
    return labels[assetClass] || assetClass;
}

// 获取策略状态样式
function getStrategyStatusStyle(status) {
    const styles = {
        'draft': 'bg-gray-100 text-gray-800',
        'testing': 'bg-yellow-100 text-yellow-800',
        'live': 'bg-green-100 text-green-800',
        'archived': 'bg-red-100 text-red-800'
    };
    return styles[status] || 'bg-gray-100 text-gray-800';
}

// 获取策略状态标签
function getStrategyStatusLabel(status) {
    const labels = {
        'draft': '草稿',
        'testing': '测试中',
        'live': '实盘',
        'archived': '已归档'
    };
    return labels[status] || status;
}

// 获取回测状态样式
function getBacktestStatusStyle(status) {
    const styles = {
        'pending': 'bg-gray-100 text-gray-800',
        'running': 'bg-blue-100 text-blue-800',
        'completed': 'bg-green-100 text-green-800',
        'failed': 'bg-red-100 text-red-800',
        'cancelled': 'bg-orange-100 text-orange-800'
    };
    return styles[status] || 'bg-gray-100 text-gray-800';
}

// 获取回测状态标签
function getBacktestStatusLabel(status) {
    const labels = {
        'pending': '待运行',
        'running': '运行中',
        'completed': '已完成',
        'failed': '失败',
        'cancelled': '已取消'
    };
    return labels[status] || status;
}

// 添加活动记录
function addActivity(message) {
    const activityList = document.getElementById('activity-list');
    const activityDiv = document.createElement('div');
    activityDiv.className = 'flex items-center p-4 bg-gray-50 rounded-lg';
    activityDiv.innerHTML = `
        <span class="text-indigo-500 mr-3">🔄</span>
        <div>
            <p class="font-medium">${message}</p>
            <p class="text-gray-500 text-sm">${new Date().toLocaleTimeString()}</p>
        </div>
    `;
    activityList.insertBefore(activityDiv, activityList.firstChild);
}

// 显示通知
function showNotification(message, type = 'info') {
    const colors = {
        'success': 'bg-green-500',
        'error': 'bg-red-500',
        'info': 'bg-blue-500',
        'warning': 'bg-yellow-500'
    };
    
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 transform transition-all duration-300 translate-x-full`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // 动画显示
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);
    
    // 自动隐藏
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}
