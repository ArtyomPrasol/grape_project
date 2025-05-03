import os

def remove_extension(file_name):
    """Убирает расширение файла"""
    return os.path.splitext(file_name)[0]

def list_to_dict(lst):
    """Преобразует список формата [[1 Привет], [2 Пока]] в словарь вида {1: 'Привет', 2: 'Пока'}"""
    return {item[0]: item[1] for item in lst} 