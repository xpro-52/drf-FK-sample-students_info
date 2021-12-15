"""
Simple Test
"""

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from .models import Student, Department


class DepartmentTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(3):
            Department.objects.create(name='test'+str(i))

    def setUp(self) -> None:
        self.api_client = APIClient()

    def test_list(self):
        resp = self.api_client.get('/departments/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        departments = Department.objects.all()
        for i in range(departments.count()):
            with self.subTest(i=i):
                self.assertEqual(resp.data[i]['name'], departments[i].name)

    def test_detail(self):
        departments = Department.objects.all()
        for i in range(3):
            resp = self.api_client.get(f'/departments/{i+1}/')
            with self.subTest(i=i):
                self.assertEqual(resp.status_code, status.HTTP_200_OK)
                self.assertEqual(resp.data['name'], departments[i].name)

    def test_create(self):
        resp = self.api_client.post(f'/departments/', data={'name':'test'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['name'], Department.objects.last().name)
        

class StudentTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(3):
            Department.objects.create(name='test'+str(i))
            Student.objects.create(first_name='firsttest'+str(i), 
                                   last_name='lasttest'+str(i),
                                   department=Department.objects.get(id=i+1))
    def setUp(self) -> None:
        self.api_client = APIClient()

    def test_list(self):
        resp = self.api_client.get('/students/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        students = Student.objects.all()
        for i in range(students.count()):
            with self.subTest(i=i):
                self.assertEqual(resp.data[i]['first_name'], students[i].first_name)

    def test_detail(self):
        students = Student.objects.all()
        for i in range(students.count()):
            resp = self.api_client.get(f'/students/{i+1}/')
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            with self.subTest(i=i):
                self.assertEqual(resp.data['first_name'], students[i].first_name)

    def test_create(self):
        resp = self.api_client.post(f'/students/', 
                                    data={'first_name':'firsttest', 
                                          'last_name': 'lasttest',
                                          'department': '/departments/1/'},
                                    format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        student = Student.objects.last()
        self.assertEqual(resp.data['first_name'], student.first_name)

