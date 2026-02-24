from django.contrib import admin
from datetime import date

from .models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'is_active', 'due_date', 'created_at', 'days_to_deadline')
    # fields = ('title', 'description', 'status', 'priority', 'is_active', 'due_date', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('due_date', 'is_active',)
    ordering = ('due_date',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description')
        }),

        ('Status & Priority', {
            'fields': ('status', 'priority', 'is_active')
        }),

        ('Dates', {
            'fields': ('due_date',)
        }),

        ('System Info', {
            'fields': ('created_at',),
            'classes': ('collapse',)  # можна зробити згорнутим
        }),
    )

    @admin.display(description="Days to deadline")
    def days_to_deadline(self, obj):
        if obj.due_date:
            return (obj.due_date - obj.created_at.date()).days
        return "-"


admin.site.register(Task, TaskAdmin)
