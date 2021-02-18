from tortoise import fields
from tortoise.models import Model


class Faculty(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(255)

    class Mеta:
        table = 'faculties'

    async def select_all_faculties(self):
        faculties = await Faculty.all()
        return faculties
