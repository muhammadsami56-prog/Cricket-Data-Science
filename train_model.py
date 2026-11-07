# Import required libraries
import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)
# Load dataset
df = pd.read_csv("data/matches.csv")

print("Dataset loaded successfully!")
print("Total matches:", len(df))

# Select input features
features = [
    "team1",
    "team2",
    "venue",
    "toss_winner",
    "toss_decision"
]

# Select target column
target = "winner"

X = df[features]
y = df[target]

print("\nFeatures selected successfully!")
print("Input features:", features)
print("Target:", target)

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nDATA SPLIT")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# Define categorical data preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("categorical", OneHotEncoder(handle_unknown="ignore"), features)
    ]
)

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

# Create complete machine learning pipeline
pipeline = Pipeline([
    ("preprocessing", preprocessor),
    ("classifier", model)
])

print("\nMachine learning pipeline created successfully!")

# Train the machine learning model
print("\nTraining Random Forest Model...")

pipeline.fit(X_train, y_train)

# Make predictions
y_pred = pipeline.predict(X_test)
import os
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nMODEL EVALUATION")
print("----------------")
print(f"Accuracy: {accuracy * 100:.2f}%")

# Display detailed classification report
print("\nDETAILED CLASSIFICATION REPORT")
print("--------------------------------")
print(classification_report(y_test, y_pred, zero_division=0))

# Save trained model
joblib.dump(pipeline, "models/cricket_model.pkl")

print("\nModel saved successfully!")
print("Location: models/cricket_model.pkl")