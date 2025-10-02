#!/usr/bin/env python3
"""
Анализ моделей для определения используемых схем
"""

import os
import sys
import ast
import glob

def analyze_model_file(file_path):
    """Анализирует файл модели для поиска схем"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Парсим файл как AST
        tree = ast.parse(content)
        
        schemas = set()
        
        # Ищем классы, наследующиеся от Base
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Проверяем, есть ли у класса атрибут __table_args__
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name) and target.id == '__table_args__':
                                if isinstance(item.value, ast.Dict):
                                    # Ищем ключ 'schema' в словаре
                                    for key, value in zip(item.value.keys, item.value.values):
                                        if isinstance(key, ast.Str) and key.s == 'schema':
                                            if isinstance(value, ast.Str):
                                                schemas.add(value.s)
        
        return schemas
    except Exception as e:
        print(f"Ошибка при анализе файла {file_path}: {e}")
        return set()

def analyze_all_models():
    """Анализирует все файлы моделей в проекте"""
    # Пути к директориям с моделями
    model_dirs = [
        'app/models',
        'app/models/calendar'
    ]
    
    all_schemas = set()
    
    print("Анализ файлов моделей:")
    
    for model_dir in model_dirs:
        if os.path.exists(model_dir):
            # Ищем все .py файлы в директории
            for file_path in glob.glob(os.path.join(model_dir, '*.py')):
                if os.path.isfile(file_path):
                    schemas = analyze_model_file(file_path)
                    if schemas:
                        print(f"  {file_path}:")
                        for schema in schemas:
                            print(f"    - {schema}")
                            all_schemas.add(schema)
                    else:
                        print(f"  {file_path}: схемы не найдены")
    
    print(f"\nВсего найдено уникальных схем: {len(all_schemas)}")
    for schema in sorted(all_schemas):
        print(f"  - {schema}")
    
    return all_schemas

if __name__ == "__main__":
    schemas = analyze_all_models()