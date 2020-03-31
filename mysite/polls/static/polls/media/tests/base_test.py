# from django.test import TestCase
#
# from django.dispatch import receiver
# from article.models import Article
# from department.models import Department
# from disease.models import Disease
# from django.db.models.signals import post_save, post_delete
# from service.models import Service, Procedure, Program
# from specialist.models import Speciality, Specialist
# from .es_parser import save_instance, delete_instance



_specialities = [
    {
        "name": u"тестовая специальность - хирург",
        "slug": "speciality1",
    },
    {
        "name": u"тестовая специальность - лор",
        "slug": "speciality2",
    }
]

_service_types_api = [
    {
        "Id": 1,
        "ParentId": None,
        "Name": u"Тип услуги 1",
        "DepartmentId": 1,
        "EventTypeId": 1
    },
    {
        "Id": 2,
        "ParentId": None,
        "Name": u"Тип услуги 2",
        "DepartmentId": 2,
        "EventTypeId": 2
    }
]

_service_types = [
    {
        "name": u"Тип услуги 1",
        "slug": "service_type_1",
        "service_type_id_from_api": _service_types_api[0]["Id"]
    },
    {
        "name": u"Тип услуги 2",
        "slug": "service_type_2",
        "service_type_id_from_api":_service_types_api[1]["Id"]
    }
]

_services_api = [
    {
        "Id": 3,
        "ParentId": 1,
        "Name": u"Услуга 1",
        "DepartmentId": 1,
        "EventTypeId": 1
    },
    {
        "Id": 4,
        "ParentId": 2,
        "Name": u"Услуга 2",
        "DepartmentId": 1,
        "EventTypeId": 1
    }
]

_services = [
    {
        "name": u"Услуга 1",
        "slug": "service_1",
        "parent_id": _services_api[0]["ParentId"],
        "service_id_from_api": _services_api[0]["Id"],
    },
    {
        "name": u"Услуга 2",
        "slug": "service_2",
        "parent_id": _services_api[1]["ParentId"],
        "service_id_from_api": _services_api[1]["Id"]
    }
]

_programs_api = [
    {
        "Id": 10,
        "Name": u"Программа 1",
        "Price": 3397.00,
        "ServiceGroupId": 3
    },
    {
        "Id": 11,
        "Name": u"Программа 2",
        "Price": 4320.00,
        "ServiceGroupId": 4
    },
]

_programs = [
    {
        "name": u"Программа 1",
        "slug": "program_1",
        "program_id_from_api": _programs_api[0]["Id"],
        "service_group_id": _programs_api[0]["ServiceGroupId"],
    },
    {
        "name": u"Программа 2",
        "slug": "program_2",
        "program_id_from_api": _programs_api[1]["Id"],
        "service_group_id": _programs_api[1]["ServiceGroupId"],
    }
]

class IndexatorBaseTest(TestCase):
    def setUp(self):
        self.create_clinics()

    def create_clinics(self):
        ''' Тестовые клиники, которые будем специалистам добавлять '''
        ClinicAPI.objects.bulk_create([
            self._create_clinic_api(x) for x in _clinics_api
        ])
        Clinic.objects.bulk_create([
            self._create_clinic(x) for x in _clinics
        ])
        Clinic.objects.filter(slug="clinic1").first().clinics_api.add(
            *[x for x in ClinicAPI.objects.filter(id_from_api__in=[1, 3])]
        )
        Clinic.objects.filter(slug="clinic2").first().clinics_api.add(
            ClinicAPI.objects.filter(id_from_api=2).first()
        )

    '''
        Вспомогательные методы, в самих тестах никак не участвуют
    '''
    # start
    def _create_clinic_api(self, data):
        obj = ClinicAPI(
            id_from_api=data["id_from_api"],
            name=data["name"],
            address=data["address"],
            phone=data["phone"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            url=data["url"],
            support_email=data["support_email"],
            support_work_time=data["support_work_time"],
            is_main_affiliate=data["is_main_affiliate"],
        )
        return obj

    def _create_clinic(self, data):
        obj = Clinic(
            name=data["name"],
            slug=data["slug"]
        )
        return obj
    # /end
