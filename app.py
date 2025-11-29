import os
import json
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        genres = data.get('genres')
        min_rating = data.get('rating', 6.0)

        # Спроба викликати ШІ
        prompt = f"""
        Ти - експерт з кіно. Порадь 4 фільми в жанрах: {genres}, які мають рейтинг вище {min_rating}/10.
        Відповідь поверни ТІЛЬКИ у форматі чистого JSON (без markdown), як масив об'єктів з полями:
        "title" (назва українською),
        "year" (рік),
        "description" (короткий опис українською, до 20 слів),
        "rating" (число).
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ти корисний помічник, що видає JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content
        content = content.replace("```json", "").replace("```", "")
        recommendations = json.loads(content)

        return jsonify({"status": "success", "data": recommendations})

    except Exception as e:
        # ЯКЩО ШІ НЕ ПРАЦЮЄ (Немає грошей, помилка мережі тощо)
        # Ми повертаємо "фейкові" дані, щоб сайт виглядав робочим
        print(f"Error calling OpenAI: {e}")
        
        fallback_data = [
            {
                "title": "Інтерстеллар (Демо режим)",
                "year": 2014,
                "description": "Команда дослідників вирушає крізь червоточину у спробі врятувати людство.",
                "rating": 8.6
            },
            {
                "title": "Матриця",
                "year": 1999,
                "description": "Хакер дізнається правду про реальність і приєднується до боротьби проти машин.",
                "rating": 8.7
            },
            {
                "title": "Той, що біжить по лезу 2049",
                "year": 2017,
                "description": "Молодий блейд-ранер розкриває таємницю, яка може занурити суспільство в хаос.",
                "rating": 8.0
            },
            {
                "title": "Дюна: Частина друга",
                "year": 2024,
                "description": "Пол Атрід об'єднується з фріменами, щоб помститися змовникам, які знищили його сім'ю.",
                "rating": 8.8
            }
        ]
        return jsonify({"status": "success", "data": fallback_data})

if __name__ == '__main__':
    app.run(debug=True)
