from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Artist, Work
from .serializers import ArtistSerializer, WorkSerializer, ClientSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        client_data = {'user': serializer.data['id'], 'name': serializer.data['username']}
        client_serializer = ClientSerializer(data=client_data)
        if client_serializer.is_valid():
            client_serializer.save()
            return Response(client_serializer.data, status=201)
    return Response(serializer.errors, status=400)

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['work_type']
    search_fields = ['artist__name']

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user.client.artist)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
