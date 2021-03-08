from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from datetime import datetime
import os
from django.views.generic.base import View
from django.http import HttpResponse

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

        temp_age_days = temp_age.days - 30

        if temp_age_days < (365 * 31):
            age_group = 0
        elif (365 * 31) <= temp_age_days < (365 * 35):
            age_group = 1
        elif (365 * 35) <= temp_age_days < (365 * 40):
            age_group = 2
        elif (365 * 40) <= temp_age_days < (365 * 45):
            age_group = 3
        else:
            age_group = 4

        return age_group

    def calculate_month_salary(self, user, temp_date):

        academic_degree = user['academic_degree']
        work_experience = user['work_experience']
        date_of_birth = user['date_of_birth']
        date_of_dissertation_defense = user['date_of_dissertation_defense']

        if academic_degree == 'Specialist':
            rate = 0
        elif academic_degree == 'Master':
            rate = 0.5
        elif academic_degree == 'PreCandidate':
            rate = 1
        elif academic_degree == 'Docent':
            rate = 1
        else:
            rate = -1

        age_i = self.get_user_age_group(date_of_birth, temp_date)

        if temp_date < date_of_dissertation_defense:
            has_k_n = False
        else:
            has_k_n = True

        if work_experience >= 36:
            if has_k_n:
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
                    'academic_degree': user['academic_degree'],
                    'academic_degree_course': user['academic_degree_course'],
                    'year': current_year,
                    'month': current_month,
                    'salary': self.calculate_month_salary(user, temp_date)
                }
                data.append(month_data)
                print(
                    f"{current_month}.{current_year}: \t{user['academic_degree']} {user['academic_degree_course']}\t{month_data['salary']}")

                if (current_month == 7 or current_month == 8) and user['academic_degree'] == 'Master':
                    pass
                else:
                    user['work_experience'] += 1

                if current_month == 8 \
                        and user['academic_degree'] == 'Master' \
                        and user['academic_degree_course'] == 1:
                    user['academic_degree_course'] = 2
                elif current_month == 8 \
                        and user['academic_degree'] == 'Master' \
                        and user['academic_degree_course'] == 2:
                    user['academic_degree'] = 'PreCandidate'
                    user['academic_degree_course'] = 0

                if current_month == 8 \
                        and user['academic_degree'] == 'Specialist' \
                        and user['academic_degree_course'] != 5:
                    user['academic_degree_course'] += 1
                elif current_month == 8 \
                        and user['academic_degree'] == 'Specialist' \
                        and user['academic_degree_course'] == 5:
                    user['academic_degree'] = 'PreCandidate'
                    user['academic_degree_course'] = 0

                if current_month == 8 \
                        and user['academic_degree'] == 'PreCandidate' \
                        and user['academic_degree_course'] != 4:
                    user['academic_degree_course'] += 1
                elif current_month == 8 \
                        and user['academic_degree'] == 'PreCandidate' \
                        and user['academic_degree_course'] == 4:
                    user['academic_degree'] = 'Docent'

                if current_month == 12:
                    current_month = 1
                    current_year += 1
                else:
                    current_month += 1

        # years_gone = current_year - user['date_of_birth'].year
        # years_required = 33 - years_gone
        # print('docent')
        # for i in range(years_required * 12):
        #     temp_date = datetime.strptime(f'{current_year}-{current_month}-{current_day}', '%Y-%m-%d')
        #     month_data = {
        #         'academic_degree': user['academic_degree'],
        #         'academic_degree_course': user['academic_degree_course'],
        #         'year': current_year,
        #         'month': current_month,
        #         # 'salary': self.calculate_month_salary(user, temp_date)
        #         'salary': DOCENT_SALARIES[self.get_user_age_group(user['date_of_birth'], temp_date)]
        #     }
        #     data.append(month_data)
        #     print(
        #         f"{current_month}.{current_year}: \t{user['academic_degree']} {user['academic_degree_course']}\t{month_data['salary']}")
        #     if current_month == 12:
        #         current_month = 1
        #         current_year += 1
        #     else:
        #         current_month += 1

        end_data = list()
        for el in data:
            if el['academic_degree'] != 'Specialist':
                end_data.append(el)

        # temp_sum = 0
        # temp_months = 0
        # for el in data:
        #     temp_sum += el['salary']
        #     temp_months += 1
        #     print('Worked ', temp_months, ' months (', int(temp_months/12), 'years)\t Got ', temp_sum)

        return Response(end_data)


class ReactAppView(View):

    def get(self, request):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        try:
            with open(os.path.join(BASE_DIR, 'frontend', 'build', 'index.html')) as file:
                return HttpResponse(file.read())

        except:
            return HttpResponse(
                """
                File index.html not found ! Build your React app !
                """,
                status=501,
            )
