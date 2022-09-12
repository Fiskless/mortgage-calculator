from django.test import TestCase

from calculator.models import BankOffer


class BankOfferModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        offer = BankOffer.objects.create(
            bank_name='Test',
            rate_min=1.8,
            rate_max=6,
            payment_min=100000,
            payment_max=1000000,
            term_min=1,
            term_max=30,
        )

    def test_bank_name_max_length(self):
        offer = BankOffer.objects.get(bank_name='Test')
        field_max_length = offer._meta.get_field('bank_name').max_length
        self.assertEquals(field_max_length, 30)

    def test_bank_name_label(self):
        offer = BankOffer.objects.get(bank_name='Test')
        field_label = offer._meta.get_field('bank_name').verbose_name
        self.assertEquals(field_label, 'Наименование банка')

    def test_rate_min_label(self):
        offer = BankOffer.objects.get(bank_name='Test')
        field_label = offer._meta.get_field('rate_min').verbose_name
        self.assertEquals(field_label, 'Минимальная ипотечная ставка')

    def test_rate_max_label(self):
        offer = BankOffer.objects.get(bank_name='Test')
        field_label = offer._meta.get_field('rate_max').verbose_name
        self.assertEquals(field_label, 'Максимальная ипотечная ставка')

    def test_payment_min_label(self):
        offer = BankOffer.objects.get(bank_name='Test')
        field_label = offer._meta.get_field('payment_min').verbose_name
        self.assertEquals(field_label, 'Минимальный размер кредита')

    def test_payment_max_label(self):
        offer = BankOffer.objects.get(bank_name='Test')
        field_label = offer._meta.get_field('payment_max').verbose_name
        self.assertEquals(field_label, 'Максимальный размер кредита')

    def test_term_min_label(self):
        offer = BankOffer.objects.get(bank_name='Test')
        field_label = offer._meta.get_field('term_min').verbose_name
        self.assertEquals(field_label, 'Минимальный срок ипотеки')

    def test_term_max_label(self):
        offer = BankOffer.objects.get(bank_name='Test')
        field_label = offer._meta.get_field('term_max').verbose_name
        self.assertEquals(field_label, 'Максимальный срок ипотеки')
