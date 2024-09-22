from django.contrib import admin
from .models import User ,Transaction
class UserAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        # Delete all transactions related to the user before deleting the user
        Transaction.objects.filter(sender=obj).delete()
        Transaction.objects.filter(recipient=obj).delete()
        # Now delete the user
        super().delete_model(request, obj)

admin.site.register(User, UserAdmin)
admin.site.register(Transaction)
