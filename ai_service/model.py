import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from django.conf import settings

"""Create fake data"""
def create_sample_data(): 
    return pd.DataFrame({
        'brand': ['Samsung']*5 + ['Apple']*5 + ['Xiaomi']*5,
        'ram': ['4GB','6GB','8GB','8GB','12GB']*3,
        'storage': ['64GB','128GB','128GB','256GB','512GB']*3,
        'screen_size': [5.8, 6.1, 6.4, 6.7, 6.9]*3,
        'price': [400,600,800,1000,1200,  # Samsung
                  800,1000,1200,1400,1600, # Apple 
                  200,300,400,500,600]     # Xiaomi
    })

def train_model():
    df = create_sample_data()
    
    # Feature engineering
    df['ram_gb'] = df['ram'].str.extract('(\d+)').astype(int)
    df['storage_gb'] = df['storage'].str.extract('(\d+)').astype(int)
    
    # Encode brands
    le = LabelEncoder()
    df['brand_encoded'] = le.fit_transform(df['brand'])
    
    # Train model
    model = RandomForestRegressor(n_estimators=20, random_state=42)
    model.fit(df[['brand_encoded', 'ram_gb', 'storage_gb', 'screen_size']], df['price'])
    
    # Save to files
    model_dir = os.path.join(settings.BASE_DIR, 'api/ai_service')
    os.makedirs(model_dir, exist_ok=True)
    
    joblib.dump(model, os.path.join(model_dir, 'phone_price_model.joblib'))
    joblib.dump(le, os.path.join(model_dir, 'label_encoder.joblib'))
    
    print(" Model trained and saved!")
    return model

def load_model():
    """Load model or create new if missing"""
    model_path = os.path.join(settings.BASE_DIR, 'api/ai_service/phone_price_model.joblib')
    if not os.path.exists(model_path):
        return train_model()
    return joblib.load(model_path)