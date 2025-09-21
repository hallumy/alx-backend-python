from django.shortcuts import render
from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing conversations
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    


class MessageViewSet(viewsets.ModelViewSet):
    """
    A Viewset for viewing messages
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
