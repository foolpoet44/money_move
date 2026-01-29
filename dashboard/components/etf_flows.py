"""
ETF flows component
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta


def render():
    """Render ETF flows component"""
    st.subheader("💸 ETF 자금 흐름 분석")
    
    # Mock data
    etf_data = {
        'SPY': {'flow': 1250000000, 'change': 2.5, 'trend': 'inflow'},
        'QQQ': {'flow': 890000000, 'change': 1.8, 'trend': 'inflow'},
        'TLT': {'flow': -450000000, 'change': -1.2, 'trend': 'outflow'},
        'HYG': {'flow': -320000000, 'change': -0.9, 'trend': 'outflow'},
        'EWY': {'flow': -180000000, 'change': -1.5, 'trend': 'outflow'},
        'GLD': {'flow': 210000000, 'change': 0.8, 'trend': 'inflow'}
    }
    
    # Flow chart
    symbols = list(etf_data.keys())
    flows = [etf_data[s]['flow'] / 1e6 for s in symbols]  # Convert to millions
    colors = ['green' if etf_data[s]['trend'] == 'inflow' else 'red' for s in symbols]
    
    fig = go.Figure(data=[
        go.Bar(
            x=symbols,
            y=flows,
            marker_color=colors,
            text=[f"${abs(f):.0f}M" for f in flows],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="ETF 순자금 흐름 (24시간)",
        xaxis_title="ETF",
        yaxis_title="순흐름 (백만 달러)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.subheader("상세 흐름 데이터")
    
    df = pd.DataFrame([
        {
            'ETF': symbol,
            '순흐름 ($M)': f"${etf_data[symbol]['flow'] / 1e6:,.0f}",
            '가격 변동 (%)': f"{etf_data[symbol]['change']:+.2f}%",
            '트렌드': '📈 유입' if etf_data[symbol]['trend'] == 'inflow' else '📉 유출'
        }
        for symbol in symbols
    ])
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Sankey diagram for sector rotation
    st.subheader("섹터 로테이션")
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            label=["주식", "채권", "기술", "금융", "에너지", "헬스케어"],
            color=["blue", "green", "purple", "orange", "red", "cyan"]
        ),
        link=dict(
            source=[0, 0, 1, 1, 0],
            target=[2, 3, 3, 4, 5],
            value=[1250, 890, 450, 320, 180],
            color=["rgba(0,0,255,0.3)", "rgba(0,255,0,0.3)", 
                   "rgba(255,0,0,0.3)", "rgba(255,165,0,0.3)", "rgba(0,255,255,0.3)"]
        )
    )])
    
    fig.update_layout(
        title="자금 이동 경로",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
