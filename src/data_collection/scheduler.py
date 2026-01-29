"""
Data collection scheduler
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from typing import Dict, List
import asyncio
import yaml
import logging
from .collectors.yahoo_finance_collector import YahooFinanceCollector
from .collectors.fred_collector import FREDCollector

logger = logging.getLogger(__name__)


class DataScheduler:
    """Scheduler for periodic data collection"""
    
    def __init__(self, config_path: str = "config/config.yaml", secrets_path: str = "config/secrets.yaml"):
        self.scheduler = AsyncIOScheduler()
        self.collectors = {}
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        try:
            with open(secrets_path, 'r') as f:
                self.secrets = yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning("secrets.yaml not found, using environment variables")
            self.secrets = {}
        
        self._initialize_collectors()
    
    def _initialize_collectors(self):
        """Initialize data collectors"""
        # Yahoo Finance collector
        yahoo_config = {
            'rate_limit_delay': 0.5
        }
        self.collectors['yahoo'] = YahooFinanceCollector(yahoo_config)
        
        # FRED collector
        fred_api_key = self.secrets.get('data_sources', {}).get('fred', {}).get('api_key')
        if fred_api_key:
            fred_config = {'api_key': fred_api_key}
            self.collectors['fred'] = FREDCollector(fred_config)
        else:
            logger.warning("FRED API key not found, FRED collector disabled")
    
    def start(self):
        """Start the scheduler"""
        # Real-time data collection (every minute)
        self.scheduler.add_job(
            self._collect_realtime_data,
            trigger=IntervalTrigger(seconds=self.config['data_collection']['update_intervals']['realtime']),
            id='realtime_collection',
            name='Real-time Data Collection',
            replace_existing=True
        )
        
        # Daily data collection (market close)
        daily_time = self.config['data_collection']['update_intervals']['daily']
        hour, minute = map(int, daily_time.split(':'))
        self.scheduler.add_job(
            self._collect_daily_data,
            trigger=CronTrigger(hour=hour, minute=minute),
            id='daily_collection',
            name='Daily Data Collection',
            replace_existing=True
        )
        
        # Weekly data collection
        self.scheduler.add_job(
            self._collect_weekly_data,
            trigger=CronTrigger(day_of_week='sat', hour=0, minute=0),
            id='weekly_collection',
            name='Weekly Data Collection',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("Data collection scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        logger.info("Data collection scheduler stopped")
    
    async def _collect_realtime_data(self):
        """Collect real-time market data"""
        logger.info("Starting real-time data collection")
        
        try:
            # Collect ETF data
            etf_symbols = (
                self.config['data_collection']['symbols']['etf_equity'] +
                self.config['data_collection']['symbols']['etf_bonds'] +
                self.config['data_collection']['symbols']['etf_sectors'] +
                self.config['data_collection']['symbols']['etf_international']
            )
            
            # Collect forex data
            forex_symbols = self.config['data_collection']['symbols']['forex']
            
            # Collect volatility data
            vol_symbols = self.config['data_collection']['symbols']['volatility']
            
            all_symbols = etf_symbols + forex_symbols + vol_symbols
            
            if 'yahoo' in self.collectors:
                data = await self.collectors['yahoo'].collect(all_symbols)
                logger.info(f"Collected {len(data)} real-time data points")
                
                # TODO: Store data in database
                # await self._store_data(data)
            
        except Exception as e:
            logger.error(f"Error in real-time data collection: {e}")
    
    async def _collect_daily_data(self):
        """Collect daily market data"""
        logger.info("Starting daily data collection")
        
        try:
            # Collect treasury yields from FRED
            if 'fred' in self.collectors:
                treasury_symbols = ['DGS2', 'DGS5', 'DGS10', 'DGS30', 'T10Y2Y']
                data = await self.collectors['fred'].collect(treasury_symbols)
                logger.info(f"Collected {len(data)} daily data points from FRED")
                
                # Get yield curve analysis
                yield_curve = await self.collectors['fred'].get_yield_curve()
                if yield_curve:
                    logger.info(f"Yield curve: {yield_curve['spreads']}")
                    if yield_curve['inverted']:
                        logger.warning("⚠️ Yield curve is INVERTED!")
            
            # Collect ETF flows
            if 'yahoo' in self.collectors:
                etf_symbols = self.config['data_collection']['symbols']['etf_equity']
                for symbol in etf_symbols:
                    flow_data = await self.collectors['yahoo'].get_etf_flows(symbol)
                    if flow_data:
                        logger.info(f"{symbol} flow: {flow_data['net_flow_indicator']}")
        
        except Exception as e:
            logger.error(f"Error in daily data collection: {e}")
    
    async def _collect_weekly_data(self):
        """Collect weekly market data"""
        logger.info("Starting weekly data collection")
        
        try:
            # Collect comprehensive historical data for analysis
            # TODO: Implement weekly data collection
            pass
        
        except Exception as e:
            logger.error(f"Error in weekly data collection: {e}")
    
    async def collect_on_demand(self, symbols: List[str], source: str = 'yahoo') -> List:
        """
        Collect data on demand
        
        Args:
            symbols: List of symbols to collect
            source: Data source ('yahoo' or 'fred')
            
        Returns:
            List of collected data
        """
        if source not in self.collectors:
            raise ValueError(f"Collector '{source}' not available")
        
        return await self.collectors[source].collect(symbols)


async def main():
    """Main function for testing"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    scheduler = DataScheduler()
    scheduler.start()
    
    try:
        # Keep running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()


if __name__ == "__main__":
    asyncio.run(main())
