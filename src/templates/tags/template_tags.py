from dateutil import parser
from datetime import datetime
from django import template
from django.utils.http import urlencode
import json
from ast import literal_eval

register = template.Library()


@register.filter(is_safe=True)
def get_date(date_text):
    try:
        if type(date_text) is datetime:
            return date_text
        else:
            date_text = parser.parse(date_text, ignoretz=True)
        return date_text.strftime('%d-%m-%Y %H:%M:%S')
    except ValueError:
        return date_text.strftime('%d-%m-%Y %H:%M:%S')


@register.simple_tag
def url_replace1(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.filter(name='private')
def private(obj, attribute):
    if obj is not None:
        if attribute in obj:
            return obj.get(attribute, 0)
    return 0
    # return getattr(obj, attribute)


@register.filter
def pretty_json(value):
    return json.dumps(value, indent=4, default=str)


@register.filter(name='jsonify')
def jsonify(data):
    return literal_eval(data)
