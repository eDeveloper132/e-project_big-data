import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib

class ClimatePredictor:
    """
    A machine learning model to predict future climate trends and detect anomalies.
    """
    def __init__(self):
        self.model = LinearRegression()

    def _generate_dummy_processed_data(self, num_records=100):
        """
        Generates a dummy DataFrame simulating data processed by Hadoop.
        This helps in standalone training and testing of the model.
        """
        # Create a time series feature
        time_feature = np.arange(num_records).reshape(-1, 1)
        
        # Create a target variable (e.g., average temperature) with some noise
        # y = mx + c + noise
        temperature = 0.1 * time_feature.flatten() + 15 + np.random.normal(0, 2, num_records)
        
        df = pd.DataFrame({
            'time_index': time_feature.flatten(),
            'avg_temperature': temperature
        })
        return df

    def train(self):
        """
        Trains the linear regression model on the dataset.
        The algorithm learns a linear relationship between a time index and the 
        average temperature to predict future trends.
        """
        print("Generating dummy data for training...")
        data = self._generate_dummy_processed_data(500)
        
        X = data[['time_index']]  # Features
        y = data['avg_temperature']  # Target

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print("Training the Linear Regression model...")
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f"Model training complete. Mean Squared Error: {mse:.2f}")

        # Save the trained model
        joblib.dump(self.model, 'climate_model.pkl')
        print("Model saved to climate_model.pkl")

    def predict(self, future_time_index):
        """

        Predicts the average temperature for a future time index.
        """
        # In a real application, load the model from file
        # self.model = joblib.load('climate_model.pkl')
        return self.model.predict(np.array([[future_time_index]]))

    def detect_anomalies(self, historical_data, current_temp):
        """
        Detects anomalies by comparing a new data point against the historical distribution.
        An anomaly is flagged if the current temperature is significantly different
        from the historical mean (e.g., > 2 standard deviations).
        """
        mean_temp = np.mean(historical_data)
        std_dev_temp = np.std(historical_data)
        
        if abs(current_temp - mean_temp) > 2 * std_dev_temp:
            return {
                "is_anomaly": True,
                "message": f"Anomaly Detected: Temperature {current_temp}°C is outside the normal range ({mean_temp:.2f} ± {2*std_dev_temp:.2f})."
            }
        return {"is_anomaly": False}

if __name__ == '__main__':
    predictor = ClimatePredictor()
    
    # 1. Train the model
    predictor.train()
    
    # 2. Example Prediction
    future_prediction = predictor.predict(510) # Predict for a future time index
    print(f"Predicted temperature for time index 510: {future_prediction[0]:.2f}°C")
    
    # 3. Example Anomaly Detection
    historical_temps = predictor._generate_dummy_processed_data()['avg_temperature']
    current_reading = 35.0 # A high temperature reading
    anomaly_result = predictor.detect_anomalies(historical_temps, current_reading)
    if anomaly_result['is_anomaly']:
        print(anomaly_result['message'])
