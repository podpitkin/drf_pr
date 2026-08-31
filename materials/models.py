from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название курса', help_text='Укажите название курса')
    preview = models.ImageField(upload_to='materials/previews', blank=True, null=True, verbose_name='Превью', help_text='Загрузите картинку')
    discription = models.TextField(blank=True, null=True, verbose_name='Описание курса', help_text='Укажите описание курса')

    class  Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название курса', help_text='Укажите название курса')
    discription = models.TextField(blank=True, null=True, verbose_name='Описание урока', help_text='Укажите описание урока')
    preview = models.ImageField(upload_to='materials/previews', blank=True, null=True, verbose_name='Превью', help_text='Загрузите картинку')
    link = models.CharField(max_length=300, verbose_name='Ссылка на видео', help_text='Укажите ссылку на видео')

    class  Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'