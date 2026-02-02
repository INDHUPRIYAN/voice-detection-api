import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from utils_audio import extract_features_from_file

X, y = [], []

print("Loading dataset...")

for label, folder in [(0, "human"), (1, "ai")]:
    folder_path = os.path.join("dataset", folder)
    for file in os.listdir(folder_path):
        if file.endswith((".mp3", ".wav")):
            try:
                path = os.path.join(folder_path, file)
                feat = extract_features_from_file(path)
                X.append(feat)
                y.append(label)
            except Exception as e:
                print("Skipping", file, e)

X = np.array(X)
y = np.array(y)

print("Total samples:", len(X))

# Normalize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# Model
model = RandomForestClassifier(
    n_estimators=600,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)


print("Training model...")
model.fit(X_train, y_train)

pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)
print("\nModel Accuracy:", acc)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, pred))

print("\nClassification Report:")
print(classification_report(y_test, pred))

joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\n✅ Model & Scaler saved successfully!")
