from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    number = Column(String)
    name = Column(String)
    email = Column(String)
    cpf = Column(String)
    registration = Column(String)
    cargo = Column(String)
    endereco = Column(String)
    p3 = Column(Integer)
    # 0 - normal, 1 - associando, 2 - cadastrando
    state = Column(Integer, default=0)
    editing = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(number={self.number}, name={self.name}, email={self.email}, cpf={self.cpf}, registration={self.registration}, cargo={self.cargo}, endereço={self.endereco}, p3={self.p3}, state={self.state}, editing={self.editing})>".format(self.number, self.name, self.email, self.cpf, self.registration, self.cargo, self.endereco, self.p3, self.state, self.editing)


class Repository:
    database = create_engine("sqlite:///database.db", echo=True)
    Base.metadata.create_all(database)
    Session = sessionmaker(bind=database)
    session = Session()

    def save_user(self, user_number):
        user = User()
        user.number = user_number
        self.session.add(user)
        self.session.commit()

    def update_state(self, user_number, state):
        q = self.session.query(User).filter(
            User.number == user_number).one_or_none()
        q.state = state
        q.editing = False
        self.session.commit()
        return q

    def update_editing_state(self, user_number, state):
        q = self.session.query(User).filter(
            User.number == user_number).one_or_none()
        q.editing = state
        self.session.commit()
        return q

    def update_username(self, user_number, name):
        q = self.session.query(User).filter(
            User.number == user_number).one_or_none()
        q.name = name
        self.session.commit()
        return q

    def update_email(self, user_number, email):
        q = self.session.query(User).filter(
            User.number == user_number).one_or_none()
        q.email = email
        self.session.commit()
        return q

    def update_cpf(self, user_number, cpf):
        q = self.session.query(User).filter(
            User.number == user_number).one_or_none()
        q.cpf = cpf
        self.session.commit()
        return q

    def update_field(self, user_number, field, value):
        result = self.session.query(User).filter(
            User.number == user_number).one_or_none()
        result.__setattr__(str(field), value)
        self.session.commit()
        return result

    def get_user_by_number(self, number):
        try:
            q = self.session.query(User).filter(
                User.number == number).one_or_none()
            p = self.session.query(User, User.name != None)
            print("THIS IS P: ", p.all())
            return q
        except SQLAlchemyError as e:
            print("Error: ", e)
            return None
