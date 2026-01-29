"""
Streamlit Dashboard for Money Flow Prediction System
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard.components import market_overview, etf_flows, signals, predictions


# Page configuration
st.set_page_config(
    page_title="Money Flow Prediction System",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .risk-extreme { color: #8b0000; font-weight: bold; }
    .risk-high { color: #ff0000; font-weight: bold; }
    .risk-moderate { color: #ff9900; font-weight: bold; }
    .risk-low { color: #36a64f; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


def render_header():
    """Render dashboard header"""
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col1:
        st.metric("시스템 상태", "🟢 정상", delta="99.9% 가동률")
    
    with col2:
        st.markdown('<div class="main-header">💰 Money Flow Prediction System</div>', unsafe_allow_html=True)
    
    with col3:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.metric("현재 시각", current_time)


def render_risk_dashboard():
    """Render risk score dashboard"""
    st.subheader("🎯 종합 리스크 스코어")
    
    # Mock data - in production, fetch from API
    risk_data = {
        'total_risk_score': 45.2,
        'risk_level': 'MODERATE',
        'components': {
            'market_volatility': 52,
            'liquidity_risk': 38,
            'credit_risk': 42,
            'currency_risk': 48,
            'geopolitical_risk': 35
        }
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Risk gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risk_data['total_risk_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "종합 리스크"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 20], 'color': "lightgreen"},
                    {'range': [20, 40], 'color': "lightyellow"},
                    {'range': [40, 60], 'color': "orange"},
                    {'range': [60, 80], 'color': "lightcoral"},
                    {'range': [80, 100], 'color': "darkred"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk level
        risk_class = f"risk-{risk_data['risk_level'].lower()}"
        st.markdown(f'<p class="{risk_class}">리스크 수준: {risk_data["risk_level"]}</p>', unsafe_allow_html=True)
    
    with col2:
        # Component breakdown
        components_df = pd.DataFrame([
            {'Component': k.replace('_', ' ').title(), 'Score': v}
            for k, v in risk_data['components'].items()
        ])
        
        fig = px.bar(
            components_df,
            x='Score',
            y='Component',
            orientation='h',
            title='리스크 구성 요소',
            color='Score',
            color_continuous_scale='RdYlGn_r'
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)


def main():
    """Main dashboard function"""
    
    # Header
    render_header()
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ 설정")
        
        # Refresh interval
        refresh_interval = st.slider("새로고침 간격 (초)", 10, 300, 60)
        
        # Asset class filter
        st.subheader("자산군 필터")
        show_equity = st.checkbox("주식", value=True)
        show_bonds = st.checkbox("채권", value=True)
        show_forex = st.checkbox("외환", value=True)
        show_commodities = st.checkbox("원자재", value=False)
        
        # Time range
        st.subheader("시간 범위")
        time_range = st.selectbox(
            "기간 선택",
            ["1일", "1주일", "1개월", "3개월", "1년"]
        )
        
        st.markdown("---")
        
        # Quick stats
        st.subheader("📊 빠른 통계")
        st.metric("활성 신호", "3", delta="+1")
        st.metric("오늘 알림", "7", delta="-2")
        st.metric("데이터 포인트", "1,234", delta="+234")
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["📊 시장 개요", "💸 자금 흐름", "🔔 신호 & 알림", "🔮 예측"])
    
    with tab1:
        render_risk_dashboard()
        st.markdown("---")
        market_overview.render()
    
    with tab2:
        etf_flows.render()
    
    with tab3:
        signals.render()
    
    with tab4:
        predictions.render()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666; font-size: 0.9rem;">'
        '💰 Money Flow Prediction System v0.1.0 | '
        '"물의 흐름을 읽는 자가 시장을 지배한다"'
        '</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
