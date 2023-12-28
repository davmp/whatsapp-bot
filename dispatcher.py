from messages import Replies, ResponseType

from Repository import Repository
import Validate

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
        self.repository = Repository()

    def format_response(self, response, user=None):
        text, media = response
        text = str(text).replace("{{prefix}}", Replies.Prefix.rand_prefix()).replace(
            "{{name}}", user.name if user is not None else '')
        r = {'body': text, 'media': media}
        return r

    def format_auth_response(self, response, user, focus=True):
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
        r = {'body': text, 'media': media}
        return r

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

    def handle(self, message, sender):
        user = self.repository.get_user_by_number(sender)
        if user is not None:
            if user.name is None:
                if len(str(message).replace(" ", "")) <= 3 or len(str(message)) > 30:
                    return self.format_response(Replies.Errors.INVALID_NAME)
                else:
                    username = str(message).replace(" ", "").lower()[
                        0].upper() + str(message).lower()[1:]
                    user = self.repository.update_username(sender, username)
                    text, media = Replies.SAUDATION2
                    body = str(text).replace("{{prefix}}", Replies.Prefix.rand_prefix()).replace(
                        "{{name}}", user.name)
                    return self.format_response((body, media))

            else:
                if user.state == 0:
                    if str(message).lower() in ResponseType.VIEW_LIST:
                        text, media = Replies.SAUDATION2
                        body = str(text).replace("{{prefix}}", Replies.Prefix.rand_prefix()).replace(
                            "{{name}}", user.name)
                        return self.format_response((body, media))
                    elif message == "1":
                        self.repository.update_state(sender, 1)
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
                        self.repository.update_state(sender, 0)
                        self.repository.update_editing_state(sender, False)
                        return self.format_response(Replies.SAUDATION2, user)

                    elif str(message).lower() in ResponseType.VIEW_LIST:
                        return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)

                    elif str(message).lower() in ResponseType.EDIT_DATA:
                        self.repository.update_editing_state(sender, True)
                        return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}', 'Edit'], user, False)

                    if user.editing is True:
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
                                if (str(message).lower() in ResponseType.LEAVE_STATE):
                                    self.repository.update_editing_state(
                                        sender, False)
                                    return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)
                                return self.format_response(Replies.Errors.INVALID_RESPONSE)
                        self.repository.update_editing_state(
                            sender, False)
                        return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)

                    else:
                        data = self.get_pending_data(user)

                        # TODO: enviar mensagem de 'voce ja é associado' e dps mostrar o menu
                        if data is None:
                            return self.format_response(Replies.SAUDATION2, user)
                        elif data == 'nome':
                            return self.format_response(Replies.SAUDATION)
                        elif data == 'email':
                            email = str(message).lower().strip()
                            if Validate.isEmailValid(email):
                                user = self.repository.update_email(
                                    sender, email)
                                return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)
                            else:
                                return self.format_response(Replies.Errors.INVALID_EMAIL)
                        elif data == 'cpf':
                            cpf = Validate.validateAndFormatCPF(message)
                            if cpf is not None:
                                user = self.repository.update_cpf(
                                    sender, cpf)
                                return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)
                            return self.format_response(Replies.Errors.INVALID_CPF)
                        elif data == 'registration':
                            if Validate.isMatriculaValid(message):
                                user = self.repository.update_field(
                                    sender, 'registration', message)
                                return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)
                            return self.format_response(Replies.Errors.INVALID_REGISTRATION)
                        elif data == 'cargo':
                            if Validate.isCargoValid(message):
                                user = self.repository.update_field(
                                    sender, 'cargo', message)
                                return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)
                            return self.format_response(Replies.Errors.INVALID_CARGO)
                        else:
                            return self.format_auth_response(Replies.Authentication.AUTHENTICATION[f'{user.state}'], user)
        else:
            self.repository.save_user(sender)
            print("user created")
            return self.format_response(Replies.SAUDATION)
