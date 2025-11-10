from email.mime.multipart import MIMEMultipart

from flask import Flask, render_template, request, flash, redirect, url_for
from email.mime.text import MIMEText
import smtplib
import os
import secrets


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Optional
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email

# Import house data configuration
from house_data import HOUSES

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
    return render_template('index.html')


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
    houses = [
        {"id": 1, "name": "Дом 0", "image": "dom1_kark/1.jpg", "description": "Современный дом из бруса с просторной террасой."},
        {"id": 2, "name": "Дом 1", "image": "dom2_kark/1.jpg", "description": "Уютный каркасный дом для круглогодичного проживания."},
        {"id": 3, "name": "Дом 2", "image": "dom3_kark/1.jpg", "description": "Классический проект из газобетона с мансардой."},
        {"id": 4, "name": "Дом 3", "image": "dom4_kark/1.jpg", "description": "Классический проект из газобетона с мансардой."},
        {"id": 5, "name": "Дом 4", "image": "dom5_kark/1.jpg", "description": "Классический проект из газобетона с мансардой."},
        {"id": 6, "name": "Дом 4", "image": "dom6_kark/1.jpg", "description": "Классический проект из газобетона с мансардой."},
    ]
    return render_template("catalog.html", houses=houses)

@app.route("/catalog/<int:house_id>")
def project_detail(house_id):
    # здесь можно подгрузить конкретный проект из БД
    return redirect(url_for('house_kark_' + str(house_id)))

    # return render_template("project_detail.html", house_id=house_id)



# ===========================Страницы с домами=============================================

@app.route('/house1')
def house_kark_1():
    house_data = HOUSES.get('dom1_kark')
    return render_template("house_template.html", 
                          house_name=house_data['name'],
                          house_folder=house_data['folder'],
                          specs=house_data['specs'],
                          floor_plans=house_data['floor_plans'],
                          photos=house_data['photos'],
                          features=house_data['features'],
                          prices=house_data['prices'],
                          configurations=house_data['configurations'],
                          services=house_data['services'])


@app.route('/house2')
def house_kark_2():
    house_data = HOUSES.get('dom2_kark')
    return render_template("house_template.html", 
                          house_name=house_data['name'],
                          house_folder=house_data['folder'],
                          specs=house_data['specs'],
                          floor_plans=house_data['floor_plans'],
                          photos=house_data['photos'],
                          features=house_data['features'],
                          prices=house_data['prices'],
                          configurations=house_data['configurations'],
                          services=house_data['services'])


@app.route('/house3')
def house_kark_3():
    house_data = HOUSES.get('dom3_kark')
    return render_template("house_template.html", 
                          house_name=house_data['name'],
                          house_folder=house_data['folder'],
                          specs=house_data['specs'],
                          floor_plans=house_data['floor_plans'],
                          photos=house_data['photos'],
                          features=house_data['features'],
                          prices=house_data['prices'],
                          configurations=house_data['configurations'],
                          services=house_data['services'])


@app.route('/house4')
def house_kark_4():
    house_data = HOUSES.get('dom4_kark')
    return render_template("house_template.html", 
                          house_name=house_data['name'],
                          house_folder=house_data['folder'],
                          specs=house_data['specs'],
                          floor_plans=house_data['floor_plans'],
                          photos=house_data['photos'],
                          features=house_data['features'],
                          prices=house_data['prices'],
                          configurations=house_data['configurations'],
                          services=house_data['services'])


@app.route('/house5')
def house_kark_5():
    house_data = HOUSES.get('dom5_kark')
    return render_template("house_template.html", 
                          house_name=house_data['name'],
                          house_folder=house_data['folder'],
                          specs=house_data['specs'],
                          floor_plans=house_data['floor_plans'],
                          photos=house_data['photos'],
                          features=house_data['features'],
                          prices=house_data['prices'],
                          configurations=house_data['configurations'],
                          services=house_data['services'])


if __name__ == '__main__':
    app.run(debug=True)

# =====================================================================================


# =========================================Черновик============================================================
