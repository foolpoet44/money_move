"""
Feature engineering for ML models
"""
from typing import Dict, List
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Feature engineering for prediction models"""
    
    def __init__(self):
        self.feature_cache = {}
    
    def create_features(self, market_data: pd.DataFrame) -> Dict:
        """
        Create comprehensive feature set
        
        Args:
            market_data: DataFrame with market data
            
        Returns:
            Dictionary of features
        """
        features = {}
        
        # Technical indicators
        features.update(self.technical_indicators(market_data))
        
        # Market structure indicators
        features.update(self.market_structure_indicators(market_data))
        
        # Momentum indicators
        features.update(self.momentum_indicators(market_data))
        
        return features
    
    def technical_indicators(self, data: pd.DataFrame) -> Dict:
        """
        Calculate technical indicators
        
        Args:
            data: Market data DataFrame
            
        Returns:
            Technical indicators
        """
        features = {}
        
        if 'close' not in data.columns:
            return features
        
        close = data['close']
        
        # RSI (Relative Strength Index)
        features['rsi_14'] = self._calculate_rsi(close, period=14)
        
        # MACD
        macd_data = self._calculate_macd(close)
        features.update(macd_data)
        
        # Bollinger Bands
        bb_data = self._calculate_bollinger_bands(close)
        features.update(bb_data)
        
        # Moving averages
        features['sma_20'] = close.rolling(window=20).mean().iloc[-1]
        features['sma_50'] = close.rolling(window=50).mean().iloc[-1]
        features['ema_12'] = close.ewm(span=12).mean().iloc[-1]
        
        return features
    
    def market_structure_indicators(self, data: pd.DataFrame) -> Dict:
        """
        Calculate market structure indicators
        
        Args:
            data: Market data with multiple symbols
            
        Returns:
            Market structure features
        """
        features = {}
        
        # These would require multiple symbols in data
        # Placeholder implementation
        
        features['market_breadth'] = 0.5  # Placeholder
        features['advance_decline_ratio'] = 1.0  # Placeholder
        
        return features
    
    def momentum_indicators(self, data: pd.DataFrame) -> Dict:
        """
        Calculate momentum indicators
        
        Args:
            data: Market data DataFrame
            
        Returns:
            Momentum features
        """
        features = {}
        
        if 'close' not in data.columns:
            return features
        
        close = data['close']
        
        # Rate of change
        features['roc_1d'] = self._calculate_roc(close, period=1)
        features['roc_5d'] = self._calculate_roc(close, period=5)
        features['roc_20d'] = self._calculate_roc(close, period=20)
        
        # Momentum
        features['momentum_10'] = close.iloc[-1] - close.iloc[-10] if len(close) >= 10 else 0
        
        return features
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """Calculate RSI"""
        if len(prices) < period + 1:
            return 50.0
        
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return float(rsi.iloc[-1]) if not np.isnan(rsi.iloc[-1]) else 50.0
    
    def _calculate_macd(self, prices: pd.Series, fast=12, slow=26, signal=9) -> Dict:
        """Calculate MACD"""
        if len(prices) < slow:
            return {'macd': 0, 'macd_signal': 0, 'macd_histogram': 0}
        
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        macd_histogram = macd - macd_signal
        
        return {
            'macd': float(macd.iloc[-1]),
            'macd_signal': float(macd_signal.iloc[-1]),
            'macd_histogram': float(macd_histogram.iloc[-1])
        }
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period=20, std_dev=2) -> Dict:
        """Calculate Bollinger Bands"""
        if len(prices) < period:
            return {'bb_upper': 0, 'bb_middle': 0, 'bb_lower': 0, 'bb_width': 0}
        
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        
        bb_upper = sma + (std * std_dev)
        bb_lower = sma - (std * std_dev)
        bb_width = bb_upper - bb_lower
        
        return {
            'bb_upper': float(bb_upper.iloc[-1]),
            'bb_middle': float(sma.iloc[-1]),
            'bb_lower': float(bb_lower.iloc[-1]),
            'bb_width': float(bb_width.iloc[-1])
        }
    
    def _calculate_roc(self, prices: pd.Series, period: int) -> float:
        """Calculate Rate of Change"""
        if len(prices) < period + 1:
            return 0.0
        
        roc = ((prices.iloc[-1] - prices.iloc[-period-1]) / prices.iloc[-period-1]) * 100
        return float(roc) if not np.isnan(roc) else 0.0
