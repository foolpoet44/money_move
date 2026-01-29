"""
Predictions component
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def render():
    """Render predictions component"""
    st.subheader("🔮 자금 흐름 예측")
    
    # Prediction horizons
    horizon = st.selectbox(
        "예측 기간 선택",
        ["24시간", "48시간", "1주일"],
        index=0
    )
    
    # Mock prediction data
    prediction = {
        'direction': 'outflow',
        'confidence': 0.73,
        'probability_distribution': {
            'outflow': 0.55,
            'neutral': 0.28,
            'inflow': 0.17
        }
    }
    
    # Probability distribution chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        categories = ['유출 (Outflow)', '중립 (Neutral)', '유입 (Inflow)']
        probabilities = [
            prediction['probability_distribution']['outflow'] * 100,
            prediction['probability_distribution']['neutral'] * 100,
            prediction['probability_distribution']['inflow'] * 100
        ]
        colors = ['#ff6b6b', '#95a5a6', '#51cf66']
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=probabilities,
                marker_color=colors,
                text=[f"{p:.1f}%" for p in probabilities],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title=f"자금 흐름 방향 예측 ({horizon})",
            yaxis_title="확률 (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("예측 방향", "📉 유출", delta=None)
        st.metric("신뢰도", f"{prediction['confidence']:.0%}")
        
        st.markdown("---")
        
        st.markdown("**주요 영향 요인:**")
        st.markdown("• 한미 금리차 확대")
        st.markdown("• 달러 강세")
        st.markdown("• VIX 상승")
    
    # Time series forecast
    st.subheader("시계열 예측")
    
    # Generate mock time series data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now() + timedelta(days=7), freq='D')
    historical = np.random.randn(30).cumsum() + 100
    forecast = np.random.randn(8).cumsum() + historical[-1]
    
    # Confidence intervals
    upper_bound = forecast + np.random.rand(8) * 5
    lower_bound = forecast - np.random.rand(8) * 5
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=dates[:30],
        y=historical,
        mode='lines',
        name='실제 데이터',
        line=dict(color='blue', width=2)
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=dates[30:],
        y=forecast,
        mode='lines',
        name='예측',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    # Confidence interval
    fig.add_trace(go.Scatter(
        x=dates[30:],
        y=upper_bound,
        mode='lines',
        name='상한',
        line=dict(width=0),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=dates[30:],
        y=lower_bound,
        mode='lines',
        name='하한',
        line=dict(width=0),
        fillcolor='rgba(255,0,0,0.2)',
        fill='tonexty',
        showlegend=True
    ))
    
    fig.update_layout(
        title="자금 흐름 지수 예측",
        xaxis_title="날짜",
        yaxis_title="지수",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Similar historical episodes
    st.subheader("유사 과거 사례")
    
    similar_episodes = [
        {
            '기간': '2023-03-10 ~ 2023-03-17',
            '시나리오': 'SVB 사태',
            '유사도': '87%',
            '결과': '📉 7일간 -12% 하락'
        },
        {
            '기간': '2022-09-20 ~ 2022-09-27',
            '시나리오': '영국 국채 위기',
            '유사도': '75%',
            '결과': '📉 5일간 -8% 하락'
        },
        {
            '기간': '2020-03-09 ~ 2020-03-16',
            '시나리오': 'COVID-19 팬데믹',
            '유사도': '62%',
            '결과': '📉 14일간 -28% 하락'
        }
    ]
    
    df = pd.DataFrame(similar_episodes)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.info("💡 현재 시장 상황은 과거 유사 사례와 비교했을 때 중간 수준의 리스크를 나타내고 있습니다.")
