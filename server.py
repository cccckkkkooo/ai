from flask import Flask, request, jsonify
import g4f
from flask_cors import CORS
from threading import Timer

app = Flask(__name__)
CORS(app)  # Разрешает запросы с других устройств

# Храним предпочтения в виде строк
saved_preferences = ""

def get_g4f_response(user_input):
    """Функция для обработки запроса через g4f."""
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": user_input}]
        )
        return response  # g4f уже возвращает строку
    except Exception as e:
        print(f"Ошибка g4f: {e}")
        return "Ошибка обработки запроса AI"

@app.route('/', methods=['POST'])
def chat():
    try:
        # Попробуем получить данные с выводом в консоль
        print("Запрос пришел!")

        raw_data = request.data.decode("utf-8")
        print(f"Сырой JSON: {raw_data}")

        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "Некорректный JSON"}), 400

        user_message = data.get("message") or data.get("text")  # Поддержка обоих вариантов

        if not user_message:
            return jsonify({"error": "Пустой запрос"}), 400

        response = get_g4f_response(user_message)
        return jsonify({"message": response})

    except Exception as e:
        print(f"Ошибка сервера: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/preferences', methods=['POST'])
def save_preferences():
    global saved_preferences
    try:
        preferences_text = request.data.decode("utf-8").strip()
        if not preferences_text:
            return "Пустой запрос", 400

        saved_preferences = preferences_text
        print(f"Сохраненные предпочтения: {saved_preferences}")
        return "Успешно сохранено", 200
    except Exception as e:
        print(f"Ошибка сервера: {e}")
        return "Ошибка сервера", 500
        
def keep_alive():
    Timer(60, keep_alive).start()
    requests.get("https://ai-travel-api.onrender.com/status")

keep_alive()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True, use_reloader=False)
