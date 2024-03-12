import threading
import xmlrpc.client

from django.contrib import messages
from loguru import logger
from odoo_auth import backends, settings
from odoo_auth.models import OdooUser


class OdooBackend(backends.OdooBackend):
    def authenticate(self, request, username: str | None = None, password: str | None = None):
        user = super().authenticate(request, username, password)

        if not user or user.first_name:
            return user

        odoo_user = OdooUser.objects.filter(user=user).first()
        if not odoo_user:
            return user

        url = settings.ODOO_SERVER_URL
        if settings.ODOO_SERVER_PORT is not None:
            url += f':{settings.ODOO_SERVER_PORT}'
        url = f'{url}/xmlrpc/2/object'

        group, name = get_group_and_name(url, odoo_user.odoo_id, password, username)

        if full_name := name:
            name = full_name.split(' ')
            user.last_name = name[0]
            user.first_name = ' '.join(name[1:])

        if group := group:
            user.group = group

        # Костыль, чтоб определять является ли пользователь сотрудником
        user.is_staff = not username.isdigit() and not group

        user.save()
        messages.add_message(
            request,
            messages.WARNING,
            'Вы только что зарегестрировались. Пожалуйста, проверьте правильность своих данных и подключите telegram',
        )

        return user


def get_group_and_name(url: str, odoo_id: int, password: str, username: str) -> tuple[str | None, str | None]:
    name_result = []
    group_result = []
    thread_group = threading.Thread(target=get_group, args=(url, odoo_id, password, group_result))
    thread_name = threading.Thread(target=get_name, args=(url, odoo_id, password, username, name_result))
    thread_group.start()
    thread_name.start()
    thread_group.join()
    thread_name.join()
    return group_result[0], name_result[0]


def get_group(url: str, odoo_id: int, password: str, result: list):
    try:
        models = xmlrpc.client.ServerProxy(url)
        data = models.execute_kw(
            'portfolio',
            odoo_id,
            password,
            'portfolio_science.grade_view',
            'search_read',
            [[['ID_student', '!=', '']]],
            {'fields': ['group'], 'order': 'id desc', 'limit': 1},
        )
        result.append(data[0]['group'])
        return
    except Exception as e:
        logger.error(e)
        result.append(None)
        return


def get_name(url: str, odoo_id: int, password: str, username: str, result: list) -> str | None:
    try:
        models = xmlrpc.client.ServerProxy(url)
        data = models.execute_kw(
            'portfolio',
            odoo_id,
            password,
            'res.users',
            'search_read',
            [[['login', '=', username]]],
            {
                'limit': 1,
                'order': 'id desc',
                'fields': ['name'],
            },
        )
        result.append(data[0]['name'])
        return
    except Exception as e:
        logger.error(e)
        result.append(None)
        return
