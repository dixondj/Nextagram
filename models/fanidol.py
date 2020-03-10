from models.base_model import BaseModel
from models.user import User
import peewee as pw

class FanIdol(BaseModel):
    fan = pw.ForeignKeyField(User, backref='idols',on_delete="CASCADE")
    idol = pw.ForeignKeyField(User, backref='fans',on_delete="CASCADE")
    approved = pw.BooleanField(default=False)
