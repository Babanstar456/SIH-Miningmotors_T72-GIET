import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler
import warnings
import numpy as np

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# --- Data Loading ---
file_synth = "synthetic_soh.csv"
file_prob = "problem_rows_sample.csv"

try:
    df_synth = pd.read_csv(file_synth)
    df_prob = pd.read_csv(file_prob)
except FileNotFoundError as e:
    print(f"Error loading file: {e}")
    exit()

# --- Data Preparation and Labeling ---

# 1. Create the binary target variable 'is_failure'
# Label 1 (Needs Replacement) for rows identified as problems, 0 (Ok/Normal) otherwise.
problem_timestamps = set(df_prob['timestamp'])
df_ml = df_synth.copy()
df_ml['is_failure'] = df_ml['timestamp'].isin(problem_timestamps).astype(int)

# 2. Feature Selection: Use all descriptive parameters
features = ['age_days', 'cycles', 'avg_dod', 'avg_temp', 'cumulative_ah']
X = df_ml[features]
y = df_ml['is_failure']

# 3. Scaling features (necessary for normalization)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=features)

# 4. Train-Test Split (Stratified to handle the imbalance)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# --- Model Training (Decision Tree Classifier) ---

# Decision Tree with class_weight='balanced' for optimal performance on imbalanced data
dt_model = DecisionTreeClassifier(random_state=42, class_weight='balanced')
dt_model.fit(X_train, y_train)

# --- Model Evaluation ---
y_pred = dt_model.predict(X_test)
f1 = f1_score(y_test, y_pred, zero_division=0)
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, zero_division=0)
rec = recall_score(y_test, y_pred, zero_division=0)

print("\n--- Final Decision Tree Model Evaluation (All Descriptive Features) ---")
print(f"  F1 Score: {f1:.4f}")
print(f"  Accuracy: {acc:.4f}")
print(f"  Precision: {prec:.4f}")
print(f"  Recall: {rec:.4f}")

# --- Prediction Function ---

def predict_battery_status(age_days: float, cycles: float, avg_dod: float, avg_temp: float, cumulative_ah: float, model, scaler, feature_names):
    """
    Predicts if a battery needs to be replaced based on all five parameters.
    
    Returns:
    - "Ok/Normal"
    - "Needs to be Replaced"
    """
    # 1. Create a DataFrame for the input data in the correct order
    new_data = pd.DataFrame([[age_days, cycles, avg_dod, avg_temp, cumulative_ah]], columns=feature_names)
    
    # 2. Scale the new data using the fitted scaler
    new_data_scaled = scaler.transform(new_data)
    
    # 3. Make the prediction
    prediction = model.predict(new_data_scaled)[0]
    
    # 4. Map the numerical prediction to a descriptive string
    status = "Needs to be Replaced" if prediction == 1 else "Ok/Normal"
    
    return status

# --- Example Usage ---
print("\n--- Example Prediction ---")

# Example 1: High age, high cumulative usage (likely needs replacement)
status_1 = predict_battery_status(
    age_days=350, cycles=70, avg_dod=0.35, avg_temp=30, cumulative_ah=7000, 
    model=dt_model, scaler=scaler, feature_names=features
)
print(f"Input 1: Age=350, Cycles=70, Avg_DoD=0.35, Avg_Temp=30, Cum_Ah=7000 -> Status: {status_1}")

# Example 2: Low age, low usage (likely Ok/Normal)
status_2 = predict_battery_status(
    age_days=50, cycles=10, avg_dod=0.20, avg_temp=25, cumulative_ah=1000, 
    model=dt_model, scaler=scaler, feature_names=features
)
print(f"Input 2: Age=50, Cycles=10, Avg_DoD=0.20, Avg_Temp=25, Cum_Ah=1000 -> Status: {status_2}")