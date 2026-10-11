import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Load dataset
df = pd.read_csv("loan_applications.csv")

NUMERIC_FEATURES = [
    "age",
    "annual_income",
    "months_employed",
    "loan_amount",
    "account_balance",
]
CATEGORICAL_FEATURES = ["employment_type", "home_ownership"]

X = df.drop(columns=["defaulted"])
y = df["defaulted"]

# 1. Split FIRST to prevent data leakage
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 2. Build ColumnTransformer for feature preprocessing
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, NUMERIC_FEATURES),
    ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
])

# 3. Build overall Pipeline including PCA and Classifier
pipe = Pipeline([
    ("preprocess", preprocessor),
    ("pca", PCA(n_components=5, random_state=42)),
    ("clf", LogisticRegression(max_iter=1000)),
])

# 4. Wrap Pipeline in GridSearchCV for leak-free cross-validation
param_grid = {
    "pca__n_components": [3, 5, 8],
    "clf__C": [0.1, 1, 10],
}
grid = GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy")
grid.fit(X_train, y_train)

# 5. Output Results
print("Best params:", grid.best_params_)
print("Best CV accuracy:", round(grid.best_score_, 4))
final_acc = accuracy_score(y_test, grid.best_estimator_.predict(X_test))
print("Final test accuracy:", round(final_acc, 4))
