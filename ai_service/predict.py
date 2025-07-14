import os  
import pandas as pd
import joblib
from django.conf import settings
from .model import load_model

def evaluate_price(phone_data):
    try:
        model_path = os.path.join(settings.BASE_DIR, 'api/ai_service/phone_price_model.joblib')
        encoder_path = os.path.join(settings.BASE_DIR, 'api/ai_service/label_encoder.joblib')
        
        if not os.path.exists(model_path):
            from .model import train_model
            train_model()
            
        model = joblib.load(model_path)
        encoder = joblib.load(encoder_path)

        # fix input features
        input_data = pd.DataFrame([{
            'brand_encoded': encoder.transform([phone_data['brand']])[0],
            'ram_gb': int(''.join(filter(str.isdigit, phone_data['ram']))),
            'storage_gb': int(''.join(filter(str.isdigit, phone_data['storage']))),
            'screen_size': float(phone_data['screen_size'].replace('"', ''))
        }])

        # Make prediction
        return round(float(model.predict(input_data)[0]), 2)
        
    except KeyError as e:
        print(f"Missing required field: {e}")
        raise KeyError(f"Required field missing: {e}")
    except Exception as e:
        print(f"Prediction failed: {str(e)}")
        return None