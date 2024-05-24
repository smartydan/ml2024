from catboost import CatBoostClassifier
import sys

model = CatBoostClassifier()
model.load_model('classifier')

if len(sys.argv) != 2:
    print("Usage: python main.py <input_file>")
    sys.exit(1)

file_name = sys.argv[1]

try:
    with open(file_name, 'rb') as f:
        content = f.read().decode('utf-8')
except FileNotFoundError as e:
    print("No such file")
    sys.exit(1)

pred = model.predict([content])
print(*pred)