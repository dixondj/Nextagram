from models.base_model import BaseModel
from models.user import User
import peewee as pw
import os
from playhouse.hybrid import hybrid_property

class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref='images',on_delete="CASCADE")
    image_path = pw.TextField()
    caption = pw.TextField(null=True)

    @hybrid_property
    def image_url(self):
        return os.getenv("AWS_DOMAIN") + self.image_path
