"""
Market overview component
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def render():
    """Render market overview component"""
    st.subheader("🌍 글로벌 시장 개요")
    
    # Mock data - in production, fetch from API
    market_data = {
        'US': {'Equity': 1.2, 'Bond': -0.3, 'Forex': 0.5, 'Commodity': 0.8},
        'EU': {'Equity': 0.5, 'Bond': -0.1, 'Forex': -0.3, 'Commodity': 0.4},
        'Asia': {'Equity': -0.8, 'Bond': 0.2, 'Forex': -1.2, 'Commodity': -0.5},
        'EM': {'Equity': -1.5, 'Bond': -0.8, 'Forex': -2.1, 'Commodity': -0.3}
    }
    
    # Create heatmap
    df = pd.DataFrame(market_data).T
    
    fig = go.Figure(data=go.Heatmap(
        z=df.values,
        x=df.columns,
        y=df.index,
        colorscale='RdYlGn',
        zmid=0,
        text=df.values,
        texttemplate='%{text:.1f}%',
        textfont={"size": 14},
        colorbar=dict(title="변동률 (%)")
    ))
    
    fig.update_layout(
        title="지역별 자산군 변동률 (24시간)",
        xaxis_title="자산군",
        yaxis_title="지역",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Key indices
    st.subheader("주요 지수")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("S&P 500", "4,567.89", "+1.2%", delta_color="normal")
        st.metric("VIX", "18.5", "-2.3%", delta_color="inverse")
    
    with col2:
        st.metric("나스닥", "14,234.56", "+1.8%", delta_color="normal")
        st.metric("DXY", "103.45", "+0.5%", delta_color="normal")
    
    with col3:
        st.metric("KOSPI", "2,567.34", "-0.8%", delta_color="normal")
        st.metric("USD/KRW", "1,325.50", "+1.2%", delta_color="normal")
    
    with col4:
        st.metric("10Y Treasury", "4.25%", "+0.05%", delta_color="normal")
        st.metric("Gold", "$2,045", "+0.3%", delta_color="normal")
