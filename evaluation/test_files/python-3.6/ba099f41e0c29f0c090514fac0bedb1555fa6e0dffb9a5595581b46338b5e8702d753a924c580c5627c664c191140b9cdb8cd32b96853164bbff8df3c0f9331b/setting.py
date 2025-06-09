from paddlelabel.api.model import TaskCategory
from .base import BaseSchema

class TaskCategorySchema(BaseSchema):

    class Meta(BaseSchema.Meta):
        model = TaskCategory