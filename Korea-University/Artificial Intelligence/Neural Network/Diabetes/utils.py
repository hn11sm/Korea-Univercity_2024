import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def preprocess(df):
    print('----------------------------------------------')
    print("Before preprocessing")
    print("Number of rows with 0 values for each variable:")
    for col in df.columns:
        missing_rows = df[df[col] == 0].shape[0]
        print(f"{col}: {missing_rows}")
    print('----------------------------------------------')

    # Replace 0 values with NaN and fill with mean 
    cols_to_fix = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    for col in cols_to_fix:
        df[col] = df[col].replace(0, np.nan)
        df[col] = df[col].fillna(df[col].mean())

    print('----------------------------------------------')
    print("After preprocessing")
    print("Number of rows with 0 values for each variable:")
    for col in df.columns:
        missing_rows = df[df[col] == 0].shape[0]
        print(f"{col}: {missing_rows}")
    print('----------------------------------------------')

    # Standardize features
    scaler = StandardScaler()
    feature_cols = df.columns[:-1]  # 'Outcome' 제외한 모든 특성
    df[feature_cols] = scaler.fit_transform(df[feature_cols])

    return df