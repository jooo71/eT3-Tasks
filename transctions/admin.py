from django.contrib import admin
from .models import User ,Transaction
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'balance', 'is_active', 'is_staff')  # Columns to display in the list view
    search_fields = ('name', 'phone_number')  # Enable searching by name or phone number
    list_filter = ('is_active', 'is_staff')  # Filters for active/staff status
    ordering = ('name',)  # Default ordering by name
    def delete_model(self, request, obj):
        # Delete all transactions related to the user before deleting the user
        Transaction.objects.filter(sender=obj).delete()
        Transaction.objects.filter(recipient=obj).delete()
        # Now delete the user
        super().delete_model(request, obj)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'sender', 'recipient', 'amount', 'date')  # Display these columns in the list view
    search_fields = ('sender__name', 'recipient__name', 'transaction_type')  # Enable searching by sender, recipient, or transaction type
    list_filter = ('transaction_type', 'date')  # Filters for transaction type and date
    ordering = ('-date',)  # Default ordering by date (newest first)

admin.site.register(User, UserAdmin)
admin.site.register(Transaction,TransactionAdmin)
