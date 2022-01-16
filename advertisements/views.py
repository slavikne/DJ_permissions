from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import render
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
    permission_classes = [IsOwnerOrReadOnly | IsAdminUser]
    filterset_class = AdvertisementFilter

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['creator', 'created_at']
    search_fields = ['title']
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    def list(self, request):

        if request.user.is_anonymous:
             queryset = Advertisement.objects.filter(~Q(status='DRAFT')).order_by('id')

        elif request.user.is_staff:
             queryset = Advertisement.objects.all().order_by('id')

        elif IsOwnerOrReadOnly() or request.user.is_authenticated:
             current_user = User.objects.get(username=request.user)
             queryset = Advertisement.objects.filter(~Q(status='DRAFT') |
                                                    Q(status='DRAFT', creator=current_user)).order_by('id')

        serializer = AdvertisementSerializer(queryset, many=True)
        return Response(serializer.data)


    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminOrOwner()]
        return []


