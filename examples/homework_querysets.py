from django.http import JsonResponse
from django.db.models import (
    Q,
)
from hr.models import (
    Department,
    Position,
)


def homework_querysets(request):
    # Запит 1: Знайдіть усі відділи (Department), у яких є позиції менеджерів, та впорядкуйте їх за назвою відділу в
    # алфавітному порядку. Використовуйте filter() і order_by().
    query_1 = Department.objects.filter(position__is_manager=True).order_by('name')

    # Запит 2: Знайдіть загальну кількість активних позицій (Position). Використовуйте filter() та count().
    query_2 = Position.objects.filter(is_active=True).count()

    # Запит 3: Виберіть усі позиції, які є активними або які належать до відділу з назвою "HR".
    # Використовуйте filter() і OR (|).
    query_3 = Position.objects.filter(Q(is_active=True) | Q(department__name="HR"))

    # Запит 4: Виберіть назви всіх відділів (Department), в яких є менеджери. Використовуйте filter() та values().
    query_4 = Department.objects.filter(position__is_manager=True).values('name')

    # Запит 5: Виберіть усі позиції, відсортовані за назвою, але виводьте лише назву та інформацію про активність.
    # Використовуйте order_by() і values().
    query_5 = Position.objects.order_by('title').values('title', 'is_active')

    response_data = {
        'departments_with_managers': list(query_1.values()),
        'total_active_positions': query_2,
        'active_positions_hr': list(query_3.values()),
        'departments_with_managers_names': list(query_4),
        'positions_sorted': list(query_5),
    }

    return JsonResponse(response_data)

