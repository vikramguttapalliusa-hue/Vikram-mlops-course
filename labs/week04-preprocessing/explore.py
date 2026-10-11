import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

df = pd.read_csv("loan_applications.csv")

NUMERIC_FEATURES = ["age", "annual_income", "months_employed", "loan_amount", "account_balance"]
X = df.drop(columns=["defaulted"])
y = df["defaulted"]

# Leaky fit (fitted on full dataset X)
leaky_scaler = StandardScaler().fit(
    SimpleImputer(strategy="mean").fit_transform(X[NUMERIC_FEATURES])
)
print("Leaky mean:   ", leaky_scaler.mean_.round(2))

# Correct fit (fitted only on X_train)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
correct_scaler = StandardScaler().fit(
    SimpleImputer(strategy="median").fit_transform(X_train[NUMERIC_FEATURES])
)
print("Correct mean: ", correct_scaler.mean_.round(2))
