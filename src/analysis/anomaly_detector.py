"""
Anomaly detection system
"""
from typing import Dict, List, Optional
from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Anomaly:
    """Anomaly detection result"""
    symbol: str
    timestamp: str
    anomaly_type: str  # 'statistical', 'ml', 'pattern'
    severity: str  # 'low', 'medium', 'high', 'critical'
    score: float  # 0-100
    details: Dict


class AnomalyDetector:
    """Multi-method anomaly detection"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.z_threshold = self.config.get('z_score_threshold', 2.0)
        self.contamination = self.config.get('isolation_forest_contamination', 0.1)
        
        # Initialize Isolation Forest
        self.isolation_forest = IsolationForest(
            contamination=self.contamination,
            random_state=42
        )
        self.model_trained = False
    
    def detect_anomalies(self, data: pd.DataFrame) -> List[Anomaly]:
        """
        Detect anomalies using multiple methods
        
        Args:
            data: DataFrame with market data
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        # Statistical anomaly detection
        stat_anomalies = self._statistical_detection(data)
        anomalies.extend(stat_anomalies)
        
        # ML-based detection (if enough data)
        if len(data) >= 100:
            ml_anomalies = self._ml_detection(data)
            anomalies.extend(ml_anomalies)
        
        # Pattern-based detection
        pattern_anomalies = self._pattern_detection(data)
        anomalies.extend(pattern_anomalies)
        
        # Remove duplicates and prioritize
        anomalies = self._deduplicate_and_prioritize(anomalies)
        
        logger.info(f"Detected {len(anomalies)} anomalies")
        return anomalies
    
    def _statistical_detection(self, data: pd.DataFrame) -> List[Anomaly]:
        """
        Statistical anomaly detection using Z-score
        
        Args:
            data: Market data
            
        Returns:
            List of statistical anomalies
        """
        anomalies = []
        
        for column in data.select_dtypes(include=[np.number]).columns:
            if column == 'timestamp':
                continue
            
            values = data[column].dropna()
            if len(values) < 30:
                continue
            
            mean = values.mean()
            std = values.std()
            
            if std == 0:
                continue
            
            z_scores = np.abs((values - mean) / std)
            
            # Find anomalies
            anomaly_indices = z_scores[z_scores > self.z_threshold].index
            
            for idx in anomaly_indices:
                z_score = z_scores[idx]
                severity = self._calculate_severity(z_score)
                
                anomalies.append(Anomaly(
                    symbol=column,
                    timestamp=str(data.loc[idx, 'timestamp']) if 'timestamp' in data.columns else str(idx),
                    anomaly_type='statistical',
                    severity=severity,
                    score=min(float(z_score) * 20, 100),  # Convert to 0-100 scale
                    details={
                        'z_score': float(z_score),
                        'value': float(values[idx]),
                        'mean': float(mean),
                        'std': float(std)
                    }
                ))
        
        return anomalies
    
    def _ml_detection(self, data: pd.DataFrame) -> List[Anomaly]:
        """
        ML-based anomaly detection using Isolation Forest
        
        Args:
            data: Market data
            
        Returns:
            List of ML-detected anomalies
        """
        anomalies = []
        
        # Prepare features
        numeric_data = data.select_dtypes(include=[np.number])
        
        if numeric_data.empty or len(numeric_data) < 100:
            return anomalies
        
        # Fill NaN values
        numeric_data = numeric_data.fillna(numeric_data.mean())
        
        # Train or predict
        if not self.model_trained:
            self.isolation_forest.fit(numeric_data)
            self.model_trained = True
        
        # Predict anomalies
        predictions = self.isolation_forest.predict(numeric_data)
        anomaly_scores = self.isolation_forest.score_samples(numeric_data)
        
        # Find anomalies (prediction = -1)
        anomaly_indices = np.where(predictions == -1)[0]
        
        for idx in anomaly_indices:
            score = abs(anomaly_scores[idx]) * 100
            severity = 'high' if score > 75 else 'medium' if score > 50 else 'low'
            
            anomalies.append(Anomaly(
                symbol='multi_feature',
                timestamp=str(data.iloc[idx]['timestamp']) if 'timestamp' in data.columns else str(idx),
                anomaly_type='ml',
                severity=severity,
                score=float(score),
                details={
                    'anomaly_score': float(anomaly_scores[idx]),
                    'features': numeric_data.iloc[idx].to_dict()
                }
            ))
        
        return anomalies
    
    def _pattern_detection(self, data: pd.DataFrame) -> List[Anomaly]:
        """
        Pattern-based anomaly detection
        
        Args:
            data: Market data
            
        Returns:
            List of pattern anomalies
        """
        anomalies = []
        
        # Example: Detect sudden volume spikes
        if 'volume' in data.columns:
            volume = data['volume'].dropna()
            if len(volume) >= 20:
                avg_volume = volume.rolling(window=20).mean()
                volume_ratio = volume / avg_volume
                
                spike_indices = volume_ratio[volume_ratio > 3.0].index
                
                for idx in spike_indices:
                    anomalies.append(Anomaly(
                        symbol='volume',
                        timestamp=str(data.loc[idx, 'timestamp']) if 'timestamp' in data.columns else str(idx),
                        anomaly_type='pattern',
                        severity='medium',
                        score=min(float(volume_ratio[idx]) * 25, 100),
                        details={
                            'volume_ratio': float(volume_ratio[idx]),
                            'volume': float(volume[idx]),
                            'avg_volume': float(avg_volume[idx])
                        }
                    ))
        
        return anomalies
    
    def _calculate_severity(self, z_score: float) -> str:
        """Calculate severity from Z-score"""
        abs_z = abs(z_score)
        
        if abs_z > 4:
            return 'critical'
        elif abs_z > 3:
            return 'high'
        elif abs_z > 2:
            return 'medium'
        else:
            return 'low'
    
    def _deduplicate_and_prioritize(self, anomalies: List[Anomaly]) -> List[Anomaly]:
        """
        Remove duplicates and prioritize anomalies
        
        Args:
            anomalies: List of anomalies
            
        Returns:
            Deduplicated and sorted list
        """
        # Sort by score (descending)
        sorted_anomalies = sorted(anomalies, key=lambda x: x.score, reverse=True)
        
        # Keep top anomalies
        return sorted_anomalies[:50]  # Limit to top 50
