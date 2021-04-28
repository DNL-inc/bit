import enum

from tortoise import fields
from tortoise.models import Model

# from middlewares import _

class Day(enum.Enum):
    # monday = _('Понедельник')
    # tuesday = _('Вторник')
    # wednesday = _('Среда')
    # thursday = _('Четверг')
    # friday = _('Пятница')
    # saturday = _('Суббота')
    # sunday = _('Воскресенье')

    monday = 'monday'
    tuesday = 'tuesday'
    wednesday = 'wednesday'
    thursday = 'thursday'
    friday = 'friday'
    saturday = 'saturday'
    sunday = 'sunday'

class Event(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(255)
    link = fields.CharField(255)
    type = fields.CharField(255)
    event_over = fields.DateField(null=True)
    time = fields.DatetimeField(null=True)
    group = fields.ForeignKeyField('models.Group', on_delete="CASCADE")
    subgroup = fields.ForeignKeyField('models.Subgroup', on_delete="CASCADE", null=True)
    day = fields.CharEnumField(Day, null=True)

    def __repr__(self):
        return str(self.id)
