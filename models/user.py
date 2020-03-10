from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re,os
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property

class User(UserMixin, BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()
    profile_image = pw.TextField(default="Braised+Pork.jpeg")
    private = pw.BooleanField(default=False)

    def follow(self,idol):
        from models.fanidol import FanIdol
        # check if has relationship in database
        if self.follow_status(idol)==None:
            return FanIdol(fan=self.id,idol=idol.id).save()
        else:
            return 0

    def unfollow(self,idol):
        from models.fanidol import FanIdol
        return FanIdol.delete().where(FanIdol.fan==self.id,FanIdol.idol==idol.id).execute()

    def approve_request(self,fan):
        from models.fanidol import FanIdol
        return FanIdol.update(approved=True).where(FanIdol.fan==fan.id,FanIdol.idol==self.id).execute()
   

    def follow_status(self,idol):
        from models.fanidol import FanIdol
        # check following status : 
        # if already follow => return that row, 
        # else return None(mean not follow this idol before)
        return FanIdol.get_or_none(FanIdol.fan==self.id,FanIdol.idol==idol.id)

    @hybrid_property
    def get_request(self):
        from models.fanidol import FanIdol
        return FanIdol.select().where(FanIdol.idol==self.id,FanIdol.approved==False)



    @hybrid_property
    def followers(self):
        from models.fanidol import FanIdol
        # to get all fans
        fans = FanIdol.select(FanIdol.fan).where(FanIdol.idol==self.id,FanIdol.approved==True)
        return User.select().where(User.id.in_(fans))

    @hybrid_property
    def followings(self):
        from models.fanidol import FanIdol
        # to get all idols
        idols = FanIdol.select(FanIdol.idol).where(FanIdol.fan==self.id,FanIdol.approved==True)
        return User.select().where(User.id.in_(idols))


    @hybrid_property
    def profile_url(self):
        return os.getenv("AWS_DOMAIN") + self.profile_image


    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)
        regex_password = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

        if duplicate_username and duplicate_username.id != self.id:
            self.errors.append('Username not unique')
        if duplicate_email and duplicate_email.id != self.id:
            self.errors.append('email not unique')
        if re.search(regex_password,self.password) == None:
            self.errors.append('Password must have minimum eight characters, at least one letter and one number')
        else:
            self.password = generate_password_hash(self.password)


        



