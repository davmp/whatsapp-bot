from messages import Replies, ResponseType

from UserEntity import UserRepository
import Validate
from messager import Messager

# 1 - Associe-se
# 2 - Covid-19


class UserState:
    AUTHENTICATION = {}
    AUTHENTICATION['1'] = ['name', 'email', 'cpf',
                           'registration', 'cargo']  # Associe-se
    # Exemplo p3 = 'ativo, aposentado ou pensionista'
    AUTHENTICATION['2'] = ['name', 'email', 'cpf', 'endereço', 'p3']


class MessageHandler:
    def __init__(self, lang='br') -> None:
        self.lang = lang
        self.repository = UserRepository()
        self.messager = Messager()

    def format_response(self, response, user=None):
        text, media = response
        text = str(text).replace("{{prefix}}", Replies.Prefix.rand_prefix()).replace(
            "{{name}}", user.name if user is not None else '')
        return {'body': text, 'media': media}

    def format_auth_response(self, response, user, focus=True, on_completion=None):
        text, media = response
        data = self.get_pending_data(user)
        print("pending data in format_auth_response: ", data)
        print("onCompletion: ", on_completion)
        if data is None and on_completion is not None:
            print("data is none")
            return on_completion(user)

        if focus is True:
            match data:
                case 'name':
                    text = str(text).replace("Nome", "> *Nome*")
                case 'email':
                    text = str(text).replace("Email", "> *Email*")
                case 'cpf':
                    text = str(text).replace("CPF", "> *CPF*")
                case 'registration':
                    text = str(text).replace("Matricula", "> *Matricula*")
                case 'cargo':
                    text = str(text).replace("Cargo", "> *Cargo*")

        text = str(text).replace("{{prefix}}", Replies.Prefix.rand_prefix())
        text = str(text).replace(
            "{{name}}", user.name if user.name is not None else '')
        text = str(text).replace(
            "{{email}}", user.email if user.email is not None else '')
        text = str(text).replace(
            "{{cpf}}", user.cpf if user.cpf is not None else '')
        text = str(text).replace(
            "{{registration}}", user.registration if user.registration is not None else '')
        text = str(text).replace(
            "{{cargo}}", user.cargo if user.cargo is not None else '')
        text = str(text).replace(
            "{{endereço}}", user.endereco if user.endereco is not None else '')
        text = str(text).replace(
            "{{p3}}", user.p3 if user.p3 is not None else '')
        return {'body': text, 'media': media}

    def get_pending_data(self, user):
        if user is None or user.state == 0:
            return False
        for i in UserState.AUTHENTICATION[f'{user.state}']:
            if getattr(user, i) is None:
                print("pending data: ", i)
                return i
            else:
                continue
        return None

    def handle_non_user(self, sender, message, user):
        if user is None:
            self.repository.save_user(sender)
            print("user created")
            return self.format_response(Replies.SAUDATION)

        username = Validate.validateName(message)
        if username is None:
            return self.format_response(Replies.Errors.INVALID_NAME)

        user = self.repository.update_field(sender, 'name', username)
        text, media = Replies.SAUDATION2
        body = str(text).replace("{{prefix}}", Replies.Prefix.rand_prefix()).replace(
            "{{name}}", user.name)
        return self.format_response((body, media))

    async def handle_user_in_menu(self, sender, user, message):
        if message in ResponseType.VIEW_LIST:
            text, media = Replies.SAUDATION2
            body = str(text).replace("{{prefix}}", Replies.Prefix.rand_prefix()).replace(
                "{{name}}", user.name)
            return self.format_response((body, media))
        elif message == "1":
            if (user.associated is True):
                await self.messager.send_message(
                    Replies.SAUDATION4[0], sender)
                return self.format_response(Replies.SAUDATION2, user)
            self.repository.update_state(sender, 1)
            return self.format_auth_response(Replies.Authentication.AUTHENTICATION['1'], user)

        elif message in ResponseType.CHANGE_NAME:
            user.name = None
            return self.format_response(Replies.CHANGE_NAME)

        return self.format_response(Replies.ABOUT.get(message, Replies.Errors.INVALID_RESPONSE))

    def handle_user_in_auth_edit(self, sender, user, message):
        match message:
            case "1":
                user = self.repository.update_field(
                    sender, 'name', None)
            case "2":
                user = self.repository.update_field(
                    sender, 'email', None)
            case "3":
                user = self.repository.update_field(
                    sender, 'cpf', None)
            case "4":
                user = self.repository.update_field(
                    sender, 'registration', None)
            case "5":
                user = self.repository.update_field(
                    sender, 'cargo', None)
            case _:
                if (message in ResponseType.LEAVE_STATE):
                    self.repository.update_editing_state(
                        sender, False)
                    return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)
                return self.format_response(Replies.Errors.INVALID_RESPONSE)
        self.repository.update_editing_state(
            sender, False)
        return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)

    def handle_data_update(self, sender, message, field, validation_func, error_response):
        validation = validation_func(message)

        if validation is not None and validation is not False:
            user = self.repository.update_field(sender, field, message)
            print("handle data update: ", self.handle_user_completed_sign_up)
            return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user, on_completion=self.handle_user_completed_sign_up)
        else:
            return self.format_response(error_response)

    async def handle_user_completed_sign_up(self, user):
        print("user completed sign up")
        self.repository.update_field(user.number, 'associated', True)
        self.repository.update_state(user.number, 0)
        await self.messager.send_message(
            Replies.SAUDATION3[0], user.number)
        return self.format_response(Replies.SAUDATION2, user)

    async def handle_user_signing_up(self, sender, user, message):
        data = self.get_pending_data(user)
        print("data: ", data)
        match data:
            case None:
                self.repository.update_editing_state(sender, False)
                self.repository.update_state(sender, 0)
                await self.messager.send_message(
                    Replies.SAUDATION3[0], sender)
                return self.format_response(Replies.SAUDATION2, user)
            case 'nome':
                return self.format_response(Replies.SAUDATION)
            case 'email':
                email = str(message).lower().strip()
                return self.handle_data_update(
                    sender, email, 'email', Validate.isEmailValid, Replies.Errors.INVALID_EMAIL)
            case 'cpf':
                return self.handle_data_update(
                    sender, message, 'cpf', Validate.validateAndFormatCPF, Replies.Errors.INVALID_CPF)
            case 'registration':
                return self.handle_data_update(
                    sender, message, 'registration', Validate.isMatriculaValid, Replies.Errors.INVALID_REGISTRATION)
            case 'cargo':
                return self.handle_data_update(
                    sender, message, 'cargo', Validate.isCargoValid, Replies.Errors.INVALID_CARGO)
            case _:
                return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)

    def handle_user_in_auth(self, sender, user, message):
        if message in ResponseType.LEAVE_STATE:
            self.repository.update_state(sender, 0)
            self.repository.update_editing_state(sender, False)
            return self.format_response(Replies.SAUDATION2, user)

        elif message in ResponseType.VIEW_LIST:
            return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)

        elif message in ResponseType.EDIT_DATA:
            self.repository.update_editing_state(sender, True)
            return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}', 'Edit'], user, False)

        if user.editing is True:
            return self.handle_user_in_auth_edit(sender, user, message)

        else:
            return self.handle_user_signing_up(sender, user, message)

    def handle(self, message, sender):
        user = self.repository.get_user_by_number(sender)
        message = str(message).lower().strip()

        if user is None or user.name is None:
            return self.handle_non_user(sender, message, user)

        else:
            if user.state == 0:
                return self.handle_user_in_menu(sender, user, message)
            else:
                return self.handle_user_in_auth(sender, user, message)
