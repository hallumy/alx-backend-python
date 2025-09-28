from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from .permissions import IsParticipantOrSender


class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing conversations
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOrSender]
    
    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)


    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with  participants
        Expected POST data: {"participants": [user_id1, user_id2]}
        """
        participant_ids = request.data.get('participants', [])
        if not participant_ids:
            return Response({"error": "No participant provided"}, status=400)


        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)
        for customuser_id in participant_ids:
            try:
                user = CustomUser.objects.get(pk=customuser_id)
                conversation.participants.add(user)
            except CustomUser.DoesNotExist:
                continue

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class MessageViewSet(viewsets.ModelViewSet):
    """
    A Viewset for viewing messages
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOrSender]
    filter_backends = [filters.SearchFilter]
    search_fields = ['message']
    def get_queryset(self):
        return self.queryset.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """
        Create a message in a conversation
        Expected POST data: {"conversation": id, "content": mesage}
        """
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise PermissionError("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user)