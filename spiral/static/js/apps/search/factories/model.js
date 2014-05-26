angular.module('searchApp').factory('ModelFactory', function () {
    var factory = {};

    factory.getBasicData = function() {
        var data =  [
            {
                'codigo': '000001',
                'nombres':'Jonathan Percy',
                'apellidos': 'Carrasco Garcia',
                'edad': 23,
                'Telefonos': '99658133'
            },
            {
                'codigo': '000002',
                'nombres':'Juan Perez',
                'apellidos': 'Garivaldo Olortega',
                'edad': 59,
                'Telefonos': '98745214'
            },
            {
                'codigo': '000003',
                'nombres':'Carla Estefany',
                'apellidos': 'Garcia Mnedez',
                'edad': 20,
                'Telefonos': '87451124'
            },
            {
                'codigo': '000004',
                'nombres':'Joshimar',
                'apellidos': 'Yotun',
                'edad': 15,
                'Telefonos': '96547841- 12488211'
            },
            {
                'codigo': '000005',
                'nombres':'Maria',
                'apellidos': 'Mercedez',
                'edad': 23,
                'Telefonos': '965748125 - 4478122'
            },
            {
                'codigo': '000006',
                'nombres':'Jose Luis',
                'apellidos': 'Cahuana',
                'edad': 10,
                'Telefonos': '98752145 -9874561'
            },
            {
                'codigo': '000007',
                'nombres':'Gustavo',
                'apellidos': 'Vidal',
                'edad': 50,
                'Telefonos': '9874572 -7742214'
            },
            {
                'codigo': '000008',
                'nombres':'Carmen',
                'apellidos': 'Vidal',
                'edad': 40,
                'Telefonos': '987548522- 5471244'
            },
            {
                'codigo': '000009',
                'nombres':'Raquel Sandra',
                'apellidos': 'Vidal',
                'edad': 23,
                'Telefonos': '98745842 - 44125'
            },
            {
                'codigo': '000010',
                'nombres':'MIchelin',
                'apellidos': 'Matalozano',
                'edad': 12,
                'Telefonos': '9854751247 - 741254'
            }


        ];
        return data;
    };

    factory.getAdvanceData = function() {
        var data =  [
            {
                'codigo': '000001',
                'nombres':'Jon Percy',
                'apellidos': 'Carrasco Garcia',
                'edad': 23,
                'Telefonos': '99658133',
                'carracteristicas':
                    {
                        'genero':'hombre',
                        'profesion': 'ingeniero',
                        'cabello':'negro',
                        'estatura':'media'
                    }

            },
            {
                'codigo': '000002',
                'nombres':'Juan Perez',
                'apellidos': 'Garivaldo Olortega',
                'edad': 59,
                'Telefonos': '98745214',
                'carracteristicas':
                    {
                        'genero':'hombre',
                        'profesion': 'actor profesional',
                        'cabello':'negro',
                        'estatura':'alta'
                    }

            },
            {
                'codigo': '000003',
                'nombres':'Carla Estefany',
                'apellidos': 'Garcia Mnedez',
                'edad': 20,
                'Telefonos': '87451124',
                'carracteristicas':
                    {
                        'genero':'mujer',
                        'profesion': 'actriz',
                        'cabello':'rubio',
                        'estatura':'media'
                    }

            },
            {
                'codigo': '000004',
                'nombres':'Joshimar',
                'apellidos': 'Yotun',
                'edad': 15,
                'Telefonos': '96547841- 12488211',
                'carracteristicas':
                    {
                        'genero':'hombre',
                        'profesion': 'Comediante',
                        'cabello':'negro',
                        'estatura':'media'
                    }

            },
            {
                'codigo': '000005',
                'nombres':'Maria',
                'apellidos': 'Mercedez',
                'edad': 23,
                'Telefonos': '965748125 - 4478122',
                'carracteristicas':
                    {
                        'genero':'mujer',
                        'profesion': 'Anfitriona',
                        'cabello':'negro',
                        'estatura':'alta'
                    }

            },
            {
                'codigo': '000006',
                'nombres':'Jose Luis',
                'apellidos': 'Cahuana',
                'edad': 10,
                'Telefonos': '98752145 -9874561',
                'carracteristicas':
                    {
                        'genero':'niño',
                        'profesion': 'ninguna',
                        'cabello':'negro',
                        'estatura':'bajo'
                    }

            },
            {
                'codigo': '000007',
                'nombres':'Gustavo',
                'apellidos': 'Vidal',
                'edad': 50,
                'Telefonos': '9874572 -7742214',
                'carracteristicas':
                    {
                        'genero':'hombre',
                        'profesion': 'abogado',
                        'cabello':'negro',
                        'estatura':'alta'
                    }

            },
            {
                'codigo': '000008',
                'nombres':'Carmen',
                'apellidos': 'Vidal',
                'edad': 40,
                'Telefonos': '987548522- 5471244',
                'carracteristicas':
                    {
                        'genero':'mujer',
                        'profesion': 'Administradora',
                        'cabello':'negro',
                        'estatura':'medio'
                    }

            },
            {
                'codigo': '000009',
                'nombres':'Raquel Sandra',
                'apellidos': 'Vidal',
                'edad': 23,
                'Telefonos': '98745842 - 44125',
                'carracteristicas':
                    {
                        'genero':'femenino',
                        'profesion': 'Actriz',
                        'cabello':'negro',
                        'estatura':'alta'
                    }
            },
            {
                'codigo': '000010',
                'nombres':'MIchelin',
                'apellidos': 'Matalozano',
                'edad': 12,
                'Telefonos': '9854751247 - 741254',
                'carracteristicas':
                    {
                        'genero':'hombre',
                        'profesion': 'ingeniero',
                        'cabello':'negro',
                        'estatura':'bajo'
                    }

            }


        ];
        return data;
    };

    return factory;
});