import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(log_data):
    df = pd.DataFrame(log_data)
    if df.empty:
        return df, df
    df['action_code'] = df['action'].astype('category').cat.codes
    df['location_code'] = df['location'].astype('category').cat.codes
    feats = df[['action_code', 'location_code']]
    model = IsolationForest(contamination=0.2, random_state=42)
    df['anomaly_score'] = model.fit_predict(feats)
    anomalies = df[df['anomaly_score'] == -1]
    return df, anomalies
