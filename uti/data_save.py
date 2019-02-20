# -*- coding: utf-8 -*
from Data.models import ServerDict


def db_save(serverName, topclass, type, first, second, third, data=''):

    server_name = 'https://guizhou.csb/' + first + '/' + second + '/' + type + '/' + third + '/' + 'xxx'
    if data == '':
        data_name = 'https://guizhou.csb/' + first + '/' + second + '/' + type + '/' + third + '/' + 'xxx'
    else:
        data_name = 'https://guizhou.csb/' + first + '/' + second + '/' + type + '/' + third + '/' + 'xxx?' + type + '=' + data
    obj = ServerDict.objects.create(id=None,
                                    name=serverName,
                                    top_class=topclass,
                                    type=type,
                                    server_name=server_name,
                                    data_name=data_name,
                                    is_delete=0)
    obj.save()
    return True
