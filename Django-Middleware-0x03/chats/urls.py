from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet
from rest_framework import routers
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter


router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]
