from modeltranslation.translator import TranslationOptions, register

from hr.models import Position


@register(Position)
class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')
