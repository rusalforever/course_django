from django.db.models import (
    Count,
    Q,
)
from django.shortcuts import render
from hr.models import (
    Department,
    Position,
)

def queryset(request):
    # Запит
    # 1: Знайдіть усі відділи(Department), у яких є позиції менеджерів, та впорядкуйте їх за назвою відділу в алфавітному порядку.
    # Використовуйте filter()і order_by().

    task1 = Department.objects.filter(position__is_manager=True).order_by('name')

    # Запит
    # 2: Знайдіть загальну кількість  активних позицій(Position).Використовуйте filter() та count().

    task2 = Position.objects.filter(is_active=True).count()

    # Запит
    # 3: Виберіть усі позиції, які є активними або які належать до відділу з назвою "HR".Використовуйте
    # filter() і OR( |).

    task3 = Position.objects.filter(Q(is_active=True) | Q(department__name='HR'))

    # Запит
    # 4: Виберіть назви всіх відділів(Department), в яких є менеджери.Використовуйте filter() та values()

    task4 = Department.objects.filter(position__is_manager=True).values('name')

    # Запит
    # 5: Виберіть усі позиції, відсортовані за назвою, але виводьте лише назву та інформацію про активність.
    # Використовуйте order_by() і values().

    task5 = Position.objects.order_by('title').values('title', 'is_active')

    return render(request, 'query_results.html', {
        'task1': task1,
        'task2': task2,
        'task3': task3,
        'task4': task4,
        'task5': task5,
    })
