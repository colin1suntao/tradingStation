// API 基础配置
const API_BASE = 'http://localhost:8000/api/v1';

// 应用状态
let state = {
    instruments: [],
    exchanges: [
        { id: 1, name: 'Binance', code: 'binance', country: 'Global' },
        { id: 2, name: 'NYSE', code: 'nyse', country: 'USA' },
        { id: 3, name: 'NASDAQ', code: 'nasdaq', country: 'USA' }
    ],
    activeSection: 'dashboard'
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

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

async function initApp() {
    await checkBackendStatus();
    await loadInstruments();
    setupEventListeners();
}

// 检查后端状态
async function checkBackendStatus() {
    try {
        const response = await fetch('http://localhost:8000/health');
        const data = await response.json();
        document.getElementById('backend-status').textContent = `已连接 - ${data.timestamp}`;
        document.getElementById('backend-status').className = 'text-green-500 text-sm mt-1';
    } catch (error) {
        document.getElementById('backend-status').textContent = '连接失败 - 使用模拟数据';
        document.getElementById('backend-status').className = 'text-red-500 text-sm mt-1';
    }
}

// 设置事件监听器
function setupEventListeners() {
    document.getElementById('search-instruments').addEventListener('input', (e) => filterInstruments(e.target.value));
    document.getElementById('filter-asset-class').addEventListener('change', (e) => filterInstruments(null, e.target.value));
}

// 显示/隐藏部分
function showSection(sectionName) {
    document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
    document.getElementById(`section-${sectionName}`).classList.remove('hidden');
    
    // 更新导航高亮
    document.querySelectorAll('nav a').forEach(a => a.classList.remove('bg-white/20', 'font-semibold'));
    document.getElementById(`nav-${sectionName}`).classList.add('bg-white/20', 'font-semibold');
    
    state.activeSection = sectionName;
    
    if (sectionName === 'instruments') {
        renderInstrumentsTable();
    }
}

// 加载标的数据
async function loadInstruments() {
    try {
        const response = await fetch(`${API_BASE}/master/instruments`);
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

// 筛选标的
function filterInstruments(searchTerm, assetClass) {
    const search = searchTerm || document.getElementById('search-instruments').value.toLowerCase();
    const filter = assetClass || document.getElementById('filter-asset-class').value;
    
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
    
    // 临时更新 state 并重新渲染
    const originalInstruments = state.instruments;
    state.instruments = filtered.length > 0 ? filtered : originalInstruments;
    renderInstrumentsTable();
    if (filtered.length === 0) state.instruments = originalInstruments;
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
        const response = await fetch(`http://localhost:8000/api/v1/datasources/sync-instruments?datasource_code=${datasourceCode}`);
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
