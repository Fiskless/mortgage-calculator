from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import BankOffer
from .serializers import BankOfferSerializer
from rest_framework import mixins
from django_filters import rest_framework as filters
import django_filters

FILTER_CHOICES = (
    ('rate', 'убыванию минимальной ставки по ипотеке'),
    ('-rate', 'возрастанию минимальной ставки по ипотеке'),
)


def calculate_monthly_payment(price, deposit, term, rate_min):
    month_count_in_year = 12
    monthly_rate = rate_min/(month_count_in_year * 100)
    total_rate = (1 + monthly_rate)**(term * month_count_in_year)
    monthly_payment = (price-deposit) * monthly_rate * total_rate / (total_rate - 1)
    return int(monthly_payment)


class OfferFilter(filters.FilterSet):

    rate_min = django_filters.NumberFilter(field_name='rate_min',
                                           label='Минимальный процент ипотеки',
                                           lookup_expr='lte')

    rate_max = django_filters.NumberFilter(field_name='rate_max',
                                           label='Максимальный процент ипотеки',
                                           lookup_expr='lte')
    payment_min = django_filters.NumberFilter(field_name='payment_min',
                                              label='Минимальный размер кредита в рублях',
                                              lookup_expr='lte')
    payment_max = django_filters.NumberFilter(field_name='payment_max',
                                              label='Максимальный размер кредита в рублях',
                                              lookup_expr='lte',
                                              )
    order = filters.ChoiceFilter(choices=FILTER_CHOICES,
                                 method='make_order_by_rate',
                                 label='Сортировать по:')

    def make_order_by_rate(self, value, queryset, name, ):
        if name == 'rate':
            return value.order_by('-rate_min')
        if name == '-rate':
            return value.order_by('rate_min')
        return value


class BankOfferListView(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = BankOffer.objects.all()
    serializer_class = BankOfferSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OfferFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = BankOfferSerializer(queryset, many=True)
        if self.request.GET.get('price', False) \
                and self.request.GET.get('deposit', False) \
                and self.request.GET.get('term', False):
            price = int(self.request.GET['price'])
            deposit = int(self.request.GET['deposit'])
            term = int(self.request.GET['term'])
            credit_amount = price - deposit
            valid_offers_list = []
            for offer in serializer.data:
                if offer['payment_min'] < credit_amount < offer['payment_max'] \
                        and offer['term_min'] < term < offer['term_max']:
                    offer['payment'] = calculate_monthly_payment(
                        price,
                        deposit,
                        term,
                        offer['term_min']
                    )
                    valid_offers_list.append(offer)
            return Response(valid_offers_list)
        return Response(serializer.data)
