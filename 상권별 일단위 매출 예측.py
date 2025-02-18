import pandas as pd
from prophet import Prophet
import numpy as np


# 파일 경로 설정
file_path = r"C:\Users\dlwlg\Desktop\머신러닝 사용 데이터\피처엔지니어링한통합데이터\피처엔지니어링일단다한통합데이터.csv"

# 데이터 로드
df = pd.read_csv(file_path)

# 필요한 칼럼 선택
df = df[['기준_년분기_코드', '상권_코드_명', '서비스_업종_코드_명', 
          '월요일_매출_금액', '화요일_매출_금액', '수요일_매출_금액', 
          '목요일_매출_금액', '금요일_매출_금액', '토요일_매출_금액', '일요일_매출_금액']]

# 기준_년분기_코드를 날짜로 변환 (각 분기의 첫 번째 날)
def convert_quarter_to_date(quarter_code):
    year = int(str(quarter_code)[:4])
    quarter = int(str(quarter_code)[4:])
    month = {1: '01', 2: '04', 3: '07', 4: '10'}[quarter]
    return f"{year}-{month}-01"

df['날짜'] = df['기준_년분기_코드'].apply(convert_quarter_to_date)
df['날짜'] = pd.to_datetime(df['날짜'])

# 분기별 실제 날짜 수 계산
start_date = pd.to_datetime("2019-01-01")
end_date = pd.to_datetime("2024-06-30")

# 전체 날짜 범위 데이터프레임 생성
date_range = pd.date_range(start=start_date, end=end_date, freq='D')
date_info_df = pd.DataFrame({'날짜': date_range})
date_info_df['요일'] = date_info_df['날짜'].dt.strftime('%A')

# 원본 데이터와 날짜 범위 데이터프레임 병합
daily_sales_list = []

for _, row in df.iterrows():
    base_date = row['날짜']
    quarter_mask = (date_info_df['날짜'] >= base_date) & (date_info_df['날짜'] < base_date + pd.DateOffset(months=3))
    quarter_dates = date_info_df[quarter_mask]

    sales_values = [row['월요일_매출_금액'], row['화요일_매출_금액'], row['수요일_매출_금액'],
                     row['목요일_매출_금액'], row['금요일_매출_금액'], row['토요일_매출_금액'], row['일요일_매출_금액']]

    # 요일별 매출 매핑
    weekday_sales_map = dict(zip(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], sales_values))

    for date in quarter_dates['날짜']:
        weekday = date.strftime('%A')
        sales_value = weekday_sales_map[weekday] / quarter_dates['요일'].value_counts()[weekday]
        daily_sales_list.append({
            '날짜': date,
            '요일': weekday,
            '상권명': row['상권_코드_명'],
            '업종': row['서비스_업종_코드_명'],
            '매출': sales_value
        })

# 데이터프레임 변환
daily_sales_df = pd.DataFrame(daily_sales_list)

# Prophet 모델링 및 결과 예측
prophet_results = []

for (district, industry), group in daily_sales_df.groupby(['상권명', '업종']):
    prophet_df = group[['날짜', '매출']].rename(columns={'날짜': 'ds', '매출': 'y'})
    model = Prophet()
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=90)  # 향후 90일 예측
    forecast = model.predict(future)

    forecast = forecast[['ds', 'yhat']].rename(columns={'ds': '날짜', 'yhat': '예측_매출'})
    forecast['상권명'] = district
    forecast['업종'] = industry
    prophet_results.append(forecast)

# 예측 결과 데이터프레임으로 변환
forecast_df = pd.concat(prophet_results)

# 결과 저장
output_file = r"C:\Users\dlwlg\Desktop\머신러닝 사용 데이터\피처엔지니어링한통합데이터\Prophet_예측_결과.csv"
forecast_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print("Prophet 모델링 및 데이터 저장이 완료되었습니다.")