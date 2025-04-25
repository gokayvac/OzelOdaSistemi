import json
import os
from BotModules.Config import DATA

class JsonManager:
    @staticmethod
    def load_data():
        os.makedirs(os.path.dirname(DATA), exist_ok=True)
        if os.path.exists(DATA):
            try:
                with open(DATA, 'r', encoding='utf-8') as f: return json.load(f)
            except Exception as e: print(f"Özel oda verilerini yüklerken hata oluştu: {e}")
        return {}

    @staticmethod
    def save_data(data):
        try:
            os.makedirs(os.path.dirname(DATA), exist_ok=True)
            with open(DATA, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e: print(f"Özel oda verilerini kaydederken hata oluştu: {e}"); return False