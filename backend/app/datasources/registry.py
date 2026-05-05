from typing import Dict, List, Optional
from .base import DataSource

class DataSourceRegistry:
    _registry: Dict[str, DataSource] = {}
    
    @classmethod
    def register(cls, datasource: DataSource):
        """注册数据源"""
        cls._registry[datasource.code] = datasource
    
    @classmethod
    def get(cls, code: str) -> Optional[DataSource]:
        """获取指定数据源"""
        return cls._registry.get(code)
    
    @classmethod
    def list_all(cls) -> List[DataSource]:
        """列出所有已注册的数据源"""
        return list(cls._registry.values())
    
    @classmethod
    def list_codes(cls) -> List[str]:
        """列出所有已注册的数据源代码"""
        return list(cls._registry.keys())
