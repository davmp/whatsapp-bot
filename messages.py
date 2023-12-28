import random


class ResponseType:
    SAUDATION = [0, "olá", "ola", "oi", "eae", "hello",
                 "hi", "bom dia", "boa tarde", "boa noite"]
    AFIRMATION = ["sim", "yes", "y", "ok"]
    NEGATION = ["nao", "no", "n", "não"]
    LEAVE_STATE = ["q", "quit", "sair", "cancel"]

    CHANGE_NAME = ["p", "mudar", "nome", "change", "change name", "name"]
    VIEW_LIST = ["l", "s", "listar"]
    EDIT_DATA = ["e", "editar", "edit"]


class Replies:
    SAUDATION = (
        "Olá, você acessou o atendimento digital da ANASP. 😃\n\nQual é o seu primeiro nome?", None)
    SAUDATION2 = ("Muito bem, *{{name}}*, seja bem vindo(a), Como podemos te ajudar? Digite apenas o *número* referente a opção desejada:\n\n1️⃣ Associe-se 🏢\n2️⃣ Institucional\n3️⃣ Quem é quem❓\n4️⃣ Benefícios 📌\n5️⃣ Resultados de Exames 📄\n6️⃣ Sou médico(a) 👨‍⚕️👩‍⚕️\n7️⃣ Demais solicitações❓\n8️⃣ Registrar reclamação 📝\n9️⃣ Agilizar meu atendimento da Unidade Nilópolis 📈\n\nPressione 'p' caso esse não seja seu nome.\nPressione 's' para receber novamente a lista de funcionalidades.",  None)
    SAUDATION3 = ("Você completou o cadastro de todos os campos necessários!\n\nMuito bem, *{{name}}*, seja bem vindo(a), Como podemos te ajudar? Digite apenas o *número* referente a opção desejada:\n\n1️⃣ Associe-se 🏢\n2️⃣ Institucional\n3️⃣ Quem é quem❓\n4️⃣ Benefícios 📌\n5️⃣ Resultados de Exames 📄\n6️⃣ Sou médico(a) 👨‍⚕️👩‍⚕️\n7️⃣ Demais solicitações❓\n8️⃣ Registrar reclamação 📝\n9️⃣ Agilizar meu atendimento da Unidade Nilópolis 📈\n\nPressione 'p' caso esse não seja seu nome.\nPressione 's' para receber novamente a lista de funcionalidades.",  None)
    SAUDATION4 = ("Você já é associado!\n\nMuito bem, *{{name}}*, seja bem vindo(a), Como podemos te ajudar? Digite apenas o *número* referente a opção desejada:\n\n1️⃣ Associe-se 🏢\n2️⃣ Institucional\n3️⃣ Quem é quem❓\n4️⃣ Benefícios 📌\n5️⃣ Resultados de Exames 📄\n6️⃣ Sou médico(a) 👨‍⚕️👩‍⚕️\n7️⃣ Demais solicitações❓\n8️⃣ Registrar reclamação 📝\n9️⃣ Agilizar meu atendimento da Unidade Nilópolis 📈\n\nPressione 'p' caso esse não seja seu nome.\nPressione 's' para receber novamente a lista de funcionalidades.",  None)
    CHANGE_NAME = (
        "Desculpe pelo inconveniente.\nPor favor, digite seu nome para continuar...", None)
    TROLL = ("This is what happeneds when you Fall in love with someone",
             "https://imgur.com/OT1iqwT.gif")
    GRAPE = ("evolute's icon, if you can take a look...", None)
    STRAW = ("https://media.giphy.com/media/3o7aCj5V9tXOjy2wRy/giphy.gif", None)
    REQUIRES_IDENTITY = ("Por favor, digite seu nome para continuar", None)

    ABOUT = {}
    ABOUT['1'] = ("*Covid-19* - Agendamento e Informações 📆\n\nA ANASP é uma associação sem fins lucrativos, que tem como objetivo oferecer serviços de saúde de qualidade a preços acessíveis. A ANASP é uma associação sem fins lucrativos, que tem como objetivo oferecer serviços de saúde de qualidade a preços acessíveis.", None)
    ABOUT['2'] = ("Análises Clínicas (inclusive pela Coleta Domiciliar)\n\nA ANASP tem como objetivo oferecer informações sobre os exames solicitados pelo SUS. Essas informações são obtidas através de laborato", None)
    ABOUT['3'] = ("Ultrassonografia 🖥️\n\nA ANASP tem como objetivo oferecer informações sobre os exames solicitados pelo SUS. Essas informações são obtidas através de laborato", None)
    ABOUT['4'] = ("Endereços e Horários de funcionamento das Unidades 📌\n\nA ANASP tem como objetivo oferecer informações sobre os exames solicitados pelo SUS. Essas informações são obtidas através de laborato",
                  "http://127.0.0.1:8000/evolute-logo-teste.png")
    ABOUT['5'] = ("Resultados de Exames 📄\n\nA ANASP tem como objetivo oferecer informações sobre os exames solicitados pelo SUS. Essas informações são obtidas através de laborato", None)
    ABOUT['6'] = ("Sou médico(a) 👨‍⚕️👩‍⚕️\n\nA ANASP tem como objetivo oferecer informações sobre os exames solicitados pelo SUS. Essas informações são obtidas através de laborato", None)
    ABOUT['7'] = ("Demais solicitações❓\n\nA ANASP tem como objetivo oferecer informações sobre os exames solicitados pelo SUS. Essas informações são obtidas através de laborato", None)
    ABOUT['8'] = ("Registrar reclamação 📝\n\nA ANASP tem como objetivo oferecer informações sobre os exames solicitados pelo SUS. Essas informações são obtidas através de laborato", None)
    ABOUT['9'] = ("Agilizar meu atendimento da Unidade Nilópolis 📈\n\nA ANASP tem como objetivo oferecer informações sobre os exames solicitados pelo SUS. Essas informações são obtidas através de laborato", None)
    ABOUT['10'] = ("O criador desse bot é o @evolute, se você quiser entrar em contato com ele, mande uma mensagem para o número +55 21 97900-0000",
                   "https://i.ibb.co/MVXbB4W/Whats-App-Image-2023-12-09-at-15-00-20-b3e9bc9b.jpg")

    class Authentication:
        AUTHENTICATION = {}
        AUTHENTICATION['1'] = ("{{prefix}}, {{name}}!\n\nAgora nós precisamos do seguinte dado:\n\nNome: {{name}}\nEmail: {{email}}\nCPF: {{cpf}}\nMatricula: {{registration}}\nCargo: {{cargo}}\n\nDigite *apenas* o dado solicitado.\n\nPara sair, digite *q*\nPara mudar algum dado, digite *editar*", None)
        AUTHENTICATION['1', 'Edit'] = (
            "Qual dado deseja alterar?\n\n1 - Nome: _{{name}}_\n2 - Email: _{{email}}_\n3 - CPF: _{{cpf}}_\n4 - Matricula: _{{registration}}_\n5 - Cargo: _{{cargo}}_\n\nPara sair, digite *q*\nPara confirmar, digite *apenas* o número solicitado. Exemplo: 2 (Edita o Email)", None)

        AUTHENTICATION['2'] = (
            "Nome: {{name}}\nEmail: {{email}}\nCPF: {{cpf}}\nEndereço: {{endereço}}\n1 - Ativo\n2 - Aposentado\n3 - Pensionista: {{p3}}", None)

    class Errors:
        INVALID_NAME = ("Por favor, digite um Primeiro Nome válido.", None)
        INVALID_RESPONSE = (
            f"Por favor, digite uma resposta já reconhecida.", None)
        INVALID_EMAIL = ("Por favor, digite um email válido.", None)
        INVALID_CPF = ("Por favor, digite um CPF válido.", None)
        INVALID_REGISTRATION = (
            "Por favor, digite uma matrícula válida.", None)
        INVALID_CARGO = ("Por favor, digite um cargo válido.", None)

    class Confirmation:
        NAME = "{{prefix}}, {{name}}.\n\nPressione 'p' caso esse não seja o seu nome.Está correto?"

    class Prefix:
        PREFIXES = [
            "Certo",
            "Muito bem",
            "Beleza",
            "Boa"
        ]

        def rand_prefix():
            return Replies.Prefix.PREFIXES[random.randint(0, len(Replies.Prefix.PREFIXES) - 1)]
