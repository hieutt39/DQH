import datetime
import json

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from src.management.pos_batch.services.sync_message import SyncMessage
from src.management.pos_batch.services.compare_schema_service import CompareSchemaService
from src.management.pos_batch.services.compare_data_services import CompareDataService
from src.management.pos_batch.services.compare_api_service import CompareApiService
from .models import ToolExecute, ToolExecuteResult, ToolApiCollection, \
    ToolApiCollectionResult, ToolApiCollectionResultDetail, ToolConnection
from src.utilities.extract_db.core import *

sync_message = SyncMessage()
configs = {
    "CreateShopCourses": ['albums', 'artists'],
    "DeleteShopConnectionLogs": ['customers']
}


def get_command_class(command_name, record):
    source_info = {
        'hostname': record.source.db_host,
        'port': record.source.db_port,
        'username': record.source.db_user,
        'password': record.source.db_password,
        'database': record.source.db_database,
    }
    destination_info = {
        'hostname': record.destination.db_host,
        'port': record.destination.db_port,
        'username': record.destination.db_user,
        'password': record.destination.db_password,
        'database': record.destination.db_database,
    }
    if command_name == 'compare_schema':
        command = CompareSchemaService(source_info, destination_info)
    elif command_name == 'compare_data':
        command = CompareDataService(source_info, destination_info)
    else:
        command = None

    return command


def pre_process(data_post):
    command_name = data_post.get('command')
    batch_name = data_post.get('batch_name')

    if batch_name == '':
        records = ToolExecute.objects.filter(status=0)
        for record in records:
            command = get_command_class(command_name, record)
            if len(record.payload.get('tables')):
                execute_process(command, record.payload.get('tables'), record)
    else:
        record = ToolExecute.objects.get(name__in=[batch_name])
        command = get_command_class(command_name, record)
        if len(record.payload.get('tables')):
            execute_process(command, record.payload.get('tables'), record)


def execute_process(command, tables, record):
    try:
        if command is not None:
            sync_message.send_message(f'<div class="box-title text-bold">{record.name}</div>')
            df = command.exec_process(tables, tables, False)
            str_html = df.to_html(classes="table table-bordered table-hover dataTable table-striped",
                                  justify="center",
                                  )
            # sync_message.send_message(str_html)
            # Save report to database
            tool_execute_result = ToolExecuteResult(tool_execute_id=record.id,
                                                    # summary=json.dumps(df.to_json(orient="split"), indent=2),
                                                    summary=str_html,
                                                    title=record.label
                                                    )
            tool_execute_result.save()
        else:
            sync_message.send_message("<div class='txt-red'>Input validate</div>")
    except Exception as e:
        sync_message.send_message(str(e))


@login_required(login_url="admin:login")
def index(request, template_name='tools/index.html'):
    return TemplateResponse(request, template_name, {})


@login_required(login_url="admin:login")
def index_batch(request, template_name='tools/index_batch.html'):
    if request.method == 'POST':
        pre_process(request.POST)

    commands = {
        'compare_schema': "Compare Schema",
        'compare_data': "Compare Data"
    }
    # batch_names = {
    #     'CreateShopCourses': "Create Shop Courses",
    #     'DeleteShopConnectionLogs': "Delete Shop Connection Logs",
    # }
    batch_names = {}
    records = ToolExecute.objects.filter(status=0)
    for record in records:
        batch_names[record.name] = record.label

    context = {
        'title': _('Tools'),
        'commands': commands,
        'batch_names': batch_names,
    }
    return TemplateResponse(request, template_name, context)


@login_required(login_url="admin:login")
def index_api(request, template_name='tools/index_api.html'):
    items = ToolApiCollection.objects.filter(status=0)
    result_items = ToolApiCollectionResult.objects.filter()[0:15]

    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        if app_id != '':
            for item in items:
                if item.pk == int(app_id):
                    compare_api_srv = CompareApiService()
                    result = compare_api_srv.exec_process(item.collection,
                                                          item.environment_source,
                                                          item.environment_destination
                                                          )
                    api_result = ToolApiCollectionResult(
                        diff_data="",
                        diff_analysis=result.get('diff_analysis').to_html(
                            classes="table table-bordered table-hover dataTable table-striped",
                            escape=False
                        ),
                        tool_execute_id=item.pk,
                        uid=compare_api_srv.uid,
                    )
                    api_result.save()

                    for api_name, df_diff in result.get('df_diff').items():
                        api_detail = ToolApiCollectionResultDetail(
                            compare_data=df_diff['compare_result'],
                            diff_data=df_diff['data'].to_html(
                                classes="table table-bordered table-hover dataTable table-striped",
                                escape=False
                            ),
                            uid=compare_api_srv.uid,
                            api_name=api_name,
                            result=df_diff['result'],
                            tool_execute_result_id=api_result.pk,
                        )
                        api_detail.save()
        else:
            sync_message.send_message("<div class='txt-red'>Input validate</div>")

    context = {
        'title': _('Tools'),
        'items': items,
        'result_items': result_items,
    }

    return TemplateResponse(request, template_name, context)


@login_required(login_url="admin:login")
def index_api_detail(request, template_name='tools/index_api_detail.html'):
    uid = request.GET.get('uid')
    api_name = request.GET.get('api_name')
    item = ToolApiCollectionResultDetail.objects.filter(uid=uid, api_name=api_name).first()

    context = {
        'title': _('Tools'),
        'item': item,
    }

    return TemplateResponse(request, template_name, context)


def task(request, task_name, template_name='tools/task.html'):
    return TemplateResponse(request, template_name, {'task_name': task_name})


@login_required(login_url="admin:login")
def compare(request, template_name='tools/compare.html'):
    connections = ToolConnection.objects.filter()[0:15]
    db_conn = DbSchema()
    compare_data = DbCompare()
    created_at = ""
    if request.method == 'POST':
        source_id = request.POST.get('source_id')
        destination_id = request.POST.get('destination_id')
        config_db_s = None
        config_db_d = None
        ssh_config_s = {}
        ssh_config_d = {}
        for connection in connections:
            if source_id == "" or destination_id == "":
                sync_message.send_message("<span class='text-red'>Source and Destination are required.</span>")
                break
            if int(source_id) == connection.id:
                config_db_s = {
                    'host': connection.db_host,
                    'port': int(connection.db_port),
                    'username': connection.db_user,
                    'password': connection.db_password,
                    'db': connection.db_database,
                }
                if connection.ssh_tunnel:
                    ssh_config_s = {
                        'ssh_tunnel': connection.ssh_tunnel,
                        'ssh_host': connection.ssh_host,
                        'ssh_port': int(connection.ssh_port),
                        'ssh_username': connection.ssh_user,
                        'ssh_password': connection.ssh_password,
                        'ssh_rsa': connection.ssh_rsa.path,
                    }

            if int(destination_id) == connection.id:
                config_db_d = {
                    'host': connection.db_host,
                    'username': connection.db_user,
                    'password': connection.db_password,
                    'db': connection.db_database,
                    'port': int(connection.db_port),
                }
                if connection.ssh_tunnel:
                    ssh_config_d = {
                        'ssh_tunnel': connection.ssh_tunnel,
                        'ssh_host': connection.ssh_host,
                        'ssh_port': int(connection.ssh_port),
                        'ssh_username': connection.ssh_user,
                        'ssh_password': connection.ssh_password,
                        'ssh_rsa': connection.ssh_rsa.path,
                    }
        if config_db_s is not None and config_db_d is not None:
            try:
                db_conn.conn_source, db_conn.tunnel_source = db_conn.mysql_connect(config_db_s, ssh_config_s)
            except Exception as e:
                sync_message.send_message(str(e))
                raise Exception

            try:
                db_conn.conn_destination, db_conn.tunnel_destination = db_conn.mysql_connect(config_db_d, ssh_config_d)
            except Exception as e:
                sync_message.send_message(str(e))
                raise Exception
            s_tables = db_conn.get_tables(db_conn.conn_source)
            d_tables = db_conn.get_tables(db_conn.conn_destination)
            compare_result = compare_data.compare('Tables', s_tables, d_tables)

            all_tables = []
            all_tables.extend(s_tables)
            all_tables.extend(d_tables)

            # data_compares = [compare_result]
            sync_message.send_message(''.join(compare_result))
            for table_name in set(all_tables):
                if table_name in s_tables:
                    structure_table_s = db_conn.get_structure_table(db_conn.conn_source, table_name)
                else:
                    structure_table_s = []
                if table_name in d_tables:
                    structure_table_d = db_conn.get_structure_table(db_conn.conn_destination, table_name)
                else:
                    structure_table_d = []

                # print("S", structure_table_s)
                # print("d", structure_table_d)
                compare_result_structure = compare_data.compare(table_name, structure_table_s, structure_table_d)
                # data_compares.append(compare_result_structure)
                created_at = datetime.datetime.now()
                # push data to FE
                sync_message.send_message(''.join(compare_result_structure))

    context = {
        'connections': connections,
        'title': _('Tools'),
        'item': {
            'compare_data': '',
            'created_at': created_at

        },
    }
    return TemplateResponse(request, template_name, context)


def compare_(request, template_name='tools/compare.html'):
    config_db_s = {
        'host': '0.0.0.0',
        'username': 'root',
        'password': 'root',
        'db': 'chinook_track',
        'port': 3306,
    }
    config_db_d = {
        'host': '0.0.0.0',
        'username': 'root',
        'password': 'root',
        'db': 'chinook',
        'port': 3306,
    }
    db_conn = DbSchema()
    compare_data = DbCompare()
    conn_source = db_conn.mysql_connect(config_db_s)
    db_conn.conn_source = conn_source
    conn_destination = db_conn.mysql_connect(config_db_d)
    db_conn.conn_destination = conn_destination
    s_tables = db_conn.get_tables(db_conn.conn_source)
    d_tables = db_conn.get_tables(db_conn.conn_destination)
    compare_result = compare_data.compare('Tables', s_tables, d_tables)

    all_tables = []
    all_tables.extend(s_tables)
    all_tables.extend(d_tables)

    data_compares = [compare_result]
    for table_name in set(all_tables):
        if table_name in s_tables:
            structure_table_s = db_conn.get_structure_table(db_conn.conn_source, table_name)
        else:
            structure_table_s = []
        if table_name in d_tables:
            structure_table_d = db_conn.get_structure_table(db_conn.conn_destination, table_name)
        else:
            structure_table_d = []

        # print("S", structure_table_s)
        # print("d", structure_table_d)
        compare_result_structure = compare_data.compare(table_name, structure_table_s, structure_table_d)
        data_compares.append(compare_result_structure)

    context = {
        'title': _('Tools'),
        'item': {
            'compare_data': ''.join(data_compares),
            'created_at': datetime.datetime.now()

        },
    }

    return TemplateResponse(request, template_name, context)
