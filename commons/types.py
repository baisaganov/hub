from enum import Enum


class ServiceType(str, Enum):
    ACCRED = 'Accreditation'
    ACCRED_RENEWAL = 'Accreditation Renewal'
    ACCRED_ARM = 'Accreditation Renewal ARM'
    HUBID = 'HUB_ID'
    ACCOUNT = 'Account'
    ADMIN = 'admin'


class AdminFuncTypes(str, Enum):
    CHANGE = 'change'
    CLEAR = 'clear'


class AdminAccountChangeType(str, Enum):
    IIN = 'iin'
    EMAIL = 'email'
    USER_ID = 'user_id'


class AccreditationType(str, Enum):
    RENEWAL_FL = 'accreditation_renewal_fl'
    RENEWAL_UL = 'accreditation_renewal_ul'
    DUBLICATE_FL = 'accreditation_dublicate_fl'
    DUBLICATE_UL = 'accreditation_dublicate_ul'


class FormButton(str, Enum):
    SAVE = 'save'
    NEXT = 'next'
    PREV = 'previous'
    SUBMIT = 'submit'
    ECP_SUBMIT = 'sign_submit'


class BusinessProccess(str, Enum):
    """Наименования услуги из Таблица с тестовыми аккаунтами"""
    ACCREDITATION = 'Аккредитация'


class AccreditationRoles(str, Enum):
    """
    Наименования ролей по процессу Аккредитации
    """
    RUK_UPR = 'accreditation_department_head'
    ZAM_PRED = 'accreditation_deputy_chairman'
    OTV_ISP = 'accreditation_executor'
    PRED = 'accreditation_chairman'
