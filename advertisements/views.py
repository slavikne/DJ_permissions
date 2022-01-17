from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .models import Advertisement
from .permissions import IsOwnerOrReadOnly, IsAdminOrOwner
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from django.db.models import Q


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров


    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminOrOwner()]
        return []

    def get_queryset(self):
        qs = Advertisement.objects.all()
        if self.request.user.is_anonymous:
             qs = Advertisement.objects.filter(~Q(status='DRAFT')).order_by('id')

        elif self.request.user.is_staff:
             qs = Advertisement.objects.all().order_by('id')

        elif IsOwnerOrReadOnly() or self.request.user.is_authenticated:
             current_user = User.objects.get(username=self.request.user)
             qs = Advertisement.objects.filter(~Q(status='DRAFT') |
                                                    Q(status='DRAFT', creator=current_user)).order_by('id')

        return qs
