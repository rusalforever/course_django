from enum import Enum


class WorkDayEnum(str, Enum):
    WORKING_DAY = 'Working Day'
    SICK_DAY = 'Sick Day'
    HOLIDAY = 'Holiday'
    WEEKEND = 'Weekend'
    UNPAID_DAY = 'Unpaid day'
