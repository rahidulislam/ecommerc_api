from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsAuthenticatedOrHasSession(permissions.BasePermission):
    """
    Custom permission to allow authenticated users or those with a session to access the view.
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated or has a session
        return request.user.is_authenticated or request.session.session_key
    
    # def has_object_permission(self, request, view, obj):
    #     # Allow access if the user is authenticated or has a session
    #     return request.user and (request.user.is_authenticated or request.session.session_key)