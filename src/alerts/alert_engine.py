"""
Alert engine for market signals
"""
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = 1
    WARNING = 2
    CRITICAL = 3
    EMERGENCY = 4


class AlertEngine:
    """Alert generation and dispatch system"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.alert_rules = self._load_alert_rules()
        self.notifiers = {}
        self.alert_history = []
        
    def _load_alert_rules(self) -> Dict:
        """Load alert rules from config"""
        return {
            'severity_thresholds': {
                'info': 0.0,
                'warning': 0.4,
                'critical': 0.6,
                'emergency': 0.8
            },
            'rate_limiting': {
                'max_alerts_per_hour': 10,
                'cooldown_minutes': 15
            }
        }
    
    def register_notifier(self, name: str, notifier):
        """
        Register a notification channel
        
        Args:
            name: Notifier name (e.g., 'slack', 'email')
            notifier: Notifier instance
        """
        self.notifiers[name] = notifier
        logger.info(f"Registered notifier: {name}")
    
    def evaluate_alerts(self, signals: List) -> List[Dict]:
        """
        Evaluate signals and generate alerts
        
        Args:
            signals: List of Signal objects
            
        Returns:
            List of generated alerts
        """
        alerts = []
        
        for signal in signals:
            severity = self._calculate_severity(signal)
            
            if severity.value >= AlertSeverity.WARNING.value:
                alert = self._create_alert(signal, severity)
                alerts.append(alert)
                
                # Dispatch alert
                self._dispatch_alert(alert)
        
        logger.info(f"Generated {len(alerts)} alerts from {len(signals)} signals")
        return alerts
    
    def _calculate_severity(self, signal) -> AlertSeverity:
        """
        Calculate alert severity from signal
        
        Args:
            signal: Signal object
            
        Returns:
            AlertSeverity enum
        """
        confidence = signal.confidence
        
        # Map signal severity to AlertSeverity
        severity_map = {
            'info': AlertSeverity.INFO,
            'warning': AlertSeverity.WARNING,
            'critical': AlertSeverity.CRITICAL,
            'emergency': AlertSeverity.EMERGENCY
        }
        
        signal_severity = severity_map.get(signal.severity, AlertSeverity.INFO)
        
        # Adjust based on confidence
        if confidence > 0.9 and signal_severity.value < AlertSeverity.EMERGENCY.value:
            return AlertSeverity(signal_severity.value + 1)
        
        return signal_severity
    
    def _create_alert(self, signal, severity: AlertSeverity) -> Dict:
        """
        Create alert dictionary
        
        Args:
            signal: Signal object
            severity: AlertSeverity
            
        Returns:
            Alert dictionary
        """
        alert_id = str(uuid.uuid4())
        
        alert = {
            'id': alert_id,
            'timestamp': datetime.now().isoformat(),
            'severity': severity.name,
            'scenario': signal.scenario,
            'confidence': signal.confidence,
            'message': self._format_alert_message(signal),
            'triggers': signal.triggers,
            'recommendation': signal.recommendation,
            'metadata': signal.metadata
        }
        
        # Add to history
        self.alert_history.append(alert)
        
        return alert
    
    def _format_alert_message(self, signal) -> str:
        """
        Format alert message
        
        Args:
            signal: Signal object
            
        Returns:
            Formatted message string
        """
        emoji_map = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'critical': '🔴',
            'emergency': '🚨'
        }
        
        emoji = emoji_map.get(signal.severity, '📊')
        
        message = f"{emoji} **{signal.scenario.replace('_', ' ').title()}**\n\n"
        message += f"신뢰도: {signal.confidence:.1%}\n\n"
        message += "**감지된 신호:**\n"
        
        for trigger in signal.triggers:
            message += f"• {trigger}\n"
        
        message += f"\n**권장사항:**\n{signal.recommendation}"
        
        return message
    
    def _dispatch_alert(self, alert: Dict):
        """
        Dispatch alert to configured channels
        
        Args:
            alert: Alert dictionary
        """
        severity = AlertSeverity[alert['severity']]
        
        # Determine which channels to use based on severity
        channels_to_use = []
        
        if severity == AlertSeverity.EMERGENCY:
            channels_to_use = list(self.notifiers.keys())  # All channels
        elif severity == AlertSeverity.CRITICAL:
            channels_to_use = ['slack', 'email']
        elif severity == AlertSeverity.WARNING:
            channels_to_use = ['slack']
        
        # Send to each channel
        for channel in channels_to_use:
            if channel in self.notifiers:
                try:
                    self.notifiers[channel].send(alert)
                    logger.info(f"Alert {alert['id']} sent to {channel}")
                except Exception as e:
                    logger.error(f"Failed to send alert to {channel}: {e}")
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """
        Get recent alerts
        
        Args:
            limit: Maximum number of alerts to return
            
        Returns:
            List of recent alerts
        """
        return self.alert_history[-limit:]
    
    def clear_history(self):
        """Clear alert history"""
        self.alert_history.clear()
        logger.info("Alert history cleared")
