"""
Signals and alerts component
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def render():
    """Render signals and alerts component"""
    st.subheader("🔔 활성 신호 및 알림")
    
    # Mock active signals
    active_signals = [
        {
            'timestamp': (datetime.now() - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M"),
            'scenario': 'Korea Capital Outflow',
            'severity': 'CRITICAL',
            'confidence': 0.85,
            'triggers': '한미 금리차 역전, 원달러 급등, EWY 순유출',
            'recommendation': '포지션 축소 또는 헤지 검토'
        },
        {
            'timestamp': (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            'scenario': 'Volatility Spike',
            'severity': 'WARNING',
            'confidence': 0.78,
            'triggers': 'VIX 급등: +22.5%',
            'recommendation': '단기 변동성 증가, 포지션 사이즈 축소 고려'
        },
        {
            'timestamp': (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
            'scenario': 'Risk Off Transition',
            'severity': 'CRITICAL',
            'confidence': 0.92,
            'triggers': 'VIX 급등, TLT 대량 유입, HYG 스프레드 확대',
            'recommendation': '주식 비중 축소, 현금/단기채 확보'
        }
    ]
    
    # Severity color mapping
    severity_colors = {
        'INFO': '🔵',
        'WARNING': '🟡',
        'CRITICAL': '🔴',
        'EMERGENCY': '🚨'
    }
    
    # Display active signals
    for signal in active_signals:
        severity_icon = severity_colors.get(signal['severity'], '⚪')
        
        with st.expander(f"{severity_icon} {signal['scenario']} - {signal['timestamp']}", expanded=True):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.metric("심각도", signal['severity'])
                st.metric("신뢰도", f"{signal['confidence']:.0%}")
            
            with col2:
                st.markdown(f"**감지된 신호:**")
                st.info(signal['triggers'])
                
                st.markdown(f"**권장사항:**")
                st.warning(signal['recommendation'])
    
    st.markdown("---")
    
    # Alert history
    st.subheader("📊 알림 히스토리")
    
    # Mock history data
    history_data = []
    for i in range(10):
        history_data.append({
            '시간': (datetime.now() - timedelta(hours=i*2)).strftime("%m-%d %H:%M"),
            '시나리오': ['Korea Outflow', 'Risk Off', 'Volatility Spike', 'Liquidity Crisis'][i % 4],
            '심각도': ['CRITICAL', 'WARNING', 'CRITICAL', 'EMERGENCY'][i % 4],
            '신뢰도': f"{(85 - i*2):.0f}%",
            '상태': '✅ 해결' if i > 3 else '⏳ 진행중'
        })
    
    df = pd.DataFrame(history_data)
    
    # Apply styling
    def highlight_severity(row):
        if row['심각도'] == 'EMERGENCY':
            return ['background-color: #8b0000; color: white'] * len(row)
        elif row['심각도'] == 'CRITICAL':
            return ['background-color: #ff6b6b; color: white'] * len(row)
        elif row['심각도'] == 'WARNING':
            return ['background-color: #ffd93d'] * len(row)
        else:
            return [''] * len(row)
    
    st.dataframe(
        df.style.apply(highlight_severity, axis=1),
        use_container_width=True,
        hide_index=True
    )
    
    # Statistics
    st.subheader("📈 알림 통계")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("오늘 알림", "7", delta="-2")
    
    with col2:
        st.metric("이번 주", "34", delta="+5")
    
    with col3:
        st.metric("평균 정확도", "82%", delta="+3%")
    
    with col4:
        st.metric("오경보율", "8%", delta="-1%")
