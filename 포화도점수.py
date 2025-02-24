df = pd.read_csv(r"C:\Users\m\project\공공데이터_상권분석\data\머신러닝\피처엔지니어링일단다한통합데이터.csv")

# 기준년분기코드 기준으로 전분분기 대비 점포수가 증가한 경우에 1/0 부여하기
df['전분기_점포수'] = df.groupby('상권_코드_명')['유사_업종_점포_수'].shift(1) 
df['점포수 증가'] = (df['유사_업종_점포_수'] > df['전분기_점포수']).astype(int)

# 20242 까지의 점수 합산
df['개업 점수'] = df.groupby('상권_코드_명')['점포수 증가'].cumsum()

df = df[df['기준_년분기_코드'] == 20242]
df['매출_점포비'] = df.groupby('상권_코드_명')['당월_매출_금액'].transform('sum') / df.groupby('상권_코드_명')['점포_수'].transform('sum')
df['매출_유동인구비'] = df.groupby('상권_코드_명')['당월_매출_금액'].transform('sum') / df.groupby('상권_코드_명')['총_유동인구_수'].transform('sum')

# 경쟁강도 지수 계산
df['경쟁강도'] = df.groupby('상권_코드_명')['점포_수'].transform('sum') / df.groupby('행정동_코드_명')['점포_수'].transform('sum')

df['프랜차이즈_비율'] = df.groupby('상권_코드_명')['프랜차이즈_점포_수'].transform('sum') / df.groupby('상권_코드_명')['점포_수'].transform('sum')
df = df.drop_duplicates()

pohado_df = df[['상권_코드_명','경쟁강도','매출_점포비','프랜차이즈_비율','개업 점수']]
# 중복 제거
pohado_df = pohado_df.drop_duplicates()

pohado_df = pohado_df.groupby('상권_코드_명')[['경쟁강도','매출_점포비','프랜차이즈_비율','개업 점수']].mean().reset_index()

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

# 분석에 사용할 변수 선택
features = ['경쟁강도', '매출_점포비', '프랜차이즈_비율', '개업 점수']

# inf 값을 NaN으로 변경
pohado_score_df = pohado_df.replace([np.inf, -np.inf], np.nan)

# 결측치를 각 컬럼의 평균값으로 대체
pohado_score_df[features] = pohado_score_df[features].fillna(pohado_score_df[features].mean())

# 데이터 표준화
scaler = StandardScaler()
df_scaled = scaler.fit_transform(pohado_score_df[features])

# PCA 수행
pca = PCA(n_components=1)
pca_result = pca.fit_transform(df_scaled)

# 0~20으로 스케일링
mms = MinMaxScaler(feature_range=(0, 20))
saturation_score = mms.fit_transform(pca_result)

# 결과를 데이터프레임에 추가
pohado_df['포화도_점수'] = saturation_score

# 상권_코드_명과 포화도_점수만 선택
result = pohado_df[['상권_코드_명', '포화도_점수']]

# 포화도 점수 기준 내림차순 정렬
result = result.sort_values('포화도_점수', ascending=False)