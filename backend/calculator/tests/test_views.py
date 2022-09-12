from rest_framework import status
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from calculator.models import BankOffer

from calculator.views import calculate_monthly_payment


class CreateNewOfferTest(TestCase):

    def setUp(self):
        offer = BankOffer.objects.create(
            bank_name='Test1',
            rate_min=1.8,
            rate_max=6,
            payment_min=100000,
            payment_max=1000000,
            term_min=1,
            term_max=30,
        )
        self.client = APIClient()

        self.valid_payload = {
            "bank_name": "Test2",
            "rate_min": 2.0,
            "rate_max": 10.0,
            "payment_min": 1000000,
            "payment_max": 10000000,
            "term_min": 10,
            "term_max": 30
        }

        self.invalid_payload_rate_min = {
            "bank_name": "Test2",
            "rate_min": -2.0,
            "rate_max": 10.0,
            "payment_min": 1000000,
            "payment_max": 10000000,
            "term_min": 10,
            "term_max": 30
        }

        self.invalid_payload_rate_max = {
            "bank_name": "Test2",
            "rate_min": 2.0,
            "rate_max": -10.0,
            "payment_min": 1000000,
            "payment_max": 10000000,
            "term_min": 10,
            "term_max": 30
        }

        self.invalid_payload_payment_min = {
            "bank_name": "Test2",
            "rate_min": 2.0,
            "rate_max": 10.0,
            "payment_min": -1000000,
            "payment_max": 10000000,
            "term_min": 10,
            "term_max": 30
        }

        self.invalid_payload_payment_max = {
            "bank_name": "Test2",
            "rate_min": 2.0,
            "rate_max": 10.0,
            "payment_min": 1000000,
            "payment_max": -10000000,
            "term_min": 10,
            "term_max": 30
        }

        self.invalid_payload_term_min = {
            "bank_name": "Test2",
            "rate_min": -2.0,
            "rate_max": 10.0,
            "payment_min": 1000000,
            "payment_max": 10000000,
            "term_min": -10,
            "term_max": 30
        }

        self.invalid_payload_term_max = {
            "bank_name": "Test2",
            "rate_min": 2.0,
            "rate_max": 10.0,
            "payment_min": 1000000,
            "payment_max": 10000000,
            "term_min": 10,
            "term_max": -30
        }

        self.invalid_payload_rate_min_more_max = {
            "bank_name": "Test2",
            "rate_min": 10.0,
            "rate_max": 2.0,
            "payment_min": 1000000,
            "payment_max": 10000000,
            "term_min": 10,
            "term_max": 30
        }

        self.invalid_payload_payment_min_more_max = {
            "bank_name": "Test2",
            "rate_min": 2.0,
            "rate_max": 10.0,
            "payment_min": 10000000,
            "payment_max": 1000000,
            "term_min": 10,
            "term_max": 30
        }

        self.invalid_payload_term_min_more_max = {
            "bank_name": "Test2",
            "rate_min": 2.0,
            "rate_max": 10.0,
            "payment_min": 1000000,
            "payment_max": 10000000,
            "term_min": 30,
            "term_max": 10
        }

    def test_offer_list_status_code(self):

        res = self.client.get(reverse('offer-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_offer_detail_status_code(self):

        offer_id = BankOffer.objects.get(bank_name='Test1').id
        response = self.client.get(reverse('offer-detail', args=[offer_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_offer(self):

        response = self.client.post(
            reverse('offer-list'),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_rate_min(self):

        response = self.client.post(
            reverse('offer-list'),
            data=self.invalid_payload_rate_min
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_rate_max(self):

        response = self.client.post(
            reverse('offer-list'),
            data=self.invalid_payload_rate_max
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_payment_min(self):

        response = self.client.post(
            reverse('offer-list'),
            data=self.invalid_payload_payment_min
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_payment_max(self):

        response = self.client.post(
            reverse('offer-list'),
            data=self.invalid_payload_payment_max
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_term_min(self):
        response = self.client.post(
            reverse('offer-list'),
            data=self.invalid_payload_term_min
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_term_max(self):
        response = self.client.post(
            reverse('offer-list'),
            data=self.invalid_payload_term_max
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_rate_min_more_max(self):
        response = self.client.post(
            reverse('offer-list'),
            data=self.invalid_payload_rate_min_more_max
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_payment_min_more_max(self):
        response = self.client.post(
            reverse('offer-list'),
            data=self.invalid_payload_payment_min_more_max
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_term_min_more_max(self):
        response = self.client.post(
            reverse('offer-list'),
            data=self.invalid_payload_term_min_more_max
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ChangeOfferTest(TestCase):

    def setUp(self):
        offer = BankOffer.objects.create(
            bank_name='Test1',
            rate_min=1.8,
            rate_max=6,
            payment_min=100000,
            payment_max=1000000,
            term_min=1,
            term_max=30,
        )
        self.client = APIClient()

        self.valid_payload = {
            "rate_min": 3.0,
        }

        self.invalid_payload_rate_min = {
            "rate_min": -2.0,
        }

        self.invalid_payload_rate_max = {
            "rate_max": -10.0,

        }

        self.invalid_payload_payment_min = {
            "payment_min": -1000000,
        }

        self.invalid_payload_payment_max = {
            "payment_max": -10000000,

        }

        self.invalid_payload_term_min = {
            "term_min": -10,
        }

        self.invalid_payload_term_max = {
            "term_max": -30,
        }

    def test_valid_change_offer(self):
        offer_id = BankOffer.objects.get(bank_name='Test1').id
        response = self.client.patch(
            reverse('offer-detail', args=[offer_id]),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BankOffer.objects.get(bank_name='Test1').rate_min, 3)

    def test_invalid_change_rate_min(self):
        offer_id = BankOffer.objects.get(bank_name='Test1').id
        response = self.client.patch(
            reverse('offer-detail', args=[offer_id]),
            data=self.invalid_payload_rate_min
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_change_rate_max(self):
        offer_id = BankOffer.objects.get(bank_name='Test1').id
        response = self.client.patch(
            reverse('offer-detail', args=[offer_id]),
            data=self.invalid_payload_rate_max
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_change_payment_min(self):
        offer_id = BankOffer.objects.get(bank_name='Test1').id
        response = self.client.patch(
            reverse('offer-detail', args=[offer_id]),
            data=self.invalid_payload_payment_min
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_change_payment_max(self):
        offer_id = BankOffer.objects.get(bank_name='Test1').id
        response = self.client.patch(
            reverse('offer-detail', args=[offer_id]),
            data=self.invalid_payload_payment_max
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_change_term_min(self):
        offer_id = BankOffer.objects.get(bank_name='Test1').id
        response = self.client.patch(
            reverse('offer-detail', args=[offer_id]),
            data=self.invalid_payload_rate_min
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_change_term_max(self):
        offer_id = BankOffer.objects.get(bank_name='Test1').id
        response = self.client.patch(
            reverse('offer-detail', args=[offer_id]),
            data=self.invalid_payload_rate_min
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteOfferTest(TestCase):

    def setUp(self):
        offer = BankOffer.objects.create(
            bank_name='Test1',
            rate_min=1.8,
            rate_max=6,
            payment_min=100000,
            payment_max=1000000,
            term_min=1,
            term_max=30,
        )
        self.client = APIClient()

        self.valid_payload = {
            "rate_min": 3.0,
        }

    def test_delete_offer(self):
        offer_id = BankOffer.objects.get(bank_name='Test1').id
        response = self.client.delete(
            reverse('offer-detail', args=[offer_id]),
        )
        self.assertEqual(BankOffer.objects.filter(bank_name='Test1').exists(), False)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PaymentTest(TestCase):

    def setUp(self):
        BankOffer.objects.create(
            bank_name='Test1',
            rate_min=1.8,
            rate_max=10,
            payment_min=100000,
            payment_max=1500000,
            term_min=10,
            term_max=30,
        )
        BankOffer.objects.create(
            bank_name='Test2',
            rate_min=3,
            rate_max=8,
            payment_min=200000,
            payment_max=1000000,
            term_min=1,
            term_max=20,
        )

        self.client = APIClient()

        self.payload_payment_none = {
            "price": 1600000,
            "deposit": 50000,
            "term": 31,
        }

        self.payload_payment_one_offer = {
            "price": 1100000,
            "deposit": 50000,
            "term": 15,
        }

        self.payload_payment_two_offer = {
            "price": 1100000,
            "deposit": 200000,
            "term": 15,
        }

    def test_payment_none(self):

        response = self.client.get(
            reverse('offer-list'),
            data=self.payload_payment_none
        )
        self.assertEqual(response.data, [])

    def test_payment_one_offer(self):

        response = self.client.get(
            reverse('offer-list'),
            data=self.payload_payment_one_offer
        )
        self.assertTrue(response.data[0]['payment'])

    def test_payment_two_offer(self):

        response = self.client.get(
            reverse('offer-list'),
            data=self.payload_payment_two_offer
        )
        self.assertTrue(response.data[0]['payment'])
        self.assertTrue(response.data[1]['payment'])

    def test_calculate_monthly_payment(self):
        self.assertEqual(
            calculate_monthly_payment(1000000, 200000, 20, 6),
            5731)



