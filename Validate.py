from validate_docbr import CPF
import re


def isEmailValid(email: str) -> bool:
    regex = re.compile(
        r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    return True if re.fullmatch(regex, email) else False


def isCPFValid(cpf: str) -> bool:
    validator = CPF()
    return validator.validate(cpf)


def isCPFFormated(cpf: str) -> bool:
    return True if re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf) else False


def isMatriculaValid(matricula: str) -> bool:
    return True if re.match(r"\d{6}", matricula) else False


def validateAndFormatCPF(cpf: str) -> str:
    if isCPFValid(cpf):
        if not isCPFFormated(cpf):
            # not formatted
            cpf = str(cpf).replace(
                ".", "").replace("-", "")
            return '{}.{}.{}-{}'.format(
                cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
        return cpf
    return None


def isCargoValid(cargo: str) -> bool:
    return True


def validateName(name: str) -> str:
    if len(str(name).replace(" ", "")) <= 3 or len(str(name)) > 30:
        return None
    return str(name).strip().title()
