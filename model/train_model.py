import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

# 1. Load Data
print("Loading data...")
df = pd.read_csv("traffic_data.csv")
X = df[["src_port", "dst_port", "packet_size", "flags"]]
y = df["label"]

# 2. Train Model
print("Training Random Forest...")
clf = RandomForestClassifier(n_estimators=10, max_depth=5)
clf.fit(X, y)
print(f"Model Accuracy: {clf.score(X, y) * 100:.2f}%")

# 3. Convert to ONNX
initial_type = [('float_input', FloatTensorType([None, 4]))]
# Force it to use an older, compatible version (Opset 12)
onx = convert_sklearn(clf, initial_types=initial_type, target_opset=12)

# 4. Save
with open("sentinel.onnx", "wb") as f:
    f.write(onx.SerializeToString())

print("Success! Model saved as 'sentinel.onnx'.")