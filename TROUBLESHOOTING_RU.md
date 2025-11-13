# Руководство по устранению неполадок Flask

Это руководство поможет решить проблемы с запуском Flask приложения.

## Быстрая диагностика

Запустите диагностический скрипт:

```bash
python3 diagnose.py
```

Скрипт проверит вашу среду и укажет на проблемы.

## Частые ошибки и решения

### Ошибка 1: ImportError: No module named 'flask'

**Проблема:** Flask не установлен или виртуальное окружение не активировано.

**Решение:**

1. Активируйте виртуальное окружение:
   ```bash
   # Linux/Mac
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Проверьте установку:
   ```bash
   python -c "import flask; print(flask.__version__)"
   ```

### Ошибка 2: ModuleNotFoundError в Flask scaffold.py

**Проблема:** Flask не может найти модуль приложения. Обычно связано с:
- Запуск из неправильной директории
- Конфликт имён файлов
- Проблемы с путями Python

**Решение:**

1. Убедитесь, что вы в корневой директории проекта:
   ```bash
   cd /path/to/Izhs-Peek-site
   ls -la  # должны видеть app.py, requirements.txt и т.д.
   ```

2. Проверьте, что нет файла с именем `flask.py` в директории проекта:
   ```bash
   ls -la flask.py  # должно быть "No such file"
   ```

3. Убедитесь, что `__pycache__` не вызывает проблем:
   ```bash
   find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
   find . -name "*.pyc" -delete
   ```

4. Попробуйте запустить с явным указанием модуля:
   ```bash
   python3 -m flask run
   ```

### Ошибка 3: FileNotFoundError: houses_data.json

**Проблема:** Приложение не находит JSON файл с данными.

**Решение:**

1. Проверьте наличие файла:
   ```bash
   ls -la houses_data.json
   ```

2. Убедитесь, что вы запускаете app.py из корневой директории проекта.

### Ошибка 4: Ошибки импорта templates/static

**Проблема:** Flask не находит шаблоны или статические файлы.

**Решение:**

1. Проверьте структуру директорий:
   ```bash
   ls -la static/ templates/
   ```

2. Убедитесь, что имеете права на чтение:
   ```bash
   chmod -R 755 static/ templates/
   ```

## Правильная последовательность запуска

### Шаг 1: Перейдите в директорию проекта

```bash
cd /path/to/Izhs-Peek-site
```

### Шаг 2: Создайте виртуальное окружение (если ещё не создано)

```bash
python3 -m venv venv
```

### Шаг 3: Активируйте виртуальное окружение

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

После активации в начале строки должно появиться `(venv)`.

### Шаг 4: Установите зависимости

```bash
pip install -r requirements.txt
```

### Шаг 5: Запустите приложение

**Метод 1 - Прямой запуск:**
```bash
python3 app.py
```

**Метод 2 - Через Flask CLI:**
```bash
export FLASK_APP=app.py
flask run
```

**Метод 3 - С отладкой:**
```bash
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run
```

## Проверка окружения

### Проверить версию Python

```bash
python3 --version
```

Требуется Python 3.8 или выше.

### Проверить установленные пакеты

```bash
pip list | grep -i flask
```

Должны увидеть:
- Flask
- Flask-WTF
- flask-wtf (может быть одно или оба)

### Проверить путь Python

```bash
which python3
```

При активированном venv должен показывать путь к venv/bin/python3.

## Специфические проблемы Windows

### PowerShell Execution Policy

Если получаете ошибку при активации venv:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Кодировка

Убедитесь, что Windows использует UTF-8:

```cmd
chcp 65001
```

## Логи и отладка

### Включить подробные логи Flask

В app.py временно добавьте:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Запустить с полным traceback

```bash
python3 -u app.py 2>&1 | tee app.log
```

Это сохранит все выходные данные в `app.log`.

## Проблемы с PyCharm/VS Code

### PyCharm

1. Откройте Settings → Project → Python Interpreter
2. Убедитесь, что выбран интерпретатор из venv
3. Нажмите на шестерёнку → Show All → Refresh

### VS Code

1. Откройте Command Palette (Ctrl+Shift+P)
2. Наберите "Python: Select Interpreter"
3. Выберите интерпретатор из venv (./venv/bin/python)

## Проверка портов

Если Flask жалуется, что порт занят:

```bash
# Linux/Mac
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## Полная переустановка

Если ничего не помогает:

```bash
# 1. Деактивируйте venv
deactivate

# 2. Удалите старое окружение
rm -rf venv/

# 3. Создайте новое
python3 -m venv venv

# 4. Активируйте
source venv/bin/activate  # или venv\Scripts\activate на Windows

# 5. Обновите pip
pip install --upgrade pip

# 6. Установите зависимости
pip install -r requirements.txt

# 7. Запустите приложение
python3 app.py
```

## Получить помощь

Если проблема не решена, предоставьте следующую информацию:

1. Вывод `diagnose.py`
2. Полный текст ошибки (traceback)
3. Вывод команд:
   ```bash
   python3 --version
   pip list
   pwd
   ls -la
   ```

## Контрольный список перед запуском

- [ ] Находитесь в корневой директории проекта
- [ ] Виртуальное окружение активировано (видно `(venv)`)
- [ ] Зависимости установлены (`pip list` показывает Flask)
- [ ] Файл `houses_data.json` существует
- [ ] Папки `static/` и `templates/` существуют
- [ ] Нет конфликтов имён файлов (нет `flask.py` в проекте)
- [ ] Python 3.8 или выше
- [ ] Порт 5000 свободен

Если все пункты выполнены, приложение должно запуститься без ошибок.
