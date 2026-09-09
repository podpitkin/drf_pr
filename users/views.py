from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from users.models import Payment
from users.serializers import PaymentSerializer, UserSerializer


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer


class PaymentListCreateView(ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ["payment_date"]
    ordering = ["payment_date"]