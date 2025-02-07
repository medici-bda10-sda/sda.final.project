## 자치구단위 서울생활인구 일별 집계표 크롤링

import requests
import csv
import time

# API 정보
API_KEY = "56777a6c6a776a6437306c716f6a62"  # 발급받은 인증키
SERVICE_NAME = "SPOP_DAILYSUM_JACHI"
DATA_TYPE = "json"
START_INDEX = 1
END_INDEX = 1000  # API에서 한 번에 최대 1000개까지 제공
FILENAME = "seoul_population_all.csv"

# CSV 파일 헤더
HEADER = [
    "기준일ID", "시군구코드", "시군구명", "총생활인구수", "내국인생활인구수",
    "장기체류외국인인구수", "단기체류외국인인구수", "일최대인구수", "일최소인구수",
    "주간인구수", "야간인구수", "일최대이동인구수", "서울외유입인구수",
    "동일자치구행정동간이동인구수", "자치구간이동인구수"
]

# CSV 파일 생성 및 헤더 작성
with open(FILENAME, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(HEADER)

    while True:
        # API 요청 URL
        url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/{DATA_TYPE}/{SERVICE_NAME}/{START_INDEX}/{END_INDEX}/"

        # API 호출
        response = requests.get(url)

        if response.status_code != 200:
            print(f"API 요청 실패: {response.status_code}")
            break

        data = response.json()

        # 데이터 존재 여부 확인
        if "SPOP_DAILYSUM_JACHI" not in data or "row" not in data["SPOP_DAILYSUM_JACHI"]:
            print("데이터가 더 이상 없습니다.")
            break

        rows = data["SPOP_DAILYSUM_JACHI"]["row"]

        # CSV에 데이터 저장
        for row in rows:
            writer.writerow([
                row["STDR_DE_ID"], row["SIGNGU_CODE_SE"], row["SIGNGU_NM"], row["TOT_LVPOP_CO"],
                row["LVPOP_CO"], row["LNGTR_STAY_FRGNR_CO"], row["SRTPD_STAY_FRGNR_CO"],
                row["DAIL_MXMM_LVPOP_CO"], row["DAIL_MUMM_LVPOP_CO"], row["DAY_LVPOP_CO"],
                row["NIGHT_LVPOP_CO"], row["DAIL_MXMM_MVMN_LVPOP_CO"], row["SU_ELSE_INFLOW_LVPOP_CO"],
                row["SAM_ADSTRD_MVMN_LVPOP_CO"], row["SIGNGU_MVMN_LVPOP_CO"]
            ])

        # 현재 가져온 데이터 개수가 1000개보다 적다면 더 이상 데이터가 없음
        if len(rows) < 1000:
            print("모든 데이터를 성공적으로 가져왔습니다.")
            break

        # 다음 페이지 요청을 위해 인덱스 증가
        START_INDEX += 1000
        END_INDEX += 1000

        print(f"{START_INDEX} ~ {END_INDEX} 데이터 가져오는 중...")

        # API 호출 제한 방지를 위한 딜레이 (필요 시 활성화)
        time.sleep(1)

print(f"CSV 파일 저장 완료: {FILENAME}")

## 서울시_상권분석_서비스(추정매출-자치구) 크롤링

import requests
import csv
import time

# API 정보
API_KEY = "56777a6c6a776a6437306c716f6a62"  # 발급받은 인증키
SERVICE_NAME = "VwsmSignguSelngW"
DATA_TYPE = "json"
START_INDEX = 1
END_INDEX = 1000  # API에서 한 번에 최대 1000개까지 제공
FILENAME = "seoul_card_sales.csv"

# CSV 파일 헤더
HEADER = [
    "기준_년분기_코드", "자치구_코드", "자치구_코드_명", "서비스_업종_코드", "서비스_업종_코드_명",
    "당월_매출_금액", "당월_매출_건수", "주중_매출_금액", "주말_매출_금액",
    "월요일_매출_금액", "화요일_매출_금액", "수요일_매출_금액", "목요일_매출_금액",
    "금요일_매출_금액", "토요일_매출_금액", "일요일_매출_금액",
    "시간대_00~06_매출_금액", "시간대_06~11_매출_금액", "시간대_11~14_매출_금액",
    "시간대_14~17_매출_금액", "시간대_17~21_매출_금액", "시간대_21~24_매출_금액",
    "남성_매출_금액", "여성_매출_금액",
    "연령대_10_매출_금액", "연령대_20_매출_금액", "연령대_30_매출_금액",
    "연령대_40_매출_금액", "연령대_50_매출_금액", "연령대_60_이상_매출_금액",
    "주중_매출_건수", "주말_매출_건수",
    "월요일_매출_건수", "화요일_매출_건수", "수요일_매출_건수", "목요일_매출_건수",
    "금요일_매출_건수", "토요일_매출_건수", "일요일_매출_건수",
    "시간대_건수~06_매출_건수", "시간대_건수~11_매출_건수", "시간대_건수~14_매출_건수",
    "시간대_건수~17_매출_건수", "시간대_건수~21_매출_건수", "시간대_건수~24_매출_건수",
    "남성_매출_건수", "여성_매출_건수",
    "연령대_10_매출_건수", "연령대_20_매출_건수", "연령대_30_매출_건수",
    "연령대_40_매출_건수", "연령대_50_매출_건수", "연령대_60_이상_매출_건수"
]

# CSV 파일 생성 및 헤더 작성
with open(FILENAME, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(HEADER)

    while True:
        # API 요청 URL
        url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/{DATA_TYPE}/{SERVICE_NAME}/{START_INDEX}/{END_INDEX}/"

        # API 호출
        response = requests.get(url)

        if response.status_code != 200:
            print(f"API 요청 실패: {response.status_code}")
            break

        data = response.json()

        # 데이터 존재 여부 확인
        if SERVICE_NAME not in data or "row" not in data[SERVICE_NAME]:
            print("데이터가 더 이상 없습니다.")
            break

        rows = data[SERVICE_NAME]["row"]

        # CSV에 데이터 저장
        for row in rows:
            writer.writerow([
                row["STDR_YYQU_CD"], row["SIGNGU_CD"], row["SIGNGU_CD_NM"],
                row["SVC_INDUTY_CD"], row["SVC_INDUTY_CD_NM"],
                row["THSMON_SELNG_AMT"], row["THSMON_SELNG_CO"],
                row["MDWK_SELNG_AMT"], row["WKEND_SELNG_AMT"],
                row["MON_SELNG_AMT"], row["TUES_SELNG_AMT"], row["WED_SELNG_AMT"],
                row["THUR_SELNG_AMT"], row["FRI_SELNG_AMT"], row["SAT_SELNG_AMT"], row["SUN_SELNG_AMT"],
                row["TMZON_00_06_SELNG_AMT"], row["TMZON_06_11_SELNG_AMT"],
                row["TMZON_11_14_SELNG_AMT"], row["TMZON_14_17_SELNG_AMT"],
                row["TMZON_17_21_SELNG_AMT"], row["TMZON_21_24_SELNG_AMT"],
                row["ML_SELNG_AMT"], row["FML_SELNG_AMT"],
                row["AGRDE_10_SELNG_AMT"], row["AGRDE_20_SELNG_AMT"],
                row["AGRDE_30_SELNG_AMT"], row["AGRDE_40_SELNG_AMT"],
                row["AGRDE_50_SELNG_AMT"], row["AGRDE_60_ABOVE_SELNG_AMT"],
                row["MDWK_SELNG_CO"], row["WKEND_SELNG_CO"],
                row["MON_SELNG_CO"], row["TUES_SELNG_CO"], row["WED_SELNG_CO"],
                row["THUR_SELNG_CO"], row["FRI_SELNG_CO"], row["SAT_SELNG_CO"], row["SUN_SELNG_CO"],
                row["TMZON_00_06_SELNG_CO"], row["TMZON_06_11_SELNG_CO"],
                row["TMZON_11_14_SELNG_CO"], row["TMZON_14_17_SELNG_CO"],
                row["TMZON_17_21_SELNG_CO"], row["TMZON_21_24_SELNG_CO"],
                row["ML_SELNG_CO"], row["FML_SELNG_CO"],
                row["AGRDE_10_SELNG_CO"], row["AGRDE_20_SELNG_CO"],
                row["AGRDE_30_SELNG_CO"], row["AGRDE_40_SELNG_CO"],
                row["AGRDE_50_SELNG_CO"], row["AGRDE_60_ABOVE_SELNG_CO"]
            ])

        # 현재 가져온 데이터 개수가 1000개보다 적다면 더 이상 데이터가 없음
        if len(rows) < 1000:
            print("모든 데이터를 성공적으로 가져왔습니다.")
            break

        # 다음 페이지 요청을 위해 인덱스 증가
        START_INDEX += 1000
        END_INDEX += 1000

        print(f"{START_INDEX} ~ {END_INDEX} 데이터 가져오는 중...")

        # API 호출 제한 방지를 위한 딜레이 (필요 시 활성화)
        time.sleep(1)

## 서울시_상권분석_서비스(점포-자치구) 크롤링

import requests
import csv
import time

# API 정보
API_KEY = "56777a6c6a776a6437306c716f6a62"  # 발급받은 인증키
SERVICE_NAME = "VwsmSignguStorW"
DATA_TYPE = "json"
START_INDEX = 1
END_INDEX = 1000  # API에서 한 번에 최대 1000개까지 제공
FILENAME = "seoul_store_data.csv"

# CSV 파일 헤더
HEADER = [
    "기준_년분기_코드", "자치구_코드", "자치구_코드_명", "서비스_업종_코드", "서비스_업종_코드_명",
    "점포_수", "유사_업종_점포_수", "개업_율", "개업_점포_수",
    "폐업_률", "폐업_점포_수", "프랜차이즈_점포_수"
]

# CSV 파일 생성 및 헤더 작성
with open(FILENAME, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(HEADER)

    while True:
        # API 요청 URL
        url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/{DATA_TYPE}/{SERVICE_NAME}/{START_INDEX}/{END_INDEX}/"

        # API 호출
        response = requests.get(url)

        if response.status_code != 200:
            print(f"API 요청 실패: {response.status_code}")
            break

        data = response.json()

        # 데이터 존재 여부 확인
        if SERVICE_NAME not in data or "row" not in data[SERVICE_NAME]:
            print("데이터가 더 이상 없습니다.")
            break

        rows = data[SERVICE_NAME]["row"]

        # CSV에 데이터 저장
        for row in rows:
            writer.writerow([
                row["STDR_YYQU_CD"], row["SIGNGU_CD"], row["SIGNGU_CD_NM"],
                row["SVC_INDUTY_CD"], row["SVC_INDUTY_CD_NM"],
                row["STOR_CO"], row["SIMILR_INDUTY_STOR_CO"], row["OPBIZ_RT"],
                row["OPBIZ_STOR_CO"], row["CLSBIZ_RT"], row["CLSBIZ_STOR_CO"], row["FRC_STOR_CO"]
            ])

        # 현재 가져온 데이터 개수가 1000개보다 적다면 더 이상 데이터가 없음
        if len(rows) < 1000:
            print("모든 데이터를 성공적으로 가져왔습니다.")
            break

        # 다음 페이지 요청을 위해 인덱스 증가
        START_INDEX += 1000
        END_INDEX += 1000

        print(f"{START_INDEX} ~ {END_INDEX} 데이터 가져오는 중...")

        # API 호출 제한 방지를 위한 딜레이 (필요 시 활성화)
        time.sleep(1)

## 서울시_상권분석_서비스(길단위인구-자치구) 크롤링링

import requests
import csv
import time

# API 정보
API_KEY = "56777a6c6a776a6437306c716f6a62"  # 발급받은 인증키
SERVICE_NAME = "VwsmSignguFlpopW"
DATA_TYPE = "json"
START_INDEX = 1
END_INDEX = 1000  # API에서 한 번에 최대 1000개씩 제공
FILENAME = "seoul_flpop_data.csv"

# CSV 파일 헤더
HEADER = [
    "기준_년분기_코드", "자치구_코드", "자치구_코드_명", "총_유동인구_수",
    "월요일_유동인구_수", "화요일_유동인구_수", "수요일_유동인구_수",
    "목요일_유동인구_수", "금요일_유동인구_수", "토요일_유동인구_수", "일요일_유동인구_수"
]

# CSV 파일 생성 및 헤더 작성
with open(FILENAME, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(HEADER)

    while True:
        # API 요청 URL
        url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/{DATA_TYPE}/{SERVICE_NAME}/{START_INDEX}/{END_INDEX}/"

        # API 호출
        response = requests.get(url)

        if response.status_code != 200:
            print(f"API 요청 실패: {response.status_code}")
            break

        data = response.json()

        # 데이터 존재 여부 확인
        if SERVICE_NAME not in data or "row" not in data[SERVICE_NAME]:
            print("데이터가 더 이상 없습니다.")
            break

        rows = data[SERVICE_NAME]["row"]

        # CSV에 데이터 저장
        for row in rows:
            writer.writerow([
                row.get("STDR_YYQU_CD", ""),
                row.get("SIGNGU_CD", ""),
                row.get("SIGNGU_CD_NM", ""),
                row.get("TOT_FLPOP_CO", ""),
                row.get("MON_FLPOP_CO", ""), row.get("TUES_FLPOP_CO", ""), 
                row.get("WED_FLPOP_CO", ""), row.get("THUR_FLPOP_CO", ""), 
                row.get("FRI_FLPOP_CO", ""), row.get("SAT_FLPOP_CO", ""), 
                row.get("SUN_FLPOP_CO", "")
            ])

        # 현재 가져온 데이터 개수가 1000개보다 적다면 더 이상 데이터가 없음
        if len(rows) < 1000:
            print("모든 데이터를 성공적으로 가져왔습니다.")
            break

        # 다음 페이지 요청을 위해 인덱스 증가
        START_INDEX += 1000
        END_INDEX += 1000

        print(f"{START_INDEX} ~ {END_INDEX} 데이터 가져오는 중...")

        # API 호출 제한 방지를 위한 딜레이 (필요 시 활성화)
        time.sleep(1)

## 평균매출비율 계산

import pandas as pd

# 파일 경로 설정
revenue_path = r"C:\Users\dlwlg\Desktop\상권 분석 데이터\서울시_상권분석_서비스(추정매출-자치구).csv"
store_path = r"C:\Users\dlwlg\Desktop\상권 분석 데이터\서울시_상권분석_서비스(점포-자치구).csv"

# 데이터 로드
revenue_df = pd.read_csv(revenue_path, encoding='utf-8-sig')
store_df = pd.read_csv(store_path, encoding='utf-8-sig')

# 공통 컬럼 기준으로 병합
common_columns = ['기준_년분기_코드', '자치구_코드', '자치구_코드_명', '서비스_업종_코드', '서비스_업종_코드_명']
merged_df = pd.merge(revenue_df, store_df, on=common_columns)

# 특정 매출 컬럼들을 '유사_업종_점포_수'로 나누기
revenue_columns = [
    '당월_매출_금액', '당월_매출_건수', '주중_매출_금액', '주말_매출_금액',
    '월요일_매출_금액', '화요일_매출_금액', '수요일_매출_금액', '목요일_매출_금액', 
    '금요일_매출_금액', '토요일_매출_금액', '일요일_매출_금액', 
    '시간대_00~06_매출_금액', '시간대_06~11_매출_금액', '시간대_11~14_매출_금액', 
    '시간대_14~17_매출_금액', '시간대_17~21_매출_금액', '시간대_21~24_매출_금액', 
    '남성_매출_금액', '여성_매출_금액', '연령대_10_매출_금액', '연령대_20_매출_금액', 
    '연령대_30_매출_금액', '연령대_40_매출_금액', '연령대_50_매출_금액', '연령대_60_이상_매출_금액', 
    '주중_매출_건수', '주말_매출_건수', '월요일_매출_건수', '화요일_매출_건수', '수요일_매출_건수', 
    '목요일_매출_건수', '금요일_매출_건수', '토요일_매출_건수', '일요일_매출_건수', 
    '시간대_건수~06_매출_건수', '시간대_건수~11_매출_건수', '시간대_건수~14_매출_건수', 
    '시간대_건수~17_매출_건수', '시간대_건수~21_매출_건수', '시간대_건수~24_매출_건수', 
    '남성_매출_건수', '여성_매출_건수', '연령대_10_매출_건수', '연령대_20_매출_건수', 
    '연령대_30_매출_건수', '연령대_40_매출_건수', '연령대_50_매출_건수', '연령대_60_이상_매출_건수'
]

# '유사_업종_점포_수' 컬럼으로 나누기 (예: '당월_매출_금액'을 '유사_업종_점포_수'로 나누기)
for col in revenue_columns:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col] / merged_df['유사_업종_점포_수']

# 비율 계산
# 연령대 금액 비율
age_columns = ['연령대_10_매출_금액', '연령대_20_매출_금액', '연령대_30_매출_금액', 
               '연령대_40_매출_금액', '연령대_50_매출_금액', '연령대_60_이상_매출_금액']
for col in age_columns:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col] / merged_df['당월_매출_금액']

# 연령대 건수 비율
age_count_columns = ['연령대_10_매출_건수', '연령대_20_매출_건수', '연령대_30_매출_건수', 
                     '연령대_40_매출_건수', '연령대_50_매출_건수', '연령대_60_이상_매출_건수']
for col in age_count_columns:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col] / merged_df['당월_매출_건수']

# 성별 금액 비율
gender_columns = ['남성_매출_금액', '여성_매출_금액']
for col in gender_columns:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col] / merged_df['당월_매출_금액']

# 성별 건수 비율
gender_count_columns = ['남성_매출_건수', '여성_매출_건수']
for col in gender_count_columns:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col] / merged_df['당월_매출_건수']

# 주별 금액 비율
week_columns = ['주중_매출_금액', '주말_매출_금액']
for col in week_columns:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col] / merged_df['당월_매출_금액']

# 주별 건수 비율
week_count_columns = ['주중_매출_건수', '주말_매출_건수']
for col in week_count_columns:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col] / merged_df['당월_매출_건수']

# 시간대 금액 비율
time_columns = ['시간대_00~06_매출_금액', '시간대_06~11_매출_금액', '시간대_11~14_매출_금액', 
                '시간대_14~17_매출_금액', '시간대_17~21_매출_금액', '시간대_21~24_매출_금액']
for col in time_columns:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col] / merged_df['당월_매출_금액']

# 시간대 건수 비율
time_count_columns = ['시간대_건수~06_매출_건수', '시간대_건수~11_매출_건수', '시간대_건수~14_매출_건수', 
                      '시간대_건수~17_매출_건수', '시간대_건수~21_매출_건수', '시간대_건수~24_매출_건수']
for col in time_count_columns:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col] / merged_df['당월_매출_건수']

# 요일별 금액 비율
weekday_columns = ['월요일_매출_금액', '화요일_매출_금액', '수요일_매출_금액', 
                  '목요일_매출_금액', '금요일_매출_금액', '토요일_매출_금액', '일요일_매출_금액']
for col in weekday_columns:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col] / merged_df['당월_매출_금액']

# 요일별 건수 비율
weekday_count_columns = ['월요일_매출_건수', '화요일_매출_건수', '수요일_매출_건수', 
                         '목요일_매출_건수', '금요일_매출_건수', '토요일_매출_건수', '일요일_매출_건수']
for col in weekday_count_columns:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col] / merged_df['당월_매출_건수']

# 결과 저장
output_path = r"C:\Users\dlwlg\Desktop\상권 분석 데이터\서울시_상권분석_서비스(평균매출비율-자치구).csv"
merged_df.to_csv(output_path, index=False, encoding='utf-8-sig')

## 자치구별 평균매출비율

import pandas as pd

# 파일 경로 설정
file_path = r"C:\Users\dlwlg\Desktop\상권 분석 데이터\서울시_상권분석_서비스(평균매출비율-자치구).csv"

# 데이터 로드
df = pd.read_csv(file_path, encoding='utf-8-sig')

# 🔹 필요한 컬럼만 선택
df_filtered = df[['기준_년분기_코드', '자치구_코드_명', '당월_매출_금액', 
                  '월요일_매출_금액', '화요일_매출_금액', '수요일_매출_금액', 
                  '목요일_매출_금액', '금요일_매출_금액', '토요일_매출_금액', '일요일_매출_금액']]

# 🔹 기준_년분기_코드, 자치구_코드_명 으로 그룹화 후 **평균** 계산
df_grouped = df_filtered.groupby(['기준_년분기_코드', '자치구_코드_명']).mean().reset_index()

# 🔹 새로운 파일로 저장
output_file_path = r"C:\Users\dlwlg\Desktop\상권 분석 데이터\서울시_상권분석_서비스(평균매출비율-자치구_그룹).csv"
df_grouped.to_csv(output_file_path, index=False, encoding='utf-8-sig')

## 자치구별 매출 인구 병합

import pandas as pd

# 파일 경로 설정
file_path1 = r"C:\Users\dlwlg\Desktop\상권 분석 데이터\서울시_상권분석_서비스(평균매출비율-자치구_그룹).csv"
file_path2 = r"C:\Users\dlwlg\Desktop\상권 분석 데이터\서울시_상권분석_서비스(길단위인구-자치구).csv"

# 데이터 로드
df1 = pd.read_csv(file_path1, encoding='utf-8-sig')
df2 = pd.read_csv(file_path2, encoding='utf-8-sig')

# 🔹 필요한 컬럼만 선택 (df1)
df1_filtered = df1[['기준_년분기_코드', '자치구_코드_명', '당월_매출_금액', 
                    '월요일_매출_금액', '화요일_매출_금액', '수요일_매출_금액', 
                    '목요일_매출_금액', '금요일_매출_금액', '토요일_매출_금액', 
                    '일요일_매출_금액']]

# 🔹 필요한 컬럼만 선택 (df2)
df2_filtered = df2[['기준_년분기_코드', '자치구_코드', '자치구_코드_명', '총_유동인구_수', 
                    '월요일_유동인구_수', '화요일_유동인구_수', '수요일_유동인구_수', 
                    '목요일_유동인구_수', '금요일_유동인구_수', '토요일_유동인구_수', 
                    '일요일_유동인구_수']]

# 🔹 기준_년분기_코드, 자치구_코드_명 을 기준으로 병합
df_merged = pd.merge(df1_filtered, df2_filtered, on=['기준_년분기_코드', '자치구_코드_명'], how='inner')

# 🔹 새로운 파일로 저장
output_file_path = r"C:\Users\dlwlg\Desktop\상권 분석 데이터\서울시_상권분석_서비스(평균매출비율+인구-자치구).csv"
df_merged.to_csv(output_file_path, index=False, encoding='utf-8-sig')

## 자치구별 일 매출 데이터 생성

# 필요한 라이브러리 불러오기
import pandas as pd
from datetime import datetime

# 데이터 파일 경로 (로컬 환경 기준)
sales_file_path = "C:/Users/dlwlg/Desktop/상권 분석 데이터/서울시_상권분석_서비스(평균매출비율+인구-자치구).csv"
population_file_path = "C:/Users/dlwlg/Desktop/상권 분석 데이터/서울 일별 유동인구.csv"

# 데이터 불러오기
sales_df = pd.read_csv(sales_file_path)
population_df = pd.read_csv(population_file_path)

# 날짜 형식 변환 (유동 인구 데이터)
population_df["기준일ID"] = pd.to_datetime(population_df["기준일ID"], format="%Y%m%d")
population_df.rename(columns={"기준일ID": "일자", "시군구명": "자치구"}, inplace=True)

# 결과 저장 리스트
daily_sales_list = []

# 분기별 데이터를 월별로 확장하고, 유동 인구를 반영하여 일별 매출 계산
for _, row in sales_df.iterrows():
    year_quarter = str(row["기준_년분기_코드"])
    year = int(year_quarter[:4])
    quarter = int(year_quarter[4])

    # 해당 분기의 월 리스트
    months_in_quarter = {
        1: [1, 2, 3],
        2: [4, 5, 6],
        3: [7, 8, 9],
        4: [10, 11, 12]
    }[quarter]

    for month in months_in_quarter:
        # 월별 총 매출 (월 평균 매출 그대로 사용)
        monthly_sales = row["당월_매출_금액"]

        # 해당 월의 유동 인구 데이터 가져오기
        month_population = population_df[
            (population_df["일자"].dt.year == year) &
            (population_df["일자"].dt.month == month) &
            (population_df["자치구"] == row["자치구_코드_명"])
        ]

        # 해당 월의 총 유동 인구 계산
        total_month_population = month_population["총생활인구수"].sum()

        # 유동 인구 비율을 활용하여 일별 매출 계산
        for _, pop_row in month_population.iterrows():
            date = pop_row["일자"]
            daily_population = pop_row["총생활인구수"]

            # 해당 날짜의 유동 인구 비율을 활용하여 매출 계산
            daily_sales = (monthly_sales * daily_population) / total_month_population if total_month_population > 0 else 0

            daily_sales_list.append({
                "일자": date.strftime("%Y-%m-%d"),
                "자치구": row["자치구_코드_명"],
                "일매출금액": daily_sales
            })

# 일별 매출 데이터프레임 생성
final_daily_sales_df = pd.DataFrame(daily_sales_list)

# CSV 파일로 저장
output_file_path = "C:/Users/dlwlg/Desktop/상권 분석 데이터/일별_매출데이터.csv"
final_daily_sales_df.to_csv(output_file_path, index=False, encoding="utf-8-sig")

print(f"일별 매출 데이터 저장 완료: {output_file_path}")
