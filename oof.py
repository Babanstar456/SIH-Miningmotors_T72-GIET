import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler
import warnings
import numpy as np

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# --- DATA PREPARATION: PLACEHOLDER DATA ---
# NOTE: You MUST REPLACE this synthetic data with your actual turbine motor data.
# Ensure your data file is in the same format with columns:
# 'Speed', 'Output_Voltage', 'Temperature', and a target 'Maintenance_Required' (0 or 1).

# Using data structure inspired by publicly available Gas Turbine datasets.
data = {
    'Speed': np.random.uniform(8000, 16000, 1000),  # RPM
    'Output_Voltage': np.random.uniform(50, 100, 1000), # Power Output (MW)
    'Temperature': np.random.uniform(800, 1200, 1000), # Inlet Temperature (°C)
    # Binary label: 1 if maintenance is required (simulated based on high values)
    'Maintenance_Required': (
        (np.random.uniform(0, 1, 1000) > 0.95) | 
        (np.random.uniform(8000, 16000, 1000) > 15500) |
        (np.random.uniform(800, 1200, 1000) > 1150)
    ).astype(int)
}
df_turbine = pd.DataFrame(data)

print(f"Dataset Size: {len(df_turbine)} records")
print(f"Maintenance Required (1) Count: {df_turbine['Maintenance_Required'].sum()}")

# --- Feature Selection ---
features = ['Speed', 'Output_Voltage', 'Temperature']
X = df_turbine[features]
y = df_turbine['Maintenance_Required']

# --- Scaling features ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=features)

# --- Train-Test Split (Stratified for class imbalance) ---
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# --- Model Training (Decision Tree Classifier) ---
# Using class_weight='balanced' to handle the low number of maintenance events.
dt_model = DecisionTreeClassifier(random_state=42, class_weight='balanced')
dt_model.fit(X_train, y_train)

# --- Model Evaluation ---
y_pred = dt_model.predict(X_test)
f1 = f1_score(y_test, y_pred, zero_division=0)
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, zero_division=0)
rec = recall_score(y_test, y_pred, zero_division=0)

print("\n--- Decision Tree Model Evaluation (Placeholder Data) ---")
print(f"  F1 Score: {f1:.4f}")
print(f"  Accuracy: {acc:.4f}")
print(f"  Precision: {prec:.4f}")
print(f"  Recall: {rec:.4f}")

# --- Prediction Function ---

def predict_maintenance_need(speed: float, voltage: float, temperature: float, model, scaler, feature_names):
    """
    Predicts if a turbine motor requires maintenance.
    
    Args:
        speed (float): Motor rotational speed (e.g., RPM).
        voltage (float): Motor output voltage/power (e.g., MW).
        temperature (float): Motor operating temperature (e.g., °C).
        model: Trained ML model.
        scaler: Fitted StandardScaler object.
        feature_names: List of feature names used for training.

    Returns:
        str: "Ok/Normal" or "Maintenance Required".
    """
    # Create a DataFrame for the input data
    new_data = pd.DataFrame([[speed, voltage, temperature]], columns=feature_names)
    
    # Scale the new data using the fitted scaler
    new_data_scaled = scaler.transform(new_data)
    
    # Make the prediction
    prediction = model.predict(new_data_scaled)[0]
    
    status = "Maintenance Required" if prediction == 1 else "Ok/Normal"
    
    return status

# --- Example Usage ---
print("\n--- Example Predictions ---")

# Example 1: Normal operation values (simulated)
status_1 = predict_maintenance_need(
    speed=12000, voltage=80, temperature=950, 
    model=dt_model, scaler=scaler, feature_names=features
)
print(f"Input 1: Speed=12000, Voltage=80, Temp=950 -> Status: {status_1}")

# Example 2: High values (simulated critical condition)
status_2 = predict_maintenance_need(
    speed=15800, voltage=95, temperature=1180, 
    model=dt_model, scaler=scaler, feature_names=features
)
print(f"Input 2: Speed=15800, Voltage=95, Temp=1180 -> Status: {status_2}")