{% extends 'base.html' %}

{% block content %}
    <h1>Query Results</h1>

    <h2>Task 1:</h2>
    <ul>
        {% for department in task1 %}
            <li>{{ department.name }}</li>
        {% endfor %}
    </ul>

    <h2>Task 2:</h2>
    <p>Total active positions: {{ task2 }}</p>

    <h2>Task 3:</h2>
    <ul>
        {% for position in task3 %}
            <li>{{ position.title }} - {{ position.is_active }}</li>
        {% endfor %}
    </ul>

    <h2>Task 4:</h2>
    <ul>
        {% for department in task4 %}
            <li>{{ department.name }}</li>
        {% endfor %}
    </ul>

    <h2>Task 5:</h2>
    <ul>
        {% for position in task5 %}
            <li>{{ position.title }} - {{ position.is_active }}</li>
        {% endfor %}
    </ul>
{% endblock %}
