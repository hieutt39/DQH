from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .models import ToolExecute, ToolExecuteResult, \
    ToolConnection, ToolApiCollection, \
    ToolApiCollectionResult, ToolApiCollectionResultDetail

admin.site.site_header = 'RRK Admin Tools'
admin.site.site_title = "RRK"
admin.site.index_title = "RRK"


@admin.register(ToolConnection)
class ConnectionAdmin(admin.ModelAdmin):
    @admin.display(description='Created At')
    def admin_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    @admin.display(description='Updated At')
    def admin_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M')

    @admin.display(boolean=True, ordering="status", description='Status')
    def admin_status(self, obj):
        return False if obj.status else True

    # fieldsets = [
    #     (None, {"fields": ['name', 'connection_info', 'status']}),
    #     ("Date information", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    # ]

    # list_display = [field.name for field in ToolConnection._meta.get_fields()]
    # list_display.remove('id')
    # list_display.remove('toolexecuteresult')
    # for i in range(len(list_display)):
    #     if list_display[i] == 'status':
    #         list_display[i] = 'admin_status'
    #     if list_display[i] == 'created_at':
    #         list_display[i] = 'admin_created_at'
    #     if list_display[i] == 'updated_at':
    #         list_display[i] = 'admin_updated_at'

    # list_filter = ('status', 'name', 'label')


@admin.register(ToolExecute)
class ExecuteAdmin(admin.ModelAdmin):
    @admin.display(description='Created At')
    def admin_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    @admin.display(description='Updated At')
    def admin_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M')

    @admin.display(boolean=True, ordering="status", description='Status')
    def admin_status(self, obj):
        return False if obj.status else True

    fieldsets = [
        ("Connections", {"fields": [("source", "destination")]}),
        ("Basic Information", {"fields": ["name", "label", "tool_type", "payload", "status"]}),
        ("Date Information", {"fields": [("created_at", "updated_at")], "classes": ["collapse"]}),
    ]

    list_display = [field.name for field in ToolExecute._meta.get_fields()]
    list_display.remove('id')
    list_display.remove('toolexecuteresult')
    for i in range(len(list_display)):
        if list_display[i] == 'status':
            list_display[i] = 'admin_status'
        if list_display[i] == 'created_at':
            list_display[i] = 'admin_created_at'
        if list_display[i] == 'updated_at':
            list_display[i] = 'admin_updated_at'

    # list_filter = ('status', 'name', 'label')


@admin.register(ToolExecuteResult)
class ExecuteResultAdmin(admin.ModelAdmin):
    @admin.display(description='Created At')
    def admin_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    @admin.display(description='Updated At')
    def admin_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M')

    @admin.display(boolean=True, ordering="status", description='Status')
    def admin_status(self, obj):
        return False if obj.status else True

    @admin.display(ordering="summary", description='Summary')
    def admin_summary(self, obj):
        return mark_safe(obj.summary)

    # fieldsets = [
    #     (None, {"fields": ["title", "tool_type", "payload", "status"]}),
    #     ("Date information", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    # ]

    list_display = [field.name for field in ToolExecuteResult._meta.get_fields()]
    list_display.remove('id')
    for i in range(len(list_display)):
        if list_display[i] == 'status':
            list_display[i] = 'admin_status'
        if list_display[i] == 'created_at':
            list_display[i] = 'admin_created_at'
        if list_display[i] == 'updated_at':
            list_display[i] = 'admin_updated_at'
        if list_display[i] == 'summary':
            list_display[i] = 'admin_summary'

    # list_filter = ('status', 'name', 'label')


@admin.register(ToolApiCollection)
class ApiCollectionAdmin(admin.ModelAdmin):
    @admin.display(description='Created At')
    def admin_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    @admin.display(description='Updated At')
    def admin_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M')

    @admin.display(boolean=True, ordering="status", description='Status')
    def admin_status(self, obj):
        return False if obj.status else True


@admin.register(ToolApiCollectionResult)
class ApiCollectionResultAdmin(admin.ModelAdmin):
    @admin.display(description='Created At')
    def admin_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    @admin.display(description='Updated At')
    def admin_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M')

    @admin.display(ordering="diff_analysis", description='diff analysis')
    def admin_diff_analysis(self, obj):
        return mark_safe(obj.diff_analysis)

    list_display = ['tool_execute', 'admin_diff_analysis', 'created_at', 'updated_at']


@admin.register(ToolApiCollectionResultDetail)
class ApiCollectionResultDetailAdmin(admin.ModelAdmin):
    @admin.display(description='Created At')
    def admin_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    @admin.display(description='Updated At')
    def admin_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M')

    list_display = ['api_name', 'tool_execute_result', 'uid', 'result', 'created_at', 'updated_at']
    # readonly_fields = ['diff_data']

    # def diff_data(self, instance):
    #     return format_html(instance.diff_data) + "ASdasd"

    for i in range(len(list_display)):
        if list_display[i] == 'created_at':
            list_display[i] = 'admin_created_at'
        if list_display[i] == 'updated_at':
            list_display[i] = 'admin_updated_at'

# admin.site.register(ToolExecute, ExecuteAdmin)
# admin.site.register(ToolExecuteResult, ExecuteResultAdmin)
