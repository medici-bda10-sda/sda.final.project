import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# 데이터 로드
data = pd.read_csv(r"C:\Users\dlwlg\Desktop\머신러닝 사용 데이터\머신러닝용_시계열데이터.csv")

# 날짜를 datetime 형식으로 변환
data['날짜'] = pd.to_datetime(data['날짜'])

# 사용자 입력: 자치구 선택
user_gu = input("예측하고 싶은 자치구를 입력하세요: ")
filtered_data = data[data['자치구'] == user_gu]

if filtered_data.empty:
    print("입력한 자치구에 해당하는 데이터가 없습니다.")
else:
    # 날짜 기준 정렬
    filtered_data = filtered_data.sort_values(by='날짜')

    # 필요한 열 선택 (날짜와 다변량 변수)
    time_series_data = filtered_data[['날짜', '총_결제금액', '평균기온', '최저기온', '최고기온', '축제개수', '총생활인구수']].copy()
    time_series_data.set_index('날짜', inplace=True)

    # 결측값 처리 (0으로 대체)
    time_series_data.fillna(0, inplace=True)

    # 데이터 스케일링 (Min-Max Scaling)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(time_series_data)

    # 시계열 데이터 생성 (윈도우 크기 설정)
    def create_sequences(data, window_size):
        X, y = [], []
        for i in range(window_size, len(data)):
            X.append(data[i-window_size:i, :-1])  # 마지막 열 제외 (타겟 변수 제외)
            y.append(data[i, -1])  # 마지막 열 (타겟 변수)
        return np.array(X), np.array(y)

    window_size = 30  # 최근 30일 데이터를 기반으로 예측
    X, y = create_sequences(scaled_data, window_size)

    # 훈련 및 테스트 데이터 분리
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # LSTM 모델 구성
    model = Sequential([
        LSTM(64, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
        Dropout(0.2),
        LSTM(32, activation='relu'),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')

    # 조기 종료 콜백 설정
    early_stopping = EarlyStopping(monitor='val_loss', patience=10)

    # 모델 학습
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50,
              batch_size=32, callbacks=[early_stopping], verbose=1)

    # 테스트 데이터에 대한 예측
    y_pred = model.predict(X_test)

    # 스케일 복원 (원래 값으로 변환)
    y_test_rescaled = scaler.inverse_transform(
        np.concatenate([np.zeros((len(y_test), scaled_data.shape[1] - 1)), y_test.reshape(-1, 1)], axis=1))[:, -1]
    
    y_pred_rescaled = scaler.inverse_transform(
        np.concatenate([np.zeros((len(y_pred), scaled_data.shape[1] - 1)), y_pred], axis=1))[:, -1]

    # 평가 지표 계산
    mae = mean_absolute_error(y_test_rescaled, y_pred_rescaled)
    rmse = np.sqrt(mean_squared_error(y_test_rescaled, y_pred_rescaled))
    r2 = r2_score(y_test_rescaled, y_pred_rescaled)

    print("\n모델 평가:")
    print(f"MAE (평균 절대 오차): {mae:.2f}")
    print(f"RMSE (평균 제곱근 오차): {rmse:.2f}")
    print(f"R² (결정계수): {r2:.4f}")

    # 예측
    predictions = model.predict(X_test)
    
    # 스케일 복원 (원래 값으로 변환)
    predictions_rescaled = scaler.inverse_transform(
        np.concatenate([np.zeros((len(predictions), scaled_data.shape[1] - 1)), predictions], axis=1))[:, -1]

    # 마지막 날짜 이후의 매출 예측
    last_date = time_series_data.index[-1]
    next_date = last_date + pd.Timedelta(days=1)
    
    print(f"\n[{user_gu}]의 마지막 날짜: {last_date.strftime('%Y-%m-%d')}")
    print(f"예상 총 결제 금액 ({next_date.strftime('%Y-%m-%d')}): {predictions_rescaled[-1]:,.0f} 원")
