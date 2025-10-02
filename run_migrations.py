#!/usr/bin/env python3
"""
Скрипт для запуска миграций в правильном порядке
"""

import os
import sys
import subprocess

def run_migrations():
    """Запуск миграций"""
    try:
        # Переходим в директорию проекта
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        
        print("Запуск миграций...")
        print("=" * 40)
        
        # Запускаем миграции с помощью alembic
        result = subprocess.run([
            sys.executable, "-m", "alembic", "upgrade", "head"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Миграции успешно выполнены")
            print(result.stdout)
            return True
        else:
            print("❌ Ошибка при выполнении миграций")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при запуске миграций: {e}")
        return False

def show_current_revision():
    """Показать текущую ревизию"""
    try:
        # Переходим в директорию проекта
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        
        print("Текущая ревизия:")
        print("=" * 40)
        
        # Показываем текущую ревизию
        result = subprocess.run([
            sys.executable, "-m", "alembic", "current"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print("❌ Ошибка при получении текущей ревизии")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при получении текущей ревизии: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "current":
        show_current_revision()
    else:
        run_migrations()