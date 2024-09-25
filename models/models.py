from extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255),nullable=False,unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(),nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(),nullable=False, server_default=db.func.now(),onupdate=db.func.now())

    @property
    def data(self):
        return{
            'id':self.id,
            'email':self.email,
            'name':self.name,
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
    name = db.Column(db.String(255))
    priceperhour = db.Column(db.String(255))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(),nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(),nullable=False, server_default=db.func.now(),onupdate=db.func.now())

    @property
    def data(self):
        return{
            'id':self.id,
            'email':self.email,
            'name':self.name,
            'priceperhour':self.priceperhour,
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
    def get_unassigned(cls):
        # Filter housekeepers who have no tasks assigned
        return cls.query.outerjoin(Task, Task.housekeeper_id == Housekeeper.id).filter(
            (Task.housekeeper_id == None) | (Task.is_done == True )).all()
    
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

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    housekeeper_id = db.Column(db.Integer, nullable=False)
    housekeeper_name = db.Column(db.String(255), nullable=False)
    workinghours = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    is_taken = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def data(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'housekeeper_id': self.housekeeper_id,
            'housekeeper_name': self.housekeeper_name,
            'address': self.address,
            'phone': self.phone,
            'summary': self.summary,
            'description': self.description,
            'workinghours': self.workinghours,
            'price': self.price,
            'is_done': self.is_done
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter(cls.user_id == user_id).all()
