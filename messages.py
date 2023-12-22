from PIL import Image

evolute = Image.open("evolute-logo-teste.png")

class Replies:
    SAUDATION = ("Ola *Ewerton Nicacio Junior*, você acessou o atendimento digital da Lafe. 😃\nQual é o seu primeiro nome?", None)
    SAUDATION2 = ("Muito bem, {{name}}, seja bem {{voice}}, Como podemos te ajudar? Digite apenas o *número* referente a opção desejada:\n\n1️⃣ *Covid-19* - Agendamento e Informações 📆\n2️⃣ Análises Clínicas (inclusive pela Coleta Domiciliar)\n3️⃣ Ultrassonografia 🖥️\n4️⃣ Endereços e Horários de funcionamento das Unidades 📌\n5️⃣ Resultados de Exames 📄\n6️⃣ Sou {{doctor}} 👨‍⚕️👩‍⚕️\n7️⃣ Demais solicitações❓\n8️⃣ Registrar reclamação 📝\n9️⃣ Agilizar meu atendimento da Unidade Nilópolis 📈",  None)
    TROLL = ("This is what happeneds when you Fall in love with someone", "https://imgur.com/OT1iqwT.gif")
    GRAPE = ("evolute's icon, if you can take a look...", evolute)
    STRAW = ("https://media.giphy.com/media/3o7aCj5V9tXOjy2wRy/giphy.gif", None)
    REQUIRES_IDENTITY = ("Por favor, digite seu nome para continuar", None)