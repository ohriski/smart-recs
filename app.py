import os
import json
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# ОТРИМАННЯ ЗМІННОЇ API KEY
# Для локального запуску можна просто вставити ключ сюди, 
# але для публікації краще брати з змінних середовища.
api_key = os.environ.get("OPENAI_API_KEY") 
client = OpenAI(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    genres = data.get('genres')
    min_rating = data.get('rating', 6.0)

    # Формування запиту до ШІ
    prompt = f"""
    Ти - експерт з кіно. Порадь 4 фільми в жанрах: {genres}, які мають рейтинг вище {min_rating}/10.
    Відповідь поверни ТІЛЬКИ у форматі чистого JSON (без markdown), як масив об'єктів з полями:
    "title" (назва українською),
    "year" (рік),
    "description" (короткий опис українською, до 20 слів),
    "rating" (число).
    """

    try:
        # Виклик OpenAI API (використовуємо модель gpt-3.5-turbo або gpt-4o-mini для економії)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ти корисний помічник, що видає JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content
        # Очистка від можливих маркерів markdown
        content = content.replace("```json", "").replace("```", "")
        recommendations = json.loads(content)

        return jsonify({"status": "success", "data": recommendations})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
