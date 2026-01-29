"""
FRED (Federal Reserve Economic Data) collector
"""
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import asyncio
from .base_collector import BaseCollector, MarketData
import logging

logger = logging.getLogger(__name__)


class FREDCollector(BaseCollector):
    """Collector for FRED economic data"""
    
    BASE_URL = "https://api.stlouisfed.org/fred"
    
    # FRED series IDs for key indicators
    SERIES_MAP = {
        "DGS2": "2_year_treasury",      # 2-Year Treasury
        "DGS10": "10_year_treasury",    # 10-Year Treasury
        "DGS30": "30_year_treasury",    # 30-Year Treasury
        "T10Y2Y": "yield_curve_10y2y",  # 10Y-2Y Spread
        "DFEDTARU": "fed_funds_rate",   # Fed Funds Target Rate
        "DEXUSEU": "usd_eur",           # USD/EUR
        "DEXJPUS": "jpy_usd",           # JPY/USD
        "DEXKOUS": "usd_krw",           # USD/KRW
    }
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.api_key = config.get('api_key')
        if not self.api_key:
            raise ValueError("FRED API key is required")
    
    async def collect(self, symbols: List[str]) -> List[MarketData]:
        """
        Collect data from FRED
        
        Args:
            symbols: List of FRED series IDs
            
        Returns:
            List of MarketData objects
        """
        results = []
        
        for symbol in symbols:
            try:
                data = await self._fetch_series(symbol)
                if data:
                    results.append(data)
                
                # Rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                self._handle_error(e, symbol)
        
        logger.info(f"Collected {len(results)}/{len(symbols)} series from FRED")
        return results
    
    async def _fetch_series(self, series_id: str) -> Optional[MarketData]:
        """
        Fetch a single FRED series
        
        Args:
            series_id: FRED series ID
            
        Returns:
            MarketData object
        """
        url = f"{self.BASE_URL}/series/observations"
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json',
            'sort_order': 'desc',
            'limit': 1
        }
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.get(url, params=params, timeout=10)
        )
        
        if response.status_code != 200:
            logger.error(f"FRED API error for {series_id}: {response.status_code}")
            return None
        
        data = response.json()
        
        if 'observations' not in data or len(data['observations']) == 0:
            logger.warning(f"No data available for {series_id}")
            return None
        
        obs = data['observations'][0]
        
        # Skip if value is '.'
        if obs['value'] == '.':
            logger.warning(f"Missing value for {series_id}")
            return None
        
        return MarketData(
            symbol=series_id,
            timestamp=datetime.strptime(obs['date'], '%Y-%m-%d'),
            price=float(obs['value']),
            metadata={
                'source': 'fred',
                'series_name': self.SERIES_MAP.get(series_id, series_id),
                'realtime_start': obs.get('realtime_start'),
                'realtime_end': obs.get('realtime_end')
            }
        )
    
    async def validate_connection(self) -> bool:
        """
        Validate FRED API connection
        
        Returns:
            True if connection is valid
        """
        try:
            test_data = await self.collect(['DGS10'])
            return len(test_data) > 0
        except Exception as e:
            logger.error(f"FRED connection validation failed: {e}")
            return False
    
    async def get_yield_curve(self) -> Dict:
        """
        Get current yield curve data
        
        Returns:
            Yield curve data with spreads
        """
        series_ids = ['DGS2', 'DGS5', 'DGS10', 'DGS30']
        data = await self.collect(series_ids)
        
        if len(data) < 2:
            return None
        
        yields = {d.symbol: d.price for d in data}
        
        # Calculate spreads
        spreads = {}
        if 'DGS10' in yields and 'DGS2' in yields:
            spreads['10y_2y'] = yields['DGS10'] - yields['DGS2']
        
        if 'DGS30' in yields and 'DGS10' in yields:
            spreads['30y_10y'] = yields['DGS30'] - yields['DGS10']
        
        return {
            'yields': yields,
            'spreads': spreads,
            'timestamp': datetime.now(),
            'inverted': spreads.get('10y_2y', 0) < 0
        }
    
    async def get_rate_differential(self, country1: str = "US", country2: str = "KR") -> float:
        """
        Calculate interest rate differential between countries
        
        Args:
            country1: First country code
            country2: Second country code
            
        Returns:
            Rate differential (country1 - country2)
        """
        # Simplified: using 10Y treasury as proxy
        # In production, would use actual policy rates
        
        if country1 == "US":
            us_data = await self._fetch_series('DGS10')
            us_rate = us_data.price if us_data else 0
        
        # For Korea, would need separate data source
        # This is a placeholder
        kr_rate = 3.5  # Placeholder
        
        return us_rate - kr_rate
