"""
Email notification service
"""
from typing import Dict, List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)


class EmailNotifier:
    """Send alerts via email"""
    
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        from_address: str,
        to_addresses: List[str],
        use_tls: bool = True
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_address = from_address
        self.to_addresses = to_addresses
        self.use_tls = use_tls
    
    def send(self, alert: Dict):
        """
        Send alert via email
        
        Args:
            alert: Alert dictionary
        """
        try:
            msg = self._create_email(alert)
            
            # Connect to SMTP server
            if self.use_tls:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            
            server.login(self.username, self.password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Alert sent via email: {alert['id']}")
        
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
    
    def _create_email(self, alert: Dict) -> MIMEMultipart:
        """
        Create email message
        
        Args:
            alert: Alert dictionary
            
        Returns:
            Email message
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"[{alert['severity']}] {alert['scenario'].replace('_', ' ').title()}"
        msg['From'] = self.from_address
        msg['To'] = ', '.join(self.to_addresses)
        
        # Create HTML content
        html_content = self._format_html_email(alert)
        
        # Create plain text version
        text_content = alert['message']
        
        # Attach both versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        return msg
    
    def _format_html_email(self, alert: Dict) -> str:
        """
        Format alert as HTML email
        
        Args:
            alert: Alert dictionary
            
        Returns:
            HTML string
        """
        severity_colors = {
            'INFO': '#36a64f',
            'WARNING': '#ff9900',
            'CRITICAL': '#ff0000',
            'EMERGENCY': '#8b0000'
        }
        
        color = severity_colors.get(alert['severity'], '#808080')
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: {color}; color: white; padding: 20px; }}
                .content {{ padding: 20px; }}
                .trigger {{ margin: 10px 0; padding: 10px; background-color: #f5f5f5; }}
                .recommendation {{ margin: 20px 0; padding: 15px; background-color: #e3f2fd; border-left: 4px solid #2196f3; }}
                .footer {{ padding: 10px; text-align: center; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>{alert['scenario'].replace('_', ' ').title()}</h2>
                <p>심각도: {alert['severity']} | 신뢰도: {alert['confidence']:.1%}</p>
            </div>
            
            <div class="content">
                <h3>감지된 신호:</h3>
                {''.join(f'<div class="trigger">• {trigger}</div>' for trigger in alert['triggers'])}
                
                <div class="recommendation">
                    <h3>권장사항:</h3>
                    <p>{alert['recommendation']}</p>
                </div>
                
                <p><small>알림 ID: {alert['id']}</small></p>
                <p><small>시간: {alert['timestamp']}</small></p>
            </div>
            
            <div class="footer">
                <p>Money Flow Prediction System</p>
            </div>
        </body>
        </html>
        """
        
        return html
