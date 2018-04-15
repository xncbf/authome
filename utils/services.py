import json
import uuid

from django.shortcuts import redirect
from django.urls import reverse


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def new_token(request):
    user = request.user.extendsuser
    user.token = uuid.uuid4()
    user.save()
    return redirect(reverse('main:mypage'))
