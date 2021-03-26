from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from datetime import datetime
import os
from django.views.generic.base import View
from django.http import HttpResponse
from rest_framework import status

MONTHS = [
    'None', 'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июнь', 'Июль', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек',
]

ASSISTANT_SALARIES = [
    96785, 89340, 74450, 74450, 74450,
]

TEACHER_SALARIES = [
    109986, 93065, 84605, 84605, 84605,
]

TEACHER_K_N_SALARIES = [
    121824, 117312, 99264, 90240, 90240,
]

DOCENT_K_N_SALARIES = [
    142130, 121826, 111674, 101522, 101522,
]


class CalculateView(APIView):
    """
    Calculates salary
    """

    class User:
        def __init__(self, academic_status, academic_course, date_of_registration, work_experience,
                     date_of_dissertation, date_of_birth):
            self.academic_status = academic_status
            self.academic_course = academic_course
            self.date_of_registration = date_of_registration
            self.work_experience = work_experience
            self.date_of_dissertation = date_of_dissertation
            self.date_of_birth = date_of_birth

    def get_user_position(self, user, temp_date):
        if user.work_experience >= 36:
            has_work_experience = True
        else:
            has_work_experience = False

        if temp_date > user.date_of_dissertation:
            has_k_n = True
        else:
            has_k_n = False

        if has_k_n is False and has_work_experience is False:
            return 'Assistant'
        elif has_k_n is False and has_work_experience is True:
            return 'Teacher'
        elif has_k_n is True and has_work_experience is False:
            return 'Teacher_k_n'
        elif has_k_n is True and has_work_experience is True:
            return 'Docent_k_n'
        else:
            return None

    def get_user_age_group(self, temp_date, date_of_birth):
        temp_age = temp_date - date_of_birth
        temp_age_days = temp_age.days - 30  # округление в меньшую

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

        if user.academic_status == 'Specialist' and user.academic_course != 6:
            rate = 0
        elif user.academic_status == 'Specialist' and user.academic_course == 6:
            rate = 1
        elif user.academic_status == 'Bachelor':
            rate = 0
        elif user.academic_status == 'Master' and user.academic_course != 6:
            rate = 0.5
        elif user.academic_status == 'Master' and user.academic_course == 6:
            rate = 1
        elif user.academic_status == 'PreCandidate':
            rate = 1
        elif user.academic_status == 'Graduate':
            rate = 1
        else:
            rate = -1

        age_group = self.get_user_age_group(temp_date, user.date_of_birth)

        if user.work_experience >= 36:
            has_work_experience = True
        else:
            has_work_experience = False

        if temp_date > user.date_of_dissertation:
            has_k_n = True
        else:
            has_k_n = False

        if has_k_n is False and has_work_experience is False:
            position = 'Assistant'
        elif has_k_n is False and has_work_experience is True:
            position = 'Teacher'
        elif has_k_n is True and has_work_experience is False:
            position = 'Teacher_k_n'
        elif has_k_n is True and has_work_experience is True:
            position = 'Docent_k_n'
        else:
            position = None

        if position == 'Assistant':
            salary = rate * ASSISTANT_SALARIES[age_group]
        elif position == 'Teacher':
            salary = rate * TEACHER_SALARIES[age_group]
        elif position == 'Teacher_k_n':
            salary = rate * TEACHER_K_N_SALARIES[age_group]
        elif position == 'Docent_k_n':
            salary = rate * DOCENT_K_N_SALARIES[age_group]
        else:
            salary = None

        if (temp_date.month == 7 or temp_date.month == 8) and user.academic_status == 'Master':
            if user.academic_course != 6:
                return 0
            else:
                return int(salary)
        else:
            return int(salary)

    def post(self, request):
        try:

            user = self.User(
                academic_status=request.data['academic_status'],
                academic_course=int(request.data['academic_course']),
                date_of_registration=datetime.strptime(request.data['date_of_registration'], '%Y-%m-%d'),
                work_experience=int(request.data['work_experience']),
                date_of_dissertation=datetime.strptime(request.data['date_of_dissertation'], '%Y-%m-%d'),
                date_of_birth=datetime.strptime(request.data['date_of_birth'], '%Y-%m-%d')
            )

            flag_of_registration = False
            flag_of_work_experience = False
            flag_of_dissertation = False

            flag_of_position_assistant = False
            flag_of_position_teacher = False
            flag_of_position_teacher_k_n = False
            flag_of_position_docent_k_n = False

            flag_of_master = True
            if user.academic_status == 'Bachelor' or user.academic_status == 'Master' and user.academic_course == 0:
                flag_of_master = False

            flag_of_aspirant = True
            if not (user.academic_status == 'PreCandidate' and user.academic_course > 0):
                flag_of_aspirant = False

            if user.academic_status == 'Bachelor' and user.academic_course == 6:
                user.academic_status = 'Master'
                user.academic_course = 0
            elif user.academic_status == 'Master' and user.academic_course == 6:
                # user.academic_status = 'Master'
                # user.academic_course = 2
                pass
            elif user.academic_status == 'Specialist' and user.academic_course == 6:
                # user.academic_status = 'Specialist'
                # user.academic_course = 5
                # user.academic_status = 'PreCandidate'
                # user.academic_course = 1
                pass
            elif user.academic_status == 'PreCandidate' and user.academic_course == 6:
                user.academic_course = None

            '''
            1) вычислим статус на момент регистрации
            2) вычислим карьеру с момента регистрации
            '''

            data = list()
            prev_events = []
            month_data = {
                'academic_status': None,
                'academic_course': None,
                'date': None,
                'salary': None,
                'status_of_work_experience': None,
                'status_of_age_group': None,
                'status_of_dissertation': None,
                'events': None,
                'vacation_salary': None
            }

            user_dissertation_age = user.date_of_dissertation - user.date_of_birth
            plus_time = int(33 - user_dissertation_age.days / 365 + 1)

            all_time = user.date_of_dissertation - datetime.now()  # user.date_of_dissertation must be > datetime.now()
            if plus_time > 0:
                all_time = int(all_time.days / 30 + 1 + 12 + plus_time * 12)
            else:
                all_time = int(all_time.days / 30 + 1 + 12)

            current_year = datetime.now().year
            current_month = datetime.now().month
            current_day = datetime.now().day

            for i in range(all_time):
                temp_date = datetime.strptime(f'{current_year}-{current_month}-{current_day}', '%Y-%m-%d')

                if temp_date < user.date_of_registration:
                    print(f'(b){temp_date.year} {temp_date.month}\t{user.academic_course} {user.academic_status}')
                else:
                    print(f'{temp_date.year} {temp_date.month}\t{user.academic_course} {user.academic_status}',
                          end='\t')

                if temp_date > user.date_of_registration:

                    events = []
                    events += prev_events
                    prev_events = []

                    # print(self.get_user_position(user, temp_date))
                    if user.academic_status != 'Bachelor' and user.academic_status != 'Specialist' \
                            or user.academic_status == 'Specialist' and user.academic_course == 6:
                        if flag_of_registration is False:
                            events.append('Оформление на должность ППС')
                            flag_of_registration = True

                        if user.work_experience == 36 and flag_of_work_experience is False:
                            events.append('3 года работы преподавателем')
                            flag_of_work_experience = True

                        if temp_date > user.date_of_dissertation and flag_of_dissertation is False:
                            events.append('Защищена диссертация')
                            flag_of_dissertation = True

                        if not flag_of_master:
                            events.append('Поступление в магистратуру')
                            flag_of_master = True

                        if not flag_of_aspirant and user.academic_status == 'PreCandidate':
                            events.append('Поступление в аспирантуру')
                            flag_of_aspirant = True

                        # if month_data['academic_status'] != user.academic_status and \
                        #         user.academic_status == 'Master' and \
                        #         user.academic_course is not None:
                        #         # user.academic_course == 1:
                        #     events.append('Поступление в магистратуру')

                        # if month_data[
                        #     'academic_status'] != user.academic_status and \
                        #         user.academic_status == 'PreCandidate' and \
                        #         user.academic_course is not None:
                        #     events.append('Поступление в аспирантуру')

                        if month_data['status_of_age_group'] != self.get_user_age_group(temp_date,
                                                                                        user.date_of_birth) \
                                and month_data['status_of_age_group'] is not None:
                            events.append('Переход в следующую возрастную группу')

                        if flag_of_position_assistant is False and self.get_user_position(user,
                                                                                          temp_date) == 'Assistant':
                            events.append('Должность Ассистента')
                            flag_of_position_assistant = True
                        if flag_of_position_teacher is False and self.get_user_position(user,
                                                                                        temp_date) == 'Teacher':
                            events.append('Должность Старшего преподавателя')
                            flag_of_position_teacher = True
                        if flag_of_position_teacher_k_n is False and self.get_user_position(user,
                                                                                            temp_date) == 'Teacher_k_n':
                            events.append('Должность Старшего Преподавателя с уч. степенью к.н.')
                            flag_of_position_teacher_k_n = True
                        if flag_of_position_docent_k_n is False and self.get_user_position(user,
                                                                                           temp_date) == 'Docent_k_n':
                            events.append('Должность Доцента с уч. степенью к.н.')
                            flag_of_position_docent_k_n = True

                    vacation_status = (temp_date.month == 7 or temp_date.month == 8) \
                                      and user.academic_status == 'Master' \
                                      and user.academic_course != 6
                    month_data = {
                        'academic_status': user.academic_status,
                        'academic_course': user.academic_course,
                        'date': f' {MONTHS[current_month]} {current_year}',
                        'salary': self.calculate_month_salary(user, temp_date),
                        'status_of_work_experience': user.work_experience >= 36,
                        'status_of_age_group': self.get_user_age_group(temp_date, user.date_of_birth),
                        'status_of_dissertation': temp_date > user.date_of_dissertation,
                        'vacation_status': vacation_status,
                        'events': events,
                        'vacation_salary': None
                    }

                    data.append({
                        'academic_status': month_data['academic_status'],
                        'academic_course': month_data['academic_course'],
                        'date': month_data['date'],
                        'salary': month_data['salary'],
                        'events': month_data['events'],
                        'vacation_status': month_data['vacation_status'],
                        'vacation_salary': month_data['vacation_salary'],
                    })

                    print(month_data['status_of_work_experience'], month_data['status_of_age_group'],
                          month_data['status_of_dissertation'], month_data['vacation_status'], month_data['salary'],
                          self.get_user_position(user, temp_date), month_data['events'])
                    if (current_month == 7 or current_month == 8) and user.academic_status == 'Master':
                        pass
                    else:
                        if user.academic_status != 'Specialist' or user.work_experience != 'Bachelor':
                            user.work_experience += 1

                if current_month == 8:

                    if user.academic_status == 'Bachelor':
                        if user.academic_course != 4:
                            user.academic_course += 1
                        elif user.academic_course == 4:
                            user.academic_status = 'Master'
                            user.academic_course = 0

                    if user.academic_status == 'Master':
                        if user.academic_course != 2 and user.academic_course != 6:
                            user.academic_course += 1
                        elif user.academic_course == 2:
                            user.academic_status = 'PreCandidate'
                            user.academic_course = 0
                        elif user.academic_course == 6:
                            user.academic_status = 'PreCandidate'
                            user.academic_course = 0

                    if user.academic_status == 'Specialist':
                        if user.academic_course != 5 and user.academic_course != 6:
                            user.academic_course += 1
                        elif user.academic_course == 5:
                            user.academic_status = 'PreCandidate'
                            user.academic_course = 0
                        elif user.academic_course == 6:
                            user.academic_status = 'PreCandidate'
                            user.academic_course = 0

                    if user.academic_status == 'PreCandidate':
                        if user.academic_course != 4 and user.academic_course is not None:
                            user.academic_course += 1
                        elif user.academic_course == 4:
                            user.academic_status = 'Graduate'
                            user.academic_course = None

                if current_month == 12:
                    current_month = 1
                    current_year += 1
                else:
                    current_month += 1

            # all_time = user['date_of_dissertation_defense'] - datetime.now()
            # all_time = int(all_time.days / 30 + 1)
            # print(all_time)
            #
            # for i in range(all_time):
            #     pass

            print('------------------------')

            # qwe = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            # qwe.reverse()

            # print(qwe[0:10])

            print(len(data))

            temp_delay = 0
            temp_events = data[0]['events']

            for i in range(len(data) - 1):

                if data[i]['academic_course'] == 0:
                    temp_delay += 1

                if data[i]['vacation_status'] is True and data[i]['academic_course'] != 0:
                    print('academic_course != 0')
                    # print(i, end='\t')
                    temp_data = data[0 + temp_delay:i]

                    pop_list = []
                    for j in range(len(temp_data) - 1):
                        # print(-j - 1, end=' ')
                        if temp_data[-j - 1]['vacation_status'] is True:
                            pop_list.append(-j - 1)

                    for pop_el in pop_list:
                        temp_data.pop(pop_el)

                    # print('\n')
                    if len(temp_data) > 10:
                        temp_data.reverse()
                        temp_data = temp_data[0:10]

                    temp_sum = 0
                    for el in temp_data:
                        temp_sum += el['salary']
                    temp_salary = int(temp_sum / len(temp_data))
                    # print(temp_salary)
                    data[i]['vacation_salary'] = temp_salary

            data = data[temp_delay:len(data)]

            data[0]['events'] = temp_events

            # flag_of_first_vacation = False
            # for i in range(len(data)):
            #     if data[i]['salary'] == 0:
            #         temp_data = data[0:i - 1]
            #         for el in temp_data:
            #             if el['salary'] == 0:
            #                 temp_data.remove(el)
            #         temp_sum = 0
            #         for el in temp_data:
            #             temp_sum += el['salary']
            #         temp_salary = int(temp_sum / len(temp_data))
            #         print(temp_salary)
            return Response(data)
        except:
            return Response({"error_message": "BAD REQUEST", "status": status.HTTP_400_BAD_REQUEST})
