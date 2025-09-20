from rest_framework import serializers
from chats.models import CustomUser, Conversation, Message

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for Django's built-in CustomUser model.

    Serializes basic user information including id, username, email,
    first name, and last name.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'user_name', 'email', 'password', 'phone_number', 'role']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.

    Includes the nested sender information using CustomUserSerializer.
    Serializes message body, sender_id, timestamp.
    """
    sender_id = CustomUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.

    Includes nested participants (users) and nested messages using
    CustomUserSerializer and MessageSerializer respectively.

    Both participants and messages are marked as read-only to indicate
    they are only included for representation purposes and not
    writable through this serializer by default.
    """
    participants_id = CustomUserSerializer(many=True, Read_only=True)
    message_body = MessageSerializer(many=True, Read_only=True)


    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participant_id', 'message_body', 'created_at' ]
