import datetime
import os
from django.shortcuts import render
from .settings import FILES_PATH


def file_list(request, date: datetime = None):
    template_name = 'index.html'
    list_names_files = os.listdir(FILES_PATH)
    list_files = []
    for name_file in list_names_files:
        item = {}
        item['name'] = name_file
        # тут ниже тоже срабатывает метод to_url конвертера StrDatetimeConverter (подозрительно):
        item['ctime'] = datetime.datetime.fromtimestamp(os.stat(os.path.join(FILES_PATH, name_file)).st_ctime)
        item['mtime'] = datetime.datetime.fromtimestamp(os.stat(os.path.join(FILES_PATH, name_file)).st_mtime)
        list_files.append(item)
    if date:
        files = filter(lambda item: item['ctime'].date() == date.date(), list_files)
        context_date = date.date()
    else:
        files = list_files
        context_date = None

    context = {
        'files': files,
        'date': context_date
    }
    return render(request, template_name, context)


def file_content(request, name):
    path = os.path.join(FILES_PATH, name)
    file_content = ''
    with open(path, 'r') as file:
        for row in file:
            file_content += f'{row}'

    return render(
        request,
        'file_content.html', context={'file_name': name, 'file_content': file_content}
    )

