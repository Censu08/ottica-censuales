from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permessi per owner o read-only"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions per tutti
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions solo per owner
        return obj.user == request.user

class IsStoreManagerOrReadOnly(permissions.BasePermission):
    """Permessi per store manager"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Verifica se è manager del negozio
        return (
            request.user.is_staff or 
            hasattr(obj, 'store') and obj.store.manager == request.user
        )

class IsCustomerOnly(permissions.BasePermission):
    """Solo clienti autenticati"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'customer_profile')
        )