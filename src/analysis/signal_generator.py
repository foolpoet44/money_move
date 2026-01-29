"""
Signal generation system
"""
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class Signal:
    """Trading/Market signal"""
    scenario: str
    severity: str  # 'info', 'warning', 'critical', 'emergency'
    confidence: float  # 0-1
    triggers: List[str]
    recommendation: str
    timestamp: datetime
    metadata: Dict


class SignalGenerator:
    """Generate market signals based on scenarios"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.signal_rules = self._load_signal_rules()
    
    def _load_signal_rules(self) -> Dict:
        """Load signal generation rules from config"""
        return {
            'korea_outflow': {
                'rate_diff_threshold': -0.5,
                'usdkrw_change_threshold': 1.0,
                'ewy_flow_days': 3
            },
            'risk_off': {
                'vix_threshold': 30,
                'hyg_spread_threshold': 5.0
            },
            'liquidity_crisis': {
                'libor_ois_threshold': 0.5,
                'move_threshold': 150
            }
        }
    
    def generate_signals(self, market_state: Dict) -> List[Signal]:
        """
        Generate signals based on market state
        
        Args:
            market_state: Current market state dictionary
            
        Returns:
            List of generated signals
        """
        signals = []
        
        # Scenario A: Korea capital outflow
        korea_signal = self._check_korea_outflow(market_state)
        if korea_signal:
            signals.append(korea_signal)
        
        # Scenario B: Risk-off transition
        risk_off_signal = self._check_risk_off(market_state)
        if risk_off_signal:
            signals.append(risk_off_signal)
        
        # Scenario C: Liquidity crisis
        liquidity_signal = self._check_liquidity_crisis(market_state)
        if liquidity_signal:
            signals.append(liquidity_signal)
        
        # Additional scenarios
        volatility_signal = self._check_volatility_spike(market_state)
        if volatility_signal:
            signals.append(volatility_signal)
        
        logger.info(f"Generated {len(signals)} signals")
        return signals
    
    def _check_korea_outflow(self, state: Dict) -> Signal:
        """
        Check for Korea capital outflow scenario
        
        Args:
            state: Market state
            
        Returns:
            Signal if conditions met, None otherwise
        """
        triggers = []
        conditions_met = 0
        
        # Check rate differential
        rate_diff = state.get('korea_us_rate_diff', 0)
        if rate_diff < self.signal_rules['korea_outflow']['rate_diff_threshold']:
            triggers.append(f"한미 금리차 역전: {rate_diff:.2f}%p")
            conditions_met += 1
        
        # Check USDKRW movement
        usdkrw_change = state.get('usdkrw_change_1d', 0)
        if usdkrw_change > self.signal_rules['korea_outflow']['usdkrw_change_threshold']:
            triggers.append(f"원달러 급등: +{usdkrw_change:.2f}%")
            conditions_met += 1
        
        # Check EWY flows
        ewy_flow = state.get('ewy_flow_3d', 0)
        if ewy_flow < 0:
            triggers.append(f"EWY ETF 순유출: {ewy_flow:,.0f}")
            conditions_met += 1
        
        # Check foreign investor flows
        kospi_foreign = state.get('kospi_foreign_flow', 0)
        if kospi_foreign < 0:
            triggers.append(f"KOSPI 외국인 순매도: {kospi_foreign:,.0f}억원")
            conditions_met += 1
        
        # Generate signal if 3+ conditions met
        if conditions_met >= 3:
            confidence = min(conditions_met / 4, 1.0)
            
            return Signal(
                scenario="korea_capital_outflow",
                severity="critical" if conditions_met == 4 else "warning",
                confidence=confidence,
                triggers=triggers,
                recommendation="포지션 축소 또는 헤지 검토. 원화 약세 대비 필요.",
                timestamp=datetime.now(),
                metadata={
                    'conditions_met': conditions_met,
                    'total_conditions': 4
                }
            )
        
        return None
    
    def _check_risk_off(self, state: Dict) -> Signal:
        """
        Check for risk-off transition
        
        Args:
            state: Market state
            
        Returns:
            Signal if conditions met
        """
        triggers = []
        conditions_met = 0
        
        # VIX spike
        vix = state.get('vix', 0)
        if vix > self.signal_rules['risk_off']['vix_threshold']:
            triggers.append(f"VIX 급등: {vix:.1f}")
            conditions_met += 1
        
        # TLT inflows
        tlt_flow = state.get('tlt_flow', 0)
        if tlt_flow > 0:
            triggers.append(f"TLT 대량 유입: +{tlt_flow:,.0f}")
            conditions_met += 1
        
        # HYG spread widening
        hyg_spread = state.get('hyg_spread', 0)
        if hyg_spread > self.signal_rules['risk_off']['hyg_spread_threshold']:
            triggers.append(f"하이일드 스프레드 확대: {hyg_spread:.2f}%p")
            conditions_met += 1
        
        # Gold + Dollar strength
        gold_change = state.get('gold_change', 0)
        dxy_change = state.get('dxy_change', 0)
        if gold_change > 1 and dxy_change > 0.5:
            triggers.append("금 가격 상승 + 달러 강세 동시 발생")
            conditions_met += 1
        
        if conditions_met >= 3:
            return Signal(
                scenario="risk_off_transition",
                severity="critical",
                confidence=min(conditions_met / 4, 1.0),
                triggers=triggers,
                recommendation="주식 비중 축소, 현금/단기채 확보. 변동성 낮아질 때까지 대기.",
                timestamp=datetime.now(),
                metadata={'conditions_met': conditions_met}
            )
        
        return None
    
    def _check_liquidity_crisis(self, state: Dict) -> Signal:
        """
        Check for liquidity crisis signs
        
        Args:
            state: Market state
            
        Returns:
            Signal if conditions met
        """
        triggers = []
        conditions_met = 0
        
        # LIBOR-OIS spread
        libor_ois = state.get('libor_ois_spread', 0)
        if libor_ois > self.signal_rules['liquidity_crisis']['libor_ois_threshold']:
            triggers.append(f"LIBOR-OIS 스프레드 급등: {libor_ois:.2f}%p")
            conditions_met += 1
        
        # Repo rate spike
        repo_spike = state.get('repo_rate_spike', False)
        if repo_spike:
            triggers.append("레포 금리 스파이크 감지")
            conditions_met += 1
        
        # MOVE index
        move_index = state.get('move_index', 0)
        if move_index > self.signal_rules['liquidity_crisis']['move_threshold']:
            triggers.append(f"MOVE 지수 급등: {move_index:.1f}")
            conditions_met += 1
        
        # Corporate bond issuance drop
        bond_issuance = state.get('corp_bond_issuance_change', 0)
        if bond_issuance < -50:
            triggers.append(f"회사채 발행 급감: {bond_issuance:.1f}%")
            conditions_met += 1
        
        if conditions_met >= 2:
            return Signal(
                scenario="liquidity_crisis",
                severity="emergency",
                confidence=min(conditions_met / 4, 1.0),
                triggers=triggers,
                recommendation="⚠️ 극도로 보수적 포지션 필요. 현금 확보 최우선. 2008년 금융위기 패턴 유사.",
                timestamp=datetime.now(),
                metadata={
                    'conditions_met': conditions_met,
                    'crisis_level': 'severe' if conditions_met >= 3 else 'moderate'
                }
            )
        
        return None
    
    def _check_volatility_spike(self, state: Dict) -> Signal:
        """
        Check for general volatility spike
        
        Args:
            state: Market state
            
        Returns:
            Signal if conditions met
        """
        vix = state.get('vix', 0)
        vix_change = state.get('vix_change_1d', 0)
        
        # Significant VIX spike
        if vix_change > 20:  # 20% increase in VIX
            return Signal(
                scenario="volatility_spike",
                severity="warning",
                confidence=0.8,
                triggers=[f"VIX 급등: +{vix_change:.1f}% (현재: {vix:.1f})"],
                recommendation="단기 변동성 증가. 포지션 사이즈 축소 고려.",
                timestamp=datetime.now(),
                metadata={'vix': vix, 'vix_change': vix_change}
            )
        
        return None
