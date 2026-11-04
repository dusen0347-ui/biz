import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="Supermarket Sales Dashboard", layout="wide")
st.title("🏪 Supermarket Sales 대시보드")

# 2. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    # 같은 폴더의 Sales.xlsx에서 supermarket_sales_test 시트를 불러옵니다.
    df = pd.read_excel("Sales.xlsx", sheet_name="supermarket_sales_test")
    # 결측치 제거
    df = df.dropna()
    return df

try:
    df = load_data()

    # 3. 사이드바 - 지점(Branch) 선택
    st.sidebar.header("필터 설정")
    branches = sorted(df["Branch"].unique())
    selected_branch = st.sidebar.selectbox("지점(Branch) 선택", branches)

    # 선택한 지점 데이터 필터링
    filtered_df = df[df["Branch"] == selected_branch]

    # 4. 주요 KPI Metric 계산
    # 엑셀 파일 내의 정확한 컬럼명(대소문자 포함)을 확인하여 적용하세요.
    # 여기서는 일반적인 'Total', 'Rating' 컬럼명을 기준으로 삼았습니다.
    total_sales = filtered_df["Total"].sum()
    avg_sales = filtered_df["Total"].mean()
    avg_rating = filtered_df["Rating"].mean()

    # Metric 표시
    col1, col2, col3 = st.columns(3)
    col1.metric(label="💰 총 매출", value=f"${total_sales:,.2f}")
    col2.metric(label="📊 평균 매출", value=f"${avg_sales:,.2f}")
    col3.metric(label="⭐ 평균 평점", value=f"{avg_rating:.2f} / 10")

    st.markdown("---")

    # 5. 상품 카테고리(Product line)별 평균 매출 계산 및 시각화
    st.subheader(f"📍 {selected_branch} 지점 - 상품 카테고리별 평균 매출")
    
    category_sales = (
        filtered_df.groupby("Product line")["Total"]
        .mean()
        .reset_index()
        .sort_values(by="Total", ascending=False)
    )

    fig = px.bar(
        category_sales,
        x="Product line",
        y="Total",
        labels={"Total": "평균 매출 ($)", "Product line": "상품 카테고리"},
        color="Total",
        color_continuous_scale="Blues"
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.info("Sales.xlsx 파일이 현재 디렉토리에 있고 시트명이 'supermarket_sales_test'인지 확인해주세요.")
