from rest_framework.routers import DefaultRouter

from .views import BankOfferListView

router = DefaultRouter()
router.register(r'offer', BankOfferListView, basename='offer')
