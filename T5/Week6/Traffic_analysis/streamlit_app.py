import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import scipy

def process_and_train(df):
    # Data processing
    for column in df.select_dtypes(include=['int']):
        if (df[column] > 0).all():
            df[column] = scipy.special.boxcox1p(df[column], 0.5)

    df.drop('is_holiday', axis=1, inplace=True)
    df['date_time'] = pd.to_datetime(df['date_time']).dt.date

    numerical_features = ['temperature', 'clouds_all', 'air_pollution_index', 'humidity', 'wind_speed', 'wind_direction']
    scaler = StandardScaler()
    df[numerical_features] = scaler.fit_transform(df[numerical_features])

    traffic_volume = df[['traffic_volume']].copy()
    df.drop('traffic_volume', axis=1, inplace=True)
    df.set_index('date_time', inplace=True)

    label_encoder = LabelEncoder()
    df['weather_type'] = label_encoder.fit_transform(df['weather_type'])
    df['weather_description'] = label_encoder.fit_transform(df['weather_description'])

    train_split = round(len(df) * 0.8)
    train_data = df.iloc[:train_split]
    test_data = df.iloc[train_split:]

    scaler = StandardScaler()
    train_data_scaled = scaler.fit_transform(train_data)
    test_data_scaled = scaler.transform(test_data)  # Corrected here

    def create_dataset(dataset, time_step):
        X, Y = [], []
        for i in range(len(dataset) - time_step - 1):
            a = dataset[i:(i + time_step), :]
            X.append(a)
            Y.append(dataset[i + time_step, 0])
        return np.array(X), np.array(Y)

    timestep = 10
    X_train, Y_train = create_dataset(train_data_scaled, timestep)
    X_test, Y_test = create_dataset(test_data_scaled, timestep)

    model = Sequential()
    model.add(LSTM(units=128, activation='tanh', return_sequences=True, input_shape=(timestep, X_train.shape[2])))
    model.add(LSTM(units=128, activation='tanh', return_sequences=True))
    model.add(LSTM(units=128, activation='tanh', return_sequences=True))
    model.add(LSTM(units=64, activation='tanh', return_sequences=False))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, Y_train, epochs=50, batch_size=32, validation_data=(X_test, Y_test))

    predictions = model.predict(X_test)
    predictions_rescaled = scaler.inverse_transform(np.concatenate((predictions, np.zeros((predictions.shape[0], X_train.shape[2] - 1))), axis=1))[:, 0]
    Y_test_rescaled = scaler.inverse_transform(np.concatenate((Y_test.reshape(-1, 1), np.zeros((Y_test.shape[0], X_train.shape[2] - 1))), axis=1))[:, 0]

    return Y_test_rescaled, predictions_rescaled



def main():
    st.title("CSV Uploader and Time Series Model")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.write("**Uploaded CSV File:**")
        st.dataframe(df.head())

        if 'date_time' in df.columns:
            Y_test_rescaled, predictions_rescaled = process_and_train(df)

            # Plot results
            plt.figure(figsize=(12, 6))
            plt.plot(Y_test_rescaled, label='Actual Traffic Volume', color='blue')
            plt.plot(predictions_rescaled, label='Predicted Traffic Volume', color='red')
            plt.title('Actual vs Predicted Traffic Volume')
            plt.xlabel('Time')
            plt.ylabel('Traffic Volume')
            plt.legend()

            st.pyplot(plt)
        else:
            st.error("The CSV file must contain a 'date_time' column.")

if __name__ == "__main__":
    main()
