from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from datetime import datetime

# MONTHS = [
#     'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июнь', 'Июль', '', '', '', '', '',
# ]

ASSISTANT_SALARIES = [
    96785, 89340, 74450, 74450, 74450,
]

TEACHER_SALARIES = [
    109986, 93065, 84605, 84605, 84605,
]

DOCENT_SALARIES = [
    142130, 121826, 111674, 101522, 101522,
]


class CalculateView(APIView):
    """
    Calculates salary
    """

    def get_user_age_group(self, date_of_birth, temp_date):
        temp_age = temp_date - date_of_birth

        print(temp_age.days)

        if temp_age.days < (365 * 31):
            age_group = 0
        elif (365 * 31) <= temp_age.days < (365 * 35):
            age_group = 1
        elif (365 * 35) <= temp_age.days < (365 * 40):
            age_group = 2
        elif (365 * 40) <= temp_age.days < (365 * 45):
            age_group = 3
        else:
            age_group = 4

        print(age_group)

        return age_group

    def calculate_month_salary(self, user, temp_date):

        academic_degree = user['academic_degree']
        work_experience = user['work_experience']
        date_of_birth = user['date_of_birth']
        date_of_dissertation_defense = user['date_of_dissertation_defense']

        if academic_degree == 'Master':
            rate = 0.5
        elif academic_degree == 'PreСandidate':
            rate = 1
        else:
            rate = -1

        age_i = self.get_user_age_group(date_of_birth, temp_date)

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
            salary = 'ERROR with calculation salary'

        current_month = temp_date.month

        if (current_month == 7 or current_month == 8) and academic_degree == 'Master':
            return 0
        else:
            return int(salary)

    def post(self, request):
        user = {
            'academic_degree': request.data['academic_degree'],
            'academic_degree_course': int(request.data['academic_degree_course']),
            'date_of_registration': datetime.strptime(request.data['date_of_registration'], '%Y-%m-%d'),
            'work_experience': int(request.data['work_experience']),
            'date_of_dissertation_defense': datetime.strptime(request.data['date_of_dissertation_defense'], '%Y-%m-%d'),
            'date_of_birth': datetime.strptime(request.data['date_of_birth'], '%Y-%m-%d'),
        }

        data = list()

        time_to_docent = user['date_of_dissertation_defense'] - datetime.now()
        months = int(time_to_docent.days / 30 + 1)

        current_year = user['date_of_registration'].year
        current_month = user['date_of_registration'].month
        current_day = user['date_of_registration'].day

        if datetime.now() < user['date_of_dissertation_defense']:
            for i in range(months):
                temp_date = datetime.strptime(f'{current_year}-{current_month}-{current_day}', '%Y-%m-%d')
                month_data = {
                    'year': current_year,
                    'month': current_month,
                    'salary': self.calculate_month_salary(user, temp_date)
                }
                data.append(month_data)

                user['work_experience'] += 1

                if current_month == 8 and user['academic_degree'] == 'Master' and user['academic_degree_course'] == 1:
                    user['academic_degree_course'] = 2
                elif current_month == 8 and user['academic_degree'] == 'Master' and user['academic_degree_course'] == 2:
                    user['academic_degree'] = 'PreСandidate'
                    user['academic_degree_course'] = 1

                if current_month == 12:
                    current_month = 1
                    current_year += 1
                else:
                    current_month += 1

        for i in range(3):
            temp_date = datetime.strptime(f'{current_year}-{current_month}-{current_day}', '%Y-%m-%d')
            month_data = {
                'year': current_year,
                'month': current_month,
                'salary': DOCENT_SALARIES[self.get_user_age_group(user['date_of_birth'], temp_date)]
            }
            data.append(month_data)
            if current_month == 12:
                current_month = 1
                current_year += 1
            else:
                current_month += 1

        return Response(data)
