from rest_framework import status
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from calculator.models import BankOffer


class OfferFiltersTest(TestCase):

    def setUp(self):
        BankOffer.objects.create(
            bank_name='Test1',
            rate_min=1.8,
            rate_max=10,
            payment_min=100000,
            payment_max=1500000,
            term_min=1,
            term_max=30,
        )
        BankOffer.objects.create(
            bank_name='Test2',
            rate_min=3,
            rate_max=8,
            payment_min=200000,
            payment_max=1000000,
            term_min=1,
            term_max=30,
        )

        self.client = APIClient()

        self.payload_filter_rate_min = {
            "rate_min": 2.0,
        }

        self.payload_filter_rate_max = {
            "rate_max": 9.0,
        }

        self.payload_filter_payment_min = {
            "payment_min": 150000,
        }

        self.payload_filter_payment_max = {
            "payment_max": 1200000,
        }

        self.payload_order_decrease_filter = {
            "order": 'rate',
        }

        self.payload_order_increase_filter = {
            "order": '-rate',
        }

    def test_filter_rate_min(self):

        response = self.client.get(
            reverse('offer-list'),
            data=self.payload_filter_rate_min
        )
        self.assertEqual(response.data[0]['rate_min'], 1.8)
        self.assertEqual(len(response.data), 1)

    def test_filter_rate_max(self):

        response = self.client.get(
            reverse('offer-list'),
            data=self.payload_filter_rate_max
        )
        self.assertEqual(response.data[0]['rate_max'], 8)
        self.assertEqual(len(response.data), 1)

    def test_filter_payment_min(self):

        response = self.client.get(
            reverse('offer-list'),
            data=self.payload_filter_payment_min
        )
        self.assertEqual(response.data[0]['payment_min'], 100000)
        self.assertEqual(len(response.data), 1)

    def test_filter_payment_max(self):

            response = self.client.get(
                reverse('offer-list'),
                data=self.payload_filter_payment_max
            )
            self.assertEqual(response.data[0]['payment_max'], 1000000)
            self.assertEqual(len(response.data), 1)

    def test_order_decrease_filter(self):

            response = self.client.get(
                reverse('offer-list'),
                data=self.payload_order_decrease_filter
            )
            current_rate_min_list = [response.data[0]['rate_min'], response.data[1]['rate_min']]
            self.assertEqual(current_rate_min_list, [3.0, 1.8])

    def test_order_increase_filter(self):

            response = self.client.get(
                reverse('offer-list'),
                data=self.payload_order_increase_filter
            )
            current_rate_min_list = [response.data[0]['rate_min'], response.data[1]['rate_min']]
            self.assertEqual(current_rate_min_list, [1.8, 3.0])