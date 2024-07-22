from rest_framework import viewsets, permissions
from . import serializers, models


class ProductCategory(viewsets.ModelViewSet):
    serializer_class=serializers.CategorySerializer
    queryset = models.Category.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    

class ProductCrudEndpoints(viewsets.ModelViewSet):
    queryset= models.Product.objects.all()   

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.ProductSerializer      
        return serializers.ProductCreateSerializer