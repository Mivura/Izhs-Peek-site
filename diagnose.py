#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic script to help identify Flask import issues
Run this before app.py to check your environment
"""

import sys
import os

print("=" * 60)
print("Flask Application Diagnostic Tool")
print("=" * 60)

# 1. Check Python version
print("\n1. Python Version:")
print(f"   {sys.version}")
print(f"   Executable: {sys.executable}")

# 2. Check current directory
print("\n2. Current Directory:")
print(f"   {os.getcwd()}")

# 3. Check if required files exist
print("\n3. Required Files Check:")
required_files = [
    'app.py',
    'houses_data.json',
    'requirements.txt',
    'static',
    'templates'
]

for item in required_files:
    exists = "✅" if os.path.exists(item) else "❌"
    print(f"   {exists} {item}")

# 4. Try importing required modules
print("\n4. Module Import Check:")
modules_to_check = [
    'flask',
    'flask_wtf',
    'wtforms',
    'openpyxl',
    'json',
    'os',
    'secrets'
]

all_imports_ok = True
for module in modules_to_check:
    try:
        __import__(module)
        print(f"   ✅ {module}")
    except ImportError as e:
        print(f"   ❌ {module} - Error: {e}")
        all_imports_ok = False

# 5. Check Flask installation
print("\n5. Flask Details:")
try:
    import flask
    print(f"   Version: {flask.__version__}")
    print(f"   Location: {flask.__file__}")
except ImportError as e:
    print(f"   ❌ Flask not installed: {e}")
    all_imports_ok = False

# 6. Check sys.path
print("\n6. Python Path (sys.path):")
for i, path in enumerate(sys.path[:5], 1):
    print(f"   {i}. {path}")
if len(sys.path) > 5:
    print(f"   ... and {len(sys.path) - 5} more")

# 7. Try loading houses_data.json
print("\n7. houses_data.json Check:")
try:
    import json
    basedir = os.path.abspath(os.path.dirname(__file__))
    json_path = os.path.join(basedir, 'houses_data.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    houses = data.get('houses', [])
    print(f"   ✅ JSON loaded successfully")
    print(f"   ✅ Found {len(houses)} houses")
except Exception as e:
    print(f"   ❌ Error loading JSON: {e}")

# 8. Try creating Flask app
print("\n8. Flask App Creation:")
try:
    from flask import Flask
    test_app = Flask(__name__)
    print(f"   ✅ Flask app created successfully")
    print(f"   ✅ App name: {test_app.name}")
    print(f"   ✅ Root path: {test_app.root_path}")
    print(f"   ✅ Static folder: {test_app.static_folder}")
    print(f"   ✅ Template folder: {test_app.template_folder}")
except Exception as e:
    print(f"   ❌ Error creating Flask app: {e}")
    import traceback
    traceback.print_exc()
    all_imports_ok = False

# Final recommendation
print("\n" + "=" * 60)
if all_imports_ok:
    print("✅ All checks passed! You should be able to run app.py")
    print("\nTo run the application:")
    print("   python3 app.py")
    print("\nOr using Flask CLI:")
    print("   export FLASK_APP=app.py")
    print("   flask run")
else:
    print("❌ Some checks failed. Please fix the issues above.")
    print("\nCommon solutions:")
    print("1. Make sure you're in the project directory")
    print("2. Activate your virtual environment:")
    print("   source venv/bin/activate  # Linux/Mac")
    print("   venv\\Scripts\\activate     # Windows")
    print("3. Install requirements:")
    print("   pip install -r requirements.txt")
    print("4. If using PyCharm or VS Code, make sure the")
    print("   interpreter is set to your venv Python")

print("=" * 60)
