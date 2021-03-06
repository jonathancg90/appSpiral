# -*- encoding: utf-8 -*-
from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from apps.sp.models.Client import Client, TypeClient


class ClientHelper(InsertHelperMixin):
    entity = Client

    def set_data(self):
        self.objects_to_insert = [
            {
                "name": 'Productora',
                "ruc": '1234567891',
                "address": 'Direccion de la productora'
            },
            {
                "name": 'Agencia',
                "ruc": '1231231231',
                "address": 'Productora',
            },
            {
                "name": 'Realizadora',
                "ruc": '3213213213',
                "address": 'Productora'
            }
        ]

    def insert_type(self):
        client_productor = Client.objects.get(name='Productora')
        client_productor.type_client.add(TypeClient.objects.get(name='Productora'))

        client_agency = Client.objects.get(name='Agencia')
        client_agency.type_client.add(TypeClient.objects.get(name='Agencia'))

        client_director = Client.objects.get(name='Realizadora')
        client_director.type_client.add(TypeClient.objects.get(name='Realizadora'))