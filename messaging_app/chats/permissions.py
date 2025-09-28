from rest_framework import permissions

class IsParticipantOrSender(permissions.BasePermission):
    """
    Custom permission to allow users to access messages or conversations
    only if they are participants.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
       
        # Conversation objects
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # Message objects
        if hasattr(obj, 'sender') and hasattr(obj, 'conversation'):
            return obj.sender == request.user or request.user in obj.conversation.participants.all()

        return False
