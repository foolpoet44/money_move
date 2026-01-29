"""
Stream processor for real-time data
"""
from typing import Dict, List, Optional
from datetime import datetime
from collections import deque
import numpy as np
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ProcessedSignal:
    """Processed market signal"""
    symbol: str
    timestamp: datetime
    value: float
    z_score: float
    anomaly_score: float
    signal_type: str  # 'normal', 'warning', 'critical'
    metadata: Dict


class StreamProcessor:
    """Real-time data stream processor"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.data_buffers = {}  # symbol -> deque of values
        self.stats_cache = {}   # symbol -> {mean, std}
    
    def process_tick(self, symbol: str, value: float, timestamp: datetime = None) -> Optional[ProcessedSignal]:
        """
        Process a single data tick
        
        Args:
            symbol: Symbol identifier
            value: Data value
            timestamp: Timestamp (default: now)
            
        Returns:
            ProcessedSignal if anomaly detected, None otherwise
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Initialize buffer if needed
        if symbol not in self.data_buffers:
            self.data_buffers[symbol] = deque(maxlen=self.window_size)
        
        # Add to buffer
        self.data_buffers[symbol].append(value)
        
        # Need enough data for statistics
        if len(self.data_buffers[symbol]) < 30:
            return None
        
        # Calculate statistics
        z_score = self._calculate_z_score(symbol, value)
        anomaly_score = self._calculate_anomaly_score(z_score)
        signal_type = self._classify_signal(anomaly_score)
        
        # Only return if significant
        if abs(z_score) > 2.0:
            return ProcessedSignal(
                symbol=symbol,
                timestamp=timestamp,
                value=value,
                z_score=z_score,
                anomaly_score=anomaly_score,
                signal_type=signal_type,
                metadata={
                    'buffer_size': len(self.data_buffers[symbol]),
                    'mean': self.stats_cache[symbol]['mean'],
                    'std': self.stats_cache[symbol]['std']
                }
            )
        
        return None
    
    def _calculate_z_score(self, symbol: str, value: float) -> float:
        """
        Calculate Z-score for anomaly detection
        
        Args:
            symbol: Symbol identifier
            value: Current value
            
        Returns:
            Z-score
        """
        data = np.array(self.data_buffers[symbol])
        mean = np.mean(data)
        std = np.std(data)
        
        # Cache statistics
        self.stats_cache[symbol] = {'mean': mean, 'std': std}
        
        if std == 0:
            return 0
        
        return (value - mean) / std
    
    def _calculate_anomaly_score(self, z_score: float) -> float:
        """
        Convert Z-score to anomaly score (0-100)
        
        Args:
            z_score: Z-score value
            
        Returns:
            Anomaly score (0-100)
        """
        # Use sigmoid-like function to map z_score to 0-100
        abs_z = abs(z_score)
        
        if abs_z < 2:
            return 0
        elif abs_z < 3:
            return 50
        elif abs_z < 4:
            return 75
        else:
            return 100
    
    def _classify_signal(self, anomaly_score: float) -> str:
        """
        Classify signal based on anomaly score
        
        Args:
            anomaly_score: Anomaly score (0-100)
            
        Returns:
            Signal type: 'normal', 'warning', 'critical'
        """
        if anomaly_score >= 75:
            return 'critical'
        elif anomaly_score >= 50:
            return 'warning'
        else:
            return 'normal'
    
    def get_statistics(self, symbol: str) -> Optional[Dict]:
        """
        Get current statistics for a symbol
        
        Args:
            symbol: Symbol identifier
            
        Returns:
            Statistics dictionary
        """
        if symbol not in self.data_buffers or len(self.data_buffers[symbol]) == 0:
            return None
        
        data = np.array(self.data_buffers[symbol])
        
        return {
            'symbol': symbol,
            'count': len(data),
            'mean': float(np.mean(data)),
            'std': float(np.std(data)),
            'min': float(np.min(data)),
            'max': float(np.max(data)),
            'current': float(data[-1]),
            'change_pct': float((data[-1] - data[0]) / data[0] * 100) if data[0] != 0 else 0
        }
    
    def clear_buffer(self, symbol: str):
        """Clear buffer for a symbol"""
        if symbol in self.data_buffers:
            self.data_buffers[symbol].clear()
            logger.info(f"Cleared buffer for {symbol}")
