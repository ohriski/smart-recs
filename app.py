from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Наша локальна база даних фільмів (імітація AI)
MOVIES_DB = {
    "sci-fi": [
        {"title": "Дюна: Частина друга", "year": 2024, "rating": 8.8, "description": "Пол Атрід об'єднується з фріменами для помсти змовникам."},
        {"title": "Інтерстеллар", "year": 2014, "rating": 8.6, "description": "Подорож крізь червоточину в пошуках нового дому для людства."},
        {"title": "Той, що біжить по лезу 2049", "year": 2017, "rating": 8.0, "description": "Розкриття таємниці, що загрожує занурити суспільство в хаос."},
        {"title": "Матриця", "year": 1999, "rating": 8.7, "description": "Хакер дізнається, що світ навколо — це симуляція."}
    ],
    "comedy": [
        {"title": "Похмілля у Вегасі", "year": 2009, "rating": 7.7, "description": "Друзі намагаються згадати події бурхливої ночі."},
        {"title": "Дедпул і Росомаха", "year": 2024, "rating": 8.1, "description": "Божевільний дует рятує мультивсесвіт."},
        {"title": "Гранд Готель Будапешт", "year": 2014, "rating": 8.1, "description": "Пригоди консьєржа у вигаданій європейській країні."},
        {"title": "Круті легаві", "year": 2007, "rating": 7.8, "description": "Поліцейський переїжджає в тихе село, де коїться щось дивне."}
    ],
    "drama": [
        {"title": "Втеча з Шоушенка", "year": 1994, "rating": 9.3, "description": "Історія надії та дружби у стінах в'язниці."},
        {"title": "Оппенгеймер", "year": 2023, "rating": 8.4, "description": "Історія створення атомної бомби та її наслідків."},
        {"title": "Паразити", "year": 2019, "rating": 8.5, "description": "Бідна сім'я хитрощами проникає в будинок багатіїв."},
        {"title": "Список Шиндлера", "year": 1993, "rating": 9.0, "description": "Історія бізнесмена, який рятує тисячі життів."}
    ],
    "horror": [
        {"title": "Чужий", "year": 1979, "rating": 8.5, "description": "Екіпаж корабля стикається з ідеальним хижаком."},
        {"title": "Сяйво", "year": 1980, "rating": 8.4, "description": "Письменник божеволіє у ізольованому готелі."},
        {"title": "Воно", "year": 2017, "rating": 7.3, "description": "Група дітей протистоїть стародавньому злу в образі клоуна."},
        {"title": "Тихе місце", "year": 2018, "rating": 7.5, "description": "Сім'я виживає в повній тиші, ховаючись від монстрів."}
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    selected_genre = data.get('genre')
    
    # Отримуємо фільми з нашої бази. Якщо жанру немає - повертаємо порожній список
    movies = MOVIES_DB.get(selected_genre, [])
    
    # Імітація затримки, щоб виглядало, ніби сервер "думає" (можна прибрати)
    import time
    time.sleep(0.5)

    return jsonify({"status": "success", "data": movies})

if __name__ == '__main__':
    app.run(debug=True)
