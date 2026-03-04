from flask import Flask, jsonify
from flask_cors import CORS
import os

app=Flask(__name__)

CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'API ситемы учета товаров',
        'version': '1.0.0',
        'endpoints': {
            'GET /': 'Информация об API',
            'GET /health': 'Проверка состояния сервера'
        }
    })

@app.route('/health')
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Создана папка 'data'")

    print("=" * 40)
    print("Сервер запущен")
    print("API доступен по адресу: http://localhost:5000")
    print("Фронтенд: frontend/index.html")
    print("=" * 40)

    app.run(debug=True, host='0.0.0.0', port=5000)