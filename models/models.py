from extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255),nullable=False,unique=True)
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(),nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(),nullable=False, server_default=db.func.now(),onupdate=db.func.now())

    @property
    def data(self):
        return{
            'id':self.id,
            'email':self.email,
            'password':self.password
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        r = cls.query.all()
        result = []

        for i in r:
            result.append(i.data)
        return result
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def get_by_email_password(cls, email,password):
        return cls.query.filter(cls.email == email, cls.password == password).first()


# housekeeper Table
class Housekeeper(db.Model):
    __tablename__ = 'housekeeper'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255),nullable=False,unique=True)
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(),nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(),nullable=False, server_default=db.func.now(),onupdate=db.func.now())

    @property
    def data(self):
        return{
            'id':self.id,
            'email':self.email,
            'password':self.password
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        r = cls.query.all()
        result = []

        for i in r:
            result.append(i.data)
        return result
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def get_by_email_password(cls, email,password):
        return cls.query.filter(cls.email == email, cls.password == password).first()

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True, default='admin@example.com')
    password = db.Column(db.String(255), nullable=False, default='123')
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def data(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        r = cls.query.all()
        result = []

        for i in r:
            result.append(i.data)
        return result
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def get_by_email_password(cls, email, password):
        return cls.query.filter(cls.email == email, cls.password == password).first()

# orders tables
# class Orders(db.Model):
#     __tablename__ = 'orders'

#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer,nullable=False)
#     item_id = db.Column(db.Integer,nullable=False)
#     user_id = db.Column(db.Integer,nullable=False)
#     quantity = db.Column(db.Integer,nullable=False)
#     total_price = db.Column(db.String(255),nullable=False)
#     created_at = db.Column(db.DateTime(),nullable=False, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime(),nullable=False, server_default=db.func.now(),onupdate=db.func.now())

#     def __init__(self,order_id,item_id,user_id,quantity,total_price):
#         self.order_id = order_id
#         self.item_id = item_id
#         self.user_id = user_id
#         self.quantity = quantity
#         self.total_price = total_price
    
#     def __repr__(self):
#          return{
#             'order_id':self.order_id,
#             'item_id':self.item_id,
#             'user_id':self.user_id,
#             'quantity':self.quantity,
#             'total_price':self.total_price,
#         }