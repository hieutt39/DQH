import json
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy as _
from django.urls import reverse
import uuid

LOAN_STATUS = (
    (0, 'Pending'),
    (1, 'Success'),
    (-1, 'Failed'),
)

CONNECTION_STATUS = (
    (1, 'Enable'),
    (0, 'Disable'),
)

LOAN_TYPE = (
    ('batch', 'Batch'),
    ('api', 'Api'),
)


class LogEntryManager(models.Manager):
    use_in_migrations = True

    def log_action(self, user_id, content_type_id, object_id, object_repr, action_flag, change_message=''):
        if isinstance(change_message, list):
            change_message = json.dumps(change_message)
        return self.model.objects.create(
            user_id=user_id,
            content_type_id=content_type_id,
            object_id=str(object_id),
            object_repr=object_repr[:200],
            action_flag=action_flag,
            change_message=change_message,
        )


def jsonfield_default_value():  # This is a callable
    return dict(table=[])


def default_connection_info():
    return {
        'source': {
            'DRIVER': 'mysql',
            'DATABASE': '',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        },
        'destination': {
            'DRIVER': 'mysql',
            'DATABASE': '',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }


class PrettyJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, indent, sort_keys, **kwargs):
        super().__init__(*args, indent=2, sort_keys=False, **kwargs)


class ToolConnection(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    name = models.CharField(verbose_name=_('Display Name'), null=False, max_length=255)
    db_driver = models.CharField(verbose_name=_('Driver'), default='mysql', null=False, max_length=255)
    db_database = models.CharField(verbose_name=_('Database'), default='web_reservation', null=False, max_length=255)
    db_user = models.CharField(verbose_name=_('Username'), default='root', null=False, max_length=255)
    db_password = models.CharField(verbose_name=_('Password'), default='root', null=False, max_length=255)
    db_host = models.CharField(verbose_name=_('Host'), default='127.0.0.1', null=False, max_length=255)
    db_port = models.CharField(verbose_name=_('Port'), default='3306', null=False, max_length=255)
    extra = models.JSONField(verbose_name=_('Extra'),
                             default=dict,
                             encoder=PrettyJSONEncoder,
                             null=True,
                             blank=True,
                             )
    ssh_tunnel = models.BooleanField(verbose_name=_('Use SSH Tunnel'), default=False)
    ssh_host = models.CharField(verbose_name=_('SSH Host'), default='', blank=True, max_length=255)
    ssh_port = models.CharField(verbose_name=_('SSH Port'), default='22', blank=True, max_length=255)
    ssh_user = models.CharField(verbose_name=_('SSH Username'), default='', blank=True, max_length=255)
    ssh_password = models.CharField(verbose_name=_('SSH Password'), default='', blank=True, max_length=255)
    ssh_rsa = models.FileField(verbose_name=_('RSA file'),
                               upload_to="assets/rsa",
                               default='',
                               blank=True,
                               help_text=_('Enter RSA file')
                               )

    status = models.IntegerField(verbose_name=_('Status'), choices=CONNECTION_STATUS, default=1, help_text="-1: error")
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, null=False)

    objects = LogEntryManager()

    class Meta:
        db_table = 'tool_connection'
        verbose_name = _('DB Connections')
        verbose_name_plural = _('DB Connections')
        ordering = ['-updated_at', '-created_at']

    def __repr__(self):
        return str(self.created_at)

    def __str__(self):
        return f'{self.name}'

    def is_activated(self):
        if self.status == 1:
            return True
        return False


class ToolExecute(models.Model):
    id = models.AutoField(verbose_name=_('ID'), primary_key=True)
    name = models.CharField(verbose_name=_('Name'), null=False, max_length=255)
    label = models.CharField(verbose_name=_('Label'), null=True, max_length=255)
    source = models.ForeignKey(ToolConnection,
                               on_delete=models.SET_NULL,
                               verbose_name=_('Source'),
                               null=True,
                               related_name='execute_source',
                               )
    destination = models.ForeignKey(ToolConnection,
                                    on_delete=models.SET_NULL,
                                    verbose_name=_('Destination'),
                                    null=True,
                                    related_name='execute_destination',
                                    )
    tool_type = models.CharField(verbose_name=_('Type'), choices=LOAN_TYPE, default='batch', null=True, max_length=20)
    payload = models.JSONField(verbose_name=_('Payload'),
                               default=jsonfield_default_value,
                               encoder=PrettyJSONEncoder,
                               null=True)
    status = models.IntegerField(verbose_name=_('Status'), choices=LOAN_STATUS, default=0, help_text="-1: error")
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, null=False)

    objects = LogEntryManager()

    class Meta:
        db_table = 'tool_execute'
        verbose_name = _('Execute')
        verbose_name_plural = _('Executes')
        ordering = ['-created_at', 'name']

    def __repr__(self):
        return str(self.created_at)

    def __str__(self):
        return f'{self.tool_type}: {self.name}'

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def is_activated(self):
        if self.status == 1:
            return True
        return False


class ToolExecuteResult(models.Model):
    title = models.CharField(verbose_name=_('Title'), null=False, max_length=255)
    tool_execute = models.ForeignKey(
        ToolExecute,
        on_delete=models.SET_NULL,
        verbose_name=_('tool execute'),
        null=True,
    )
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the Execute')
    status = models.IntegerField(verbose_name=_('Status'), choices=LOAN_STATUS, default=0, help_text="-1: error")
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, null=False)

    objects = LogEntryManager()

    class Meta:
        db_table = 'tool_execute_result'
        verbose_name = _('Execute Results')
        verbose_name_plural = _('Execute Results')
        ordering = ['-created_at', 'title']

    def __repr__(self):
        return str(self.created_at)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('execute-detail', args=[str(self.id)])


class ToolApiCollection(models.Model):
    name = models.CharField(verbose_name=_('App name'), null=False, max_length=255)
    collection = models.FileField(verbose_name=_('Collection file'),
                                  upload_to="assets/collections",
                                  help_text=_('Enter a collection file to Execute')
                                  )
    environment_source = models.JSONField(verbose_name=_('Environment source'),
                                          default=dict,
                                          encoder=PrettyJSONEncoder,
                                          null=True,
                                          blank=True,
                                          )
    environment_destination = models.JSONField(verbose_name=_('Environment destination'),
                                               default=dict,
                                               encoder=PrettyJSONEncoder,
                                               null=True,
                                               blank=True,
                                               )
    status = models.IntegerField(verbose_name=_('Status'), choices=LOAN_STATUS, default=0, help_text="-1: error")
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, null=False)

    objects = LogEntryManager()

    class Meta:
        db_table = 'tool_api_collection'
        verbose_name = _('Api Collections')
        verbose_name_plural = _('Api Collections')
        ordering = ['-created_at', 'name']

    def __repr__(self):
        return str(self.created_at)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('api-collection', args=[str(self.id)])


class ToolApiCollectionResult(models.Model):
    tool_execute = models.ForeignKey(
        ToolApiCollection,
        on_delete=models.SET_NULL,
        verbose_name=_('tool collection result'),
        null=True,
    )
    diff_data = models.JSONField(verbose_name=_('Diff Data'), default=dict, encoder=PrettyJSONEncoder, null=True)
    diff_analysis = models.JSONField(verbose_name=_('Diff Analysis'), default=dict, encoder=PrettyJSONEncoder,
                                     null=True)
    uid = models.UUIDField(default=uuid.uuid4, null=True, blank=True, max_length=50, primary_key=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, null=False)

    objects = LogEntryManager()

    class Meta:
        db_table = 'tool_api_collection_result'
        verbose_name = _('Api Collection results')
        verbose_name_plural = _('Api Collection results')
        ordering = ['-created_at']

    def __repr__(self):
        return str(self.created_at)

    def __str__(self):
        return self.tool_execute.name


class ToolApiCollectionResultDetail(models.Model):
    tool_execute_result = models.ForeignKey(
        ToolApiCollectionResult,
        on_delete=models.CASCADE,
        verbose_name=_('tool collection result detail'),
        null=True,
    )
    api_name = models.CharField(verbose_name=_('Api name'), null=True, max_length=255)
    compare_data = models.TextField(help_text='Enter a brief description of the Execute', default="")
    diff_data = models.JSONField(verbose_name=_('Diff Data'), default=dict, encoder=PrettyJSONEncoder, null=True)
    result = models.CharField(verbose_name=_('Result'), null=True, max_length=25, default='Failed')
    uid = models.UUIDField(default=uuid.uuid4, null=True, blank=True, max_length=50, primary_key=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, null=False)

    objects = LogEntryManager()

    class Meta:
        db_table = 'tool_api_collection_result_detail'
        verbose_name = _('Api Collection result detail')
        verbose_name_plural = _('Api Collection result detail')
        ordering = ['-created_at']

    def __repr__(self):
        return str(self.created_at)

    def __str__(self):
        return f'{self.tool_execute_result.tool_execute.name}: {self.api_name}'
    
    
class SiteStatistics(models.Model):
    total_visits = models.PositiveIntegerField(default=0)

    @classmethod
    def increment_visits(cls):
        stats, created = cls.objects.get_or_create(id=1)  # Chỉ tạo một bản ghi duy nhất
        stats.total_visits += 1
        stats.save()
        return stats.total_visits
