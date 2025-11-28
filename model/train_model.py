import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

print("Loading data...")
df = pd.read_csv("traffic_data.csv")
X = df[["src_port", "dst_port", "packet_size", "flags"]]
y = df["label"]

print("Training Random Forest...")
clf = RandomForestClassifier(n_estimators=10, max_depth=5)
clf.fit(X, y)
print(f"Model Accuracy: {clf.score(X, y) * 100:.2f}%")

initial_type = [('float_input', FloatTensorType([None, 4]))]
onx = convert_sklearn(clf, initial_types=initial_type, target_opset=12)

with open("sentinel.onnx", "wb") as f:
    f.write(onx.SerializeToString())

print("Success! Model saved as 'sentinel.onnx'.")