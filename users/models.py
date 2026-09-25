from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.decorators import method_decorator


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Почта', help_text='Укажите почту')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Телефон', help_text='Укажите телефон')
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name='Город', help_text='Укажите город')
    avatar = models.ImageField(upload_to='users/avatars', blank=True, null=True, verbose_name='Аватар', help_text='Загрузите аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    cash = 'cash'
    transfer = 'transfer'
    payment_method = [(cash, 'Наличные'), (transfer, 'Перевод'),]

    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='payments', verbose_name='Пользователь', help_text='Укажите кто сделал платёж')
    payment_date = models.DateTimeField(verbose_name='Дата оплаты',help_text='Дата совершения платежа')
    paid_course = models.ForeignKey('materials.Course',on_delete=models.CASCADE,blank=True, null=True,related_name='payments', verbose_name='Оплаченный курс',help_text='Укажите оплаченный курс')
    paid_lesson = models.ForeignKey("materials.Lesson",on_delete=models.CASCADE,blank=True, null=True,related_name="payments",verbose_name="Оплаченный урок",help_text="Укажите оплаченный урок")
    amount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Сумма оплаты",help_text="Укажите сумму оплаты")
    payment_method = models.CharField(max_length=30,choices=payment_method,default=cash,verbose_name="Способ оплаты",help_text="Выберите способ оплаты")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user} — {self.amount}"
