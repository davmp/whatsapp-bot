from messages import Replies
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
from email_validator import validate_email, EmailNotValidError
from validate_docbr import CPF

class ResponseType:
    SAUDATION = [0, "olá", "ola", "oi", "eae", "hello", "hi", "bom dia", "boa tarde", "boa noite"]
    AFIRMATION = ["sim", "yes", "y", "ok"]
    NEGATION = ["nao", "no", "n", "não"]
    LEAVE_STATE = ["q", "quit", "sair", "cancel"]

    CHANGE_NAME = ["p", "mudar", "nome", "change", "change name", "name"]
    VIEW_LIST = ["l", "s", "listar"]
    EDIT_DATA = ["e", "editar", "edit"]

# 1 - Associe-se
# 2 - Covid-19
class UserState:
    AUTHENTICATION = {}
    AUTHENTICATION['1'] = ['name', 'email', 'cpf', 'registration', 'cargo'] # Associe-se
    AUTHENTICATION['2'] = ['name', 'email', 'cpf', 'endereço', 'p3'] # Exemplo p3 = 'ativo, aposentado ou pensionista'

class MessageHandler:
    def __init__(self, lang='br') -> None:
          self.lang = lang
          self.authenticator = Authenticator(User)
          self.validador = CPF()

    def format_response(self, response, user=None):
        text, media = response
        str(text).replace("{{prefix}}", Replies.Prefix.rand_prefix()).replace("{{name}}", user.name if user is not None else '')
        r = {'body': text, 'media': media}
        return r
    
    def format_auth_response(self, response, user, focus = True):
        text, media = response
        data = self.get_pending_data(user)

        if focus is True:
            if data == 'name':
                text = str(text).replace("Nome", ">*Nome*")
            elif data == 'email':
                text = str(text).replace("Email", ">*Email*")
            elif data == 'cpf':
                text = str(text).replace("CPF", ">*CPF*")
            elif data == 'registration':
                text = str(text).replace("Matricula", ">*Matricula*")
            elif data == 'cargo':
                text = str(text).replace("Cargo", ">*Cargo*")

        text = str(text).replace("{{prefix}}", Replies.Prefix.rand_prefix())
        text = str(text).replace("{{name}}", user.name if user.name is not None else '')
        text = str(text).replace("{{email}}", user.email if user.email is not None else '')
        text = str(text).replace("{{cpf}}", user.cpf if user.cpf is not None else '')
        text = str(text).replace("{{registration}}", user.registration if user.registration is not None else '')
        text = str(text).replace("{{cargo}}", user.cargo if user.cargo is not None else '')
        text = str(text).replace("{{endereço}}", user.endereço if user.endereço is not None else '')
        text = str(text).replace("{{p3}}", user.p3 if user.p3 is not None else '')
        r = {'body': text, 'media': media}
        return r
    
    def get_pending_data(self, user):
        if user is None or user.state == 0:
            return False
        for i in UserState.AUTHENTICATION[f'{user.state}']:
            if getattr(user, i) is None:
                return i
            else:
                continue
        return None
    
    def validate_email(self, email):
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
        
    def handle(self, message, sender):
        user = self.authenticator.get_user_by_number(sender)
        if user is not None:
            if user.name is None:
                if len(str(message).replace(" ", "")) <= 3 or len(str(message)) > 30:
                    return self.format_response(Replies.Errors.INVALID_NAME)
                else:
                    username = str(message).replace(" ", "").lower()[0].upper() + str(message).lower()[1:]
                    user = self.authenticator.update_username(sender, username)
                    text, media = Replies.SAUDATION2
                    body = str(text).replace("{{prefix}}", Replies.Prefix.rand_prefix()).replace("{{name}}", user.name)
                    return self.format_response((body, media))

            else:
                if user.state == 0:
                    if str(message).lower() in ResponseType.VIEW_LIST:
                        text, media = Replies.SAUDATION2
                        body = str(text).replace("{{prefix}}", Replies.Prefix.rand_prefix()).replace("{{name}}", user.name)
                        return self.format_response((body, media))
                    elif message == "1":
                        self.authenticator.update_state(sender, 1)
                        return self.format_auth_response(Replies.Authentication.AUTHENTICATION['1'], user)
                    elif message == "2":
                        return self.format_response(Replies.About.ABOUT_2)
                    elif message == "3":
                        return self.format_response(Replies.About.ABOUT_3)
                    elif message == "4":
                        return self.format_response(Replies.About.ABOUT_4)
                    elif message == "5":
                        return self.format_response(Replies.About.ABOUT_5)
                    elif message == "6":
                        return self.format_response(Replies.About.ABOUT_6)
                    elif message == "7":
                        return self.format_response(Replies.About.ABOUT_7)
                    elif message == "8":
                        return self.format_response(Replies.About.ABOUT_8)
                    elif message == "9":
                        return self.format_response(Replies.About.ABOUT_9)
                    elif str(message).lower() in ResponseType.CHANGE_NAME:
                        user.name = None
                        return self.format_response(Replies.CHANGE_NAME)
                    elif message == "creator":
                        return self.format_response(Replies.CREATOR)
                    else:
                        return self.format_response(Replies.Errors.INVALID_RESPONSE)
                else:
                    if str(message).lower() in ResponseType.LEAVE_STATE:
                        self.authenticator.update_state(sender, 0)
                        self.authenticator.update_editing_state(sender, False)
                        return self.format_response(Replies.SAUDATION2, user)
                    
                    elif str(message).lower() in ResponseType.VIEW_LIST:
                        return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)
                    
                    elif str(message).lower() in ResponseType.EDIT_DATA:
                        self.authenticator.update_editing_state(sender, True)
                        return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}', 'Edit'], user, False)
                    
                    if user.editing is True:
                        if str(message).lower() in ResponseType.LEAVE_STATE:
                            self.authenticator.update_editing_state(sender, False)
                            return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)
                        else:
                            data = Replies.Authentication.AUTHENTICATION[f'{user.state}']
                            if data == 'nome':
                                user = self.authenticator.update_username(sender, None)
                            elif data == 'email':
                                user = self.authenticator.update_email(sender, None)
                            elif data == 'cpf':
                                user = self.authenticator.update_cpf(sender, None)
                            else:
                                return self.format_response(Replies.Errors.INVALID_RESPONSE)
                            
                            return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user, False)
                        
                    else:
                        data = self.get_pending_data(user)

                        if data is None or data is False:
                            return self.format_response(Replies.SAUDATION2, user)
                        elif data == 'nome':
                            return self.format_response(Replies.SAUDATION)
                        elif data == 'email':
                            if self.validate_email(message):
                                email = str(message).lower().replace(" ", "")
                                user = self.authenticator.update_email(sender, email)
                                return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)
                            else:
                                return self.format_response(Replies.Errors.INVALID_EMAIL)
                        elif data == 'cpf':
                            if self.validador.validate(message) is True:
                                cpf = message
                                if len(str(message).replace(".")) == len(str(message)):
                                    # not formatted
                                    message = str(message)
                                    cpf = '{}.{}.{}-{}'.format(message[:3], message[3:6], message[6:9], message[9:])

                                user = self.authenticator.update_cpf(sender, cpf)
                                return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)
                            else:
                                return self.format_response(Replies.Errors.INVALID_CPF)
                        else:
                            return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)
        else:
            self.authenticator.save_user(sender)
            print("user created")
            return self.format_response(Replies.SAUDATION)
        
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
        endereço = Column(String)
        p3 = Column(Integer)
        state = Column(Integer, default=0) # 0 - normal, 1 - associando, 2 - cadastrando
        editing = Column(Boolean, default=False)

        def __repr__(self):
            return f"<User(number={self.number}, name={self.name}, email={self.email}, cpf={self.cpf}, registration={self.registration}, cargo={self.cargo}, endereço={self.endereço}, p3={self.p3}, state={self.state}, editing={self.editing})>".format(self.number, self.name, self.email, self.cpf, self.registration, self.cargo, self.endereço, self.p3, self.state, self.editing)

class Authenticator:
    database = create_engine("sqlite:///database.db", echo=True)
    Base.metadata.create_all(database)
    Session = sessionmaker(bind=database)
    session = Session()

    def __init__(self, user) -> None:
        self.user = user

    def save_user(self, user_number):
        self.user = User(number = user_number)
        self.session.add(self.user)
        self.session.commit()

    def update_state(self, user_number, state):
        q = self.session.query(User).filter(User.number == user_number).one_or_none()
        q.state = state
        q.editing = False
        self.session.commit()
        return q
    
    def update_editing_state(self, user_number, state):
        q = self.session.query(User).filter(User.number == user_number).one_or_none()
        q.editing = state
        self.session.commit()
        return q

    def update_username(self, user_number, name):
        q = self.session.query(User).filter(User.number == user_number).one_or_none()
        q.name = name
        self.session.commit()
        return q
    
    def update_email(self, user_number, email):
        q = self.session.query(User).filter(User.number == user_number).one_or_none()
        q.email = email
        self.session.commit()
        return q
    
    def update_cpf(self, user_number, cpf):
        q = self.session.query(User).filter(User.number == user_number).one_or_none()
        q.cpf = cpf
        self.session.commit()
        return q

    def get_user_by_number(self, number):
        try:
            q = self.session.query(User).filter(User.number == number).one_or_none()
            p = self.session.query(User, User.name != None)
            print("THIS IS P: " , p.all())
            return q
        except SQLAlchemyError as e:
            return None