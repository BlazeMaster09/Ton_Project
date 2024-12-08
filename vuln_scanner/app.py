from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Vulnerability
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vulnerabilities.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)

# Главная страница
@app.route('/')
def index():
    
    return render_template('index.html')
@app.route('/index')
def home():
    
    return render_template('main.html')


@app.route('/main')
def main():
    
    return render_template('/main.html')

@app.route('/sign-up')
def signup():
    return render_template('/sign-up.html')


@app.route('/testip')
def testip():
    return render_template('/testip.html')

@app.route('/story')
def story():
    return render_template('/story.html')



# Парсинг данных
@app.route('/parse', methods=['POST'])
def parse():
    try:
        url = "https://sploitus.com/?query=Exploit#exploits"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            search_results = soup.find('div', id='search-results')

            if search_results:
                for result in search_results.find_all('div', class_='card'):  # Примерная структура
                    vuln_id = result.get('data-id', 'N/A')  # Примерное поле
                    title = result.find('h2').text.strip() if result.find('h2') else 'No Title'
                    description = result.find('p').text.strip() if result.find('p') else 'No Description'
                    published_date = result.find('time').text.strip() if result.find('time') else 'Unknown Date'
                    source_link = result.find('a', href=True)['href'] if result.find('a', href=True) else 'No Link'

                    # Сохранение в БД
                    vulnerability = Vulnerability(
                        vuln_id=vuln_id,
                        title=title,
                        description=description,
                        published_date=published_date,
                        source_link=source_link
                    )
                    db.session.add(vulnerability)

                db.session.commit()
                flash("Данные успешно спарсены и сохранены!", "success")
            else:
                flash("Не удалось найти раздел 'search-results'", "danger")
        else:
            flash(f"Ошибка запроса: {response.status_code}", "danger")

    except Exception as e:
        flash(f"Ошибка парсинга: {str(e)}", "danger")

    return redirect(url_for('index'))

# Инициализация базы данных
@app.cli.command('init-db')
def init_db():
    db.create_all()
    print("База данных успешно инициализирована.")

if __name__ == '__main__':
    app.run(debug=True)
