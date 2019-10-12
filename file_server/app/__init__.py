from django.urls import register_converter
from app.converter import StrDatetimeConverter

register_converter(StrDatetimeConverter, 'StrDatetimeConverter')
