from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from datetime import datetime

ASSISTANT_SALARIES = [
    96785, 89340, 74450, 74450, 74450,
]

TEACHER_SALARIES = [
    109986, 93065, 84605, 84605, 84605,
]

DOCENT_SALARIES = [
    142130, 121826, 111674, 101522, 101522,
]


class DataView(APIView):
    """
    ...
    """

    def calculate_month_salary(self, user):

        academic_degree = user['academic_degree']
        work_experience = user['work_experience']
        date_of_birth = user['date_of_birth']
        date_of_dissertation_defense = user['date_of_dissertation_defense']

        if academic_degree == 'Магистр':
            rate = 0.5
        else:
            rate = 1

        age = datetime.now() - date_of_birth

        if age.days <= (365 * 30):
            age_i = 0
        elif (365 * 30) < age.days <= (365 * 34):
            age_i = 1
        elif (365 * 34) < age.days <= (365 * 39):
            age_i = 2
        elif (365 * 39) < age.days <= (365 * 44):
            age_i = 3
        else:
            age_i = 4

        if datetime.now() < date_of_dissertation_defense:
            is_docent = False
        else:
            is_docent = True

        if work_experience >= 36:
            if is_docent:
                status = 'Docent'
            else:
                status = 'Teacher'
        else:
            status = 'Assistant'

        if status == 'Assistant':
            salary = rate * ASSISTANT_SALARIES[age_i]
        elif status == 'Teacher':
            salary = rate * TEACHER_SALARIES[age_i]
        elif status == 'Docent':
            salary = rate * DOCENT_SALARIES[age_i]
        else:
            print('ERROR')

        return salary

    def post(self, request):
        user = {
            'academic_degree': request.data['academic_degree'],
            'date_of_registration': datetime.strptime(request.data['date_of_registration'], '%Y-%m-%d'),
            'work_experience': int(request.data['work_experience']),
            'date_of_dissertation_defense': datetime.strptime(request.data['date_of_dissertation_defense'], '%Y-%m-%d'),
            'date_of_birth': datetime.strptime(request.data['date_of_birth'], '%Y-%m-%d'),
        }

        data = list()

        for i in range(5):
            month_data = {
                'month': i + 1,
                'salary': self.calculate_month_salary(user)
            }
            data.append(month_data)

            user['work_experience'] += 1

        return Response(data)
