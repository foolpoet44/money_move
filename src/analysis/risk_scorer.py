"""
Risk scoring system
"""
from typing import Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RiskScorer:
    """Calculate comprehensive risk scores"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.weights = self.config.get('weights', {
            'market_volatility': 0.25,
            'liquidity_risk': 0.25,
            'credit_risk': 0.20,
            'currency_risk': 0.20,
            'geopolitical_risk': 0.10
        })
    
    def calculate_risk_score(self, market_state: Dict) -> Dict:
        """
        Calculate comprehensive risk score
        
        Args:
            market_state: Current market state
            
        Returns:
            Risk score breakdown
        """
        risk_components = {
            'market_volatility': self._score_volatility(market_state),
            'liquidity_risk': self._score_liquidity(market_state),
            'credit_risk': self._score_credit(market_state),
            'currency_risk': self._score_currency(market_state),
            'geopolitical_risk': self._score_geopolitical(market_state)
        }
        
        # Calculate weighted total
        total_score = sum(
            risk_components[key] * self.weights[key]
            for key in risk_components
        )
        
        risk_level = self._categorize_risk(total_score)
        recommendation = self._get_risk_recommendation(total_score, risk_level)
        
        return {
            'total_risk_score': round(total_score, 2),
            'risk_level': risk_level,
            'components': risk_components,
            'recommendation': recommendation,
            'timestamp': datetime.now().isoformat()
        }
    
    def _score_volatility(self, state: Dict) -> float:
        """
        Score market volatility risk (0-100)
        
        Args:
            state: Market state
            
        Returns:
            Volatility risk score
        """
        vix = state.get('vix', 15)
        
        # VIX-based scoring
        if vix < 15:
            score = 10
        elif vix < 20:
            score = 25
        elif vix < 30:
            score = 50
        elif vix < 40:
            score = 75
        else:
            score = 95
        
        # Adjust for VIX trend
        vix_change = state.get('vix_change_5d', 0)
        if vix_change > 20:
            score = min(score + 15, 100)
        
        return float(score)
    
    def _score_liquidity(self, state: Dict) -> float:
        """
        Score liquidity risk (0-100)
        
        Args:
            state: Market state
            
        Returns:
            Liquidity risk score
        """
        score = 20  # Base score
        
        # Bid-ask spreads
        spread_widening = state.get('spread_widening', False)
        if spread_widening:
            score += 25
        
        # Trading volume
        volume_ratio = state.get('volume_ratio', 1.0)
        if volume_ratio < 0.7:  # Low volume
            score += 20
        elif volume_ratio > 1.5:  # Panic volume
            score += 15
        
        # MOVE index (bond volatility)
        move = state.get('move_index', 80)
        if move > 150:
            score += 30
        elif move > 120:
            score += 15
        
        return min(float(score), 100)
    
    def _score_credit(self, state: Dict) -> float:
        """
        Score credit risk (0-100)
        
        Args:
            state: Market state
            
        Returns:
            Credit risk score
        """
        score = 15  # Base score
        
        # High yield spread
        hyg_spread = state.get('hyg_spread', 3.0)
        if hyg_spread > 7:
            score += 40
        elif hyg_spread > 5:
            score += 25
        elif hyg_spread > 4:
            score += 10
        
        # Investment grade spread
        ig_spread = state.get('ig_spread', 1.0)
        if ig_spread > 2:
            score += 20
        elif ig_spread > 1.5:
            score += 10
        
        # Default rate trend
        default_rate_change = state.get('default_rate_change', 0)
        if default_rate_change > 0.5:
            score += 25
        
        return min(float(score), 100)
    
    def _score_currency(self, state: Dict) -> float:
        """
        Score currency risk (0-100)
        
        Args:
            state: Market state
            
        Returns:
            Currency risk score
        """
        score = 20  # Base score
        
        # Dollar strength
        dxy = state.get('dxy', 100)
        dxy_change = state.get('dxy_change_1m', 0)
        
        if dxy_change > 5:  # Strong dollar appreciation
            score += 30
        elif dxy_change > 3:
            score += 15
        
        # Emerging market currencies
        em_fx_stress = state.get('em_fx_stress', False)
        if em_fx_stress:
            score += 25
        
        # Carry trade unwind
        usdjpy_change = state.get('usdjpy_change_1w', 0)
        if abs(usdjpy_change) > 3:  # Rapid yen movement
            score += 20
        
        return min(float(score), 100)
    
    def _score_geopolitical(self, state: Dict) -> float:
        """
        Score geopolitical risk (0-100)
        
        Args:
            state: Market state
            
        Returns:
            Geopolitical risk score
        """
        # This would typically integrate news sentiment analysis
        # Placeholder implementation
        
        score = 30  # Base score
        
        # Oil price volatility (proxy for geopolitical stress)
        oil_volatility = state.get('oil_volatility', 0)
        if oil_volatility > 5:
            score += 25
        
        # Gold as safe haven
        gold_change = state.get('gold_change_1m', 0)
        if gold_change > 10:
            score += 20
        
        return min(float(score), 100)
    
    def _categorize_risk(self, score: float) -> str:
        """
        Categorize risk level
        
        Args:
            score: Total risk score
            
        Returns:
            Risk level category
        """
        if score > 80:
            return "EXTREME"
        elif score > 60:
            return "HIGH"
        elif score > 40:
            return "MODERATE"
        elif score > 20:
            return "LOW"
        else:
            return "MINIMAL"
    
    def _get_risk_recommendation(self, score: float, level: str) -> str:
        """
        Get recommendation based on risk level
        
        Args:
            score: Risk score
            level: Risk level
            
        Returns:
            Recommendation string
        """
        recommendations = {
            "EXTREME": "🔴 최고 위험 수준. 방어적 포지션 필수. 현금 비중 최대화. 헤지 전략 즉시 실행.",
            "HIGH": "🟠 높은 위험. 포지션 축소 권장. 변동성 대비 필요. 손절매 라인 엄격히 준수.",
            "MODERATE": "🟡 중간 위험. 신중한 접근 필요. 분산 투자 유지. 시장 모니터링 강화.",
            "LOW": "🟢 낮은 위험. 정상적인 포지션 운용 가능. 기회 포착 준비.",
            "MINIMAL": "🔵 최소 위험. 공격적 전략 가능. 성장 기회 적극 활용."
        }
        
        return recommendations.get(level, "리스크 평가 필요")
