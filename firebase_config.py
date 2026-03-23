import firebase_admin
from firebase_admin import credentials, db
import hashlib
import time
# Путь к JSON-файлу с ключом сервиса
SERVICE_ACCOUNT_KEY = "serviceAccountKey.json"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def initialize_firebase():
    """Инициализирует подключение к Firebase"""
    try:
        # Проверяем, не инициализирован ли уже Firebase
        if not firebase_admin._apps:
            cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://pr0mine431-default-rtdb.firebaseio.com/'  # Замените на ваш URL
            })
            print("Firebase инициализирована успешно")
    except Exception as e:
        print(f"Ошибка инициализации Firebase: {e}")


# Вызываем инициализацию при импорте модуля
initialize_firebase()


def save_user_to_firebase(login, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        ref = db.reference('users')
        ref.child(login).set({
            'password_hash': hashed_password,
            'registered_at': int(time.time() * 1000)  # Unix-время в мс
        })
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def check_user_in_firebase(login, password):
    hashed_password = hash_password(password)
    try:
        ref = db.reference(f'users/{login}')
        user_data = ref.get()
        if user_data and user_data.get('password_hash') == hashed_password:
            return True
        return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
