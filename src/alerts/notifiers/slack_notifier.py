"""
Slack notification service
"""
from typing import Dict
import requests
import logging

logger = logging.getLogger(__name__)


class SlackNotifier:
    """Send alerts to Slack"""
    
    def __init__(self, webhook_url: str, channel: str = None, username: str = "Money Flow Bot"):
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username
    
    def send(self, alert: Dict):
        """
        Send alert to Slack
        
        Args:
            alert: Alert dictionary
        """
        try:
            payload = self._format_slack_message(alert)
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code != 200:
                logger.error(f"Slack API error: {response.status_code} - {response.text}")
            else:
                logger.info(f"Alert sent to Slack: {alert['id']}")
        
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {e}")
    
    def _format_slack_message(self, alert: Dict) -> Dict:
        """
        Format alert as Slack message
        
        Args:
            alert: Alert dictionary
            
        Returns:
            Slack message payload
        """
        # Color based on severity
        color_map = {
            'INFO': '#36a64f',      # Green
            'WARNING': '#ff9900',   # Orange
            'CRITICAL': '#ff0000',  # Red
            'EMERGENCY': '#8b0000'  # Dark red
        }
        
        color = color_map.get(alert['severity'], '#808080')
        
        # Build attachment
        attachment = {
            'color': color,
            'title': f"{alert['scenario'].replace('_', ' ').title()}",
            'text': alert['message'],
            'fields': [
                {
                    'title': '심각도',
                    'value': alert['severity'],
                    'short': True
                },
                {
                    'title': '신뢰도',
                    'value': f"{alert['confidence']:.1%}",
                    'short': True
                }
            ],
            'footer': 'Money Flow Prediction System',
            'ts': int(alert['timestamp'].timestamp()) if hasattr(alert['timestamp'], 'timestamp') else None
        }
        
        payload = {
            'username': self.username,
            'attachments': [attachment]
        }
        
        if self.channel:
            payload['channel'] = self.channel
        
        return payload
