from email.mime.multipart import MIMEMultipart

from flask import Flask, render_template, request, flash, redirect, url_for
from email.mime.text import MIMEText
import smtplib
import os
import secrets
import json


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Optional
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email

# ===========================Загрузка данных о домах из JSON=============================================
def load_houses_data():
    """Загрузка данных о домах из JSON файла"""
    # Получаем абсолютный путь к директории, где находится app.py
    basedir = os.path.abspath(os.path.dirname(__file__))
    json_path = os.path.join(basedir, 'houses_data.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['houses']

global_houses_kark = ["dom" + str(i) + "_kark/house_1.html" for i in range(1, 5)]
global_houses_brus = ["dom" + str(i) + "_brus/house_1.html" for i in range(1, 5)]
app = Flask(__name__)
print(global_houses_kark)

secret_key = secrets.token_hex(16)
print(secret_key)
SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 465
# yandexsmtpPIK

# ===========================Главное меню=============================================
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-' + secrets.token_hex(16))
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Настройки SMTP для Яндекс
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
# app.config['MAIL_PORT'] = 465
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('YANDEX_EMAIL', 'mitsubishi22122005@yandex.ru')
app.config['MAIL_PASSWORD'] = os.environ.get('YANDEX_APP_PASSWORD', 'irhaserzmzoqarfm')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('YANDEX_EMAIL', 'mitsubishi22122005@yandex.ru')

# Создаем папку для загрузок, если её нет
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# ===========================Главное меню=============================================

@app.route('/')
@app.route('/index')
@app.route('/welcome')
def home():
    """Главная страница с динамической загрузкой проектов"""
    houses = load_houses_data()
    return render_template('index.html', houses=houses)


print()


# ===========================Функция отправки обратной связи=============================================
# Функция для отправки email через Яндекс SMTP

# @app.route('/submit', methods=['POST'])
def send_email(subject, body, to_emails):
    try:
        msg = MIMEMultipart()
        msg['From'] = app.config['MAIL_DEFAULT_SENDER']
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

        text = msg.as_string()
        server.sendmail(app.config['MAIL_DEFAULT_SENDER'], to_emails, text)
        server.quit()

        print("Email успешно отправлен")
        return True
    except Exception as e:
        print(f"Ошибка при отправке email: {str(e)}")
        return False


#

@app.route('/contact', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        # Проверка обязательных полей (только имя, телефон и соглашение)
        if not request.form.get('name') or not request.form.get('phone'):
            flash('Пожалуйста, заполните обязательные поля (Имя и Телефон)', 'error')
            return render_template('contact.html')

        # if not request.form.get('agreement'):
        #     flash('Необходимо принять условия соглашения', 'error')
        #     return render_template('contact.html')

        # КАПЧА БОЛЬШЕ НЕ ОБЯЗАТЕЛЬНА - убрали эту проверку

        # Обработка загруженных файлов
        # uploaded_files = request.files.getlist('files')
        # saved_files = []
        #
        # for file in uploaded_files:
        #     if file and file.filename:
        #         filename = secure_filename(file.filename)
        #         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #         file.save(file_path)
        #         saved_files.append(filename)

        # Формируем данные заявки
        application_data = {
            'name': request.form.get('name'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email'),
            'project': request.form.get('project'),
            'region': request.form.get('region'),
            'comment': request.form.get('comment'),
            # 'files': saved_files
        }

        # Формируем текст для email
        email_body = f"""
        Новая заявка с сайта:

        Имя: {application_data['name']}
        Телефон: {application_data['phone']}
        E-mail: {application_data['email'] or 'Не указан'}
        Название проекта: {application_data['project'] or 'Не указано'}
        Регион строительства: {application_data['region'] or 'Не указан'}
        Комментарий: {application_data['comment'] or 'Не указан'}
       
        """
        # Файлы: {', '.join(application_data['files']) if application_data['files'] else 'Не прикреплены'}
        # Отправляем email
        email_sent = send_email(
            subject='Новая заявка с сайта',
            body=email_body,
            to_emails=[app.config['MAIL_DEFAULT_SENDER']]
        )

        print("Получена новая заявка:", application_data)
        print(f"Email отправлен: {email_sent}")

        flash('Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.', 'success')
        return redirect(url_for('home'))

    return render_template('contact.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    print("=== DEBUG: Contact route called ===")

    if request.method == 'POST':
        print("=== DEBUG: POST request received ===")
        print(f"Form data: {dict(request.form)}")

        # Только проверка имени и телефона
        if not request.form.get('name') or not request.form.get('phone'):
            flash('Пожалуйста, заполните обязательные поля (Имя и Телефон)', 'error')
            return render_template('contact.html')

        print("=== DEBUG: Form validation passed ===")

        # Формируем данные заявки (без файлов)
        application_data = {
            'name': request.form.get('name'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email'),
            'project': request.form.get('project'),
            'region': request.form.get('region'),
            'comment': request.form.get('comment')
        }

        print(f"=== DEBUG: Application data: {application_data} ===")

        # Формируем текст для email
        email_body = f"""
        Новая заявка с сайта:

        Имя: {application_data['name']}
        Телефон: {application_data['phone']}
        E-mail: {application_data['email'] or 'Не указан'}
        Название проекта: {application_data['project'] or 'Не указано'}
        Регион строительства: {application_data['region'] or 'Не указан'}
        Комментарий: {application_data['comment'] or 'Не указан'}
        """

        # Отправляем email
        try:
            email_sent = send_email(
                subject='Новая заявка с сайта',
                body=email_body,
                to_emails=[app.config['MAIL_DEFAULT_SENDER']]
            )
            print(f"=== DEBUG: Email sent: {email_sent} ===")
        except Exception as e:
            print(f"=== DEBUG: Email error: {str(e)} ===")
            email_sent = False

        print("=== DEBUG: Form processed successfully ===")

        # После успешной отправки перенаправляем на главную страницу
        flash('Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.', 'success')
        return redirect(url_for('home'))

    return render_template('contact.html')


# ===========================Отправка суммы в калькуляторе=============================================

@app.route('/submit', methods=['POST'])
def submit():
    # Обработка отправки формы
    selected_services = request.form.getlist('services')
    total = request.form.get('total_amount', 0)
    # Здесь можно добавить логику сохранения заявки
    return redirect(url_for('contact'))
    # return "Заявка отправлена! Сумма: " + total


# ===========================Загрузка меню с контактами=============================================
#
# @app.route("/contact")
# def contact():
#     return render_template("contact.html")

# ===========================  О нас ==============================================================

@app.route('/about')
def AboutUs():
    return render_template('about.html')


# =========================== Каталог домов ========================================================


@app.route("/catalog")
def catalog():
    """Каталог домов с динамической загрузкой из JSON"""
    houses = load_houses_data()
    return render_template("catalog.html", houses=houses)

@app.route("/catalog/<int:house_id>")
def project_detail(house_id):
    """Перенаправление на детальную страницу дома"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == house_id), None)
    if house:
        return redirect(url_for(house['route']))
    return redirect(url_for('catalog'))



# ===========================Страницы с домами=============================================

@app.route('/house1')
def house_kark_1():
    """Страница дома 1 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 1), None)
    photos = house['photos'] if house else []
    return render_template("dom1_kark/house_1.html", photos=photos, house=house)


@app.route('/house2')
def house_kark_2():
    """Страница дома 2 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 2), None)
    photos = house['photos'] if house else []
    return render_template("dom2_kark/house_1.html", photos=photos, house=house)


@app.route('/house3')
def house_kark_3():
    """Страница дома 3 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 3), None)
    photos = house['photos'] if house else []
    return render_template("dom3_kark/house_1.html", photos=photos, house=house)


@app.route('/house4')
def house_kark_4():
    """Страница дома 4 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 4), None)
    photos = house['photos'] if house else []
    return render_template("dom4_kark/house_1.html", photos=photos, house=house)


@app.route('/house5')
def house_kark_5():
    """Страница дома 5 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 5), None)
    photos = house['photos'] if house else []
    return render_template("dom5_kark/house_1.html", photos=photos, house=house)


@app.route('/house6')
def house_kark_6():
    """Страница дома 6 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 6), None)
    photos = house['photos'] if house else []
    return render_template("dom6_kark/house_1.html", photos=photos, house=house)


@app.route('/house7')
def house_kark_7():
    """Страница дома 7 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 7), None)
    photos = house['photos'] if house else []
    return render_template("dom7_kark/house_1.html", photos=photos, house=house)


@app.route('/house8')
def house_kark_8():
    """Страница дома 8 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 8), None)
    photos = house['photos'] if house else []
    return render_template("dom8_kark/house_1.html", photos=photos, house=house)


@app.route('/house9')
def house_kark_9():
    """Страница дома 9 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 9), None)
    photos = house['photos'] if house else []
    return render_template("dom9_kark/house_1.html", photos=photos, house=house)


@app.route('/house10')
def house_kark_10():
    """Страница дома 10 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 10), None)
    photos = house['photos'] if house else []
    return render_template("dom10_kark/house_1.html", photos=photos, house=house)


@app.route('/house11')
def house_kark_11():
    """Страница дома 11 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 11), None)
    photos = house['photos'] if house else []
    return render_template("dom11_kark/house_1.html", photos=photos, house=house)


@app.route('/house12')
def house_kark_12():
    """Страница дома 12 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 12), None)
    photos = house['photos'] if house else []
    return render_template("dom12_kark/house_1.html", photos=photos, house=house)


@app.route('/house13')
def house_kark_13():
    """Страница дома 13 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 13), None)
    photos = house['photos'] if house else []
    return render_template("dom13_kark/house_1.html", photos=photos, house=house)


@app.route('/house14')
def house_kark_14():
    """Страница дома 14 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 14), None)
    photos = house['photos'] if house else []
    return render_template("dom14_kark/house_1.html", photos=photos, house=house)


@app.route('/house15')
def house_kark_15():
    """Страница дома 15 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 15), None)
    photos = house['photos'] if house else []
    return render_template("dom15_kark/house_1.html", photos=photos, house=house)


@app.route('/house16')
def house_kark_16():
    """Страница дома 16 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 16), None)
    photos = house['photos'] if house else []
    return render_template("dom16_kark/house_1.html", photos=photos, house=house)


@app.route('/house17')
def house_kark_17():
    """Страница дома 17 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 17), None)
    photos = house['photos'] if house else []
    return render_template("dom17_kark/house_1.html", photos=photos, house=house)


@app.route('/house18')
def house_kark_18():
    """Страница дома 18 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 18), None)
    photos = house['photos'] if house else []
    return render_template("dom18_kark/house_1.html", photos=photos, house=house)


@app.route('/house19')
def house_kark_19():
    """Страница дома 19 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 19), None)
    photos = house['photos'] if house else []
    return render_template("dom19_kark/house_1.html", photos=photos, house=house)


@app.route('/house20')
def house_kark_20():
    """Страница дома 20 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 20), None)
    photos = house['photos'] if house else []
    return render_template("dom20_kark/house_1.html", photos=photos, house=house)


@app.route('/house21')
def house_kark_21():
    """Страница дома 21 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 21), None)
    photos = house['photos'] if house else []
    return render_template("dom21_kark/house_1.html", photos=photos, house=house)


@app.route('/house22')
def house_kark_22():
    """Страница дома 22 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 22), None)
    photos = house['photos'] if house else []
    return render_template("dom22_kark/house_1.html", photos=photos, house=house)


@app.route('/house23')
def house_kark_23():
    """Страница дома 23 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 23), None)
    photos = house['photos'] if house else []
    return render_template("dom23_kark/house_1.html", photos=photos, house=house)


@app.route('/house24')
def house_kark_24():
    """Страница дома 24 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 24), None)
    photos = house['photos'] if house else []
    return render_template("dom24_kark/house_1.html", photos=photos, house=house)


@app.route('/house25')
def house_kark_25():
    """Страница дома 25 с динамической загрузкой данных"""
    houses = load_houses_data()
    house = next((h for h in houses if h['id'] == 25), None)
    photos = house['photos'] if house else []
    return render_template("dom25_kark/house_1.html", photos=photos, house=house)


if __name__ == '__main__':
    app.run(debug=True)

# if os.environ.get('PRODUCTION'):
#     app.config['DEBUG'] = False
# =====================================================================================


# =========================================Черновик============================================================
