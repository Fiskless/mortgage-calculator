from django.db import models
from django.core.validators import MinValueValidator


class BankOffer(models.Model):

    bank_name = models.CharField(
        verbose_name='Наименование банка',
        max_length=30,
        unique=True
    )
    rate_min = models.FloatField(
        verbose_name='Минимальная ипотечная ставка',
        help_text='Введите ставку в процентах',
        validators=[MinValueValidator(0.0)]
    )
    rate_max = models.FloatField(
        verbose_name='Максимальная ипотечная ставка',
        help_text='Введите ставку в процентах',
        validators=[MinValueValidator(0.0)]
    )
    payment_min = models.PositiveIntegerField(
        verbose_name='Минимальный размер кредита',
        help_text='Минимальный размер кредита в рублях без копеек',
    )
    payment_max = models.PositiveIntegerField(
        verbose_name='Максимальный размер кредита',
        help_text='Максимальный размер кредита в рублях без копеек',
    )
    term_min = models.PositiveIntegerField(
        verbose_name='Минимальный срок ипотеки',
        help_text='Срок ипотеки в годах',
    )
    term_max = models.PositiveIntegerField(
        verbose_name='Максимальный срок ипотеки',
        help_text='Срок ипотеки в годах',
    )

    class Meta:
        verbose_name = 'Предложение банка'
        verbose_name_plural = 'Предложения банков'

    def __str__(self):
        return self.bank_name