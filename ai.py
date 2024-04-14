import datetime
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def prepare_data(prices):
    df = pd.DataFrame(prices)
    df['priceUsd'] = pd.to_numeric(df['priceUsd'])
    df['time'] = pd.to_numeric(df['time'])

    # Convert UNIX timestamp to datetime for easier manipulation
    df['date'] = pd.to_datetime(df['time'], unit='ms')
    df.set_index('date', inplace=True)

    # We will use days since the first date in the dataset as our feature
    df['days_since'] = (df.index - df.index.min()).days

    # Shift the price by subtracting the last known price to adjust the intercept
    last_price = df['priceUsd'].iloc[-1]
    df['adjusted_price'] = df['priceUsd'] - last_price

    return df[['days_since']], df['adjusted_price'], last_price

def predict(prices, future_time):
    now = int(datetime.datetime.now().timestamp() * 1000)
    if int(future_time) <= now:
        print("Provided future time is not in the future.")
        return None, None

    X, y, last_price = prepare_data(prices)
    
    # Train the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression(fit_intercept=True)
    model.fit(X_train, y_train)
    
    # Prepare future time data
    future_date = pd.to_datetime(future_time, unit='ms')
    days_since_future = (future_date - X_train.index.min()).days
    future_features = np.array([[days_since_future]])

    # Make prediction and adjust by adding the last known price
    predicted_deviation = model.predict(future_features)[0]
    predicted_price = predicted_deviation + last_price

    # Test the model's accuracy
    y_pred = model.predict(X_test)
    accuracy = 100 - (mean_absolute_error(y_test + last_price, y_pred + last_price) / (y_test + last_price).mean()) * 100

    return predicted_price, accuracy