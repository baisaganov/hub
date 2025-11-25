import configparser

import pandas as pd

from commons.types import BusinessProccess
from config.settings import config_path


def get_roles_list(bp_type: BusinessProccess):
    """
    Получение списка ролей из таблицы по Типу БП
    :param bp_type: BusinessProccess услуги
    :return: [str]
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    csv = pd.read_csv(config['testing_accs']['test_accs'])
    table_dict = csv.to_dict(orient='index')
    roles_list = []
    for index in table_dict:
        if table_dict.get(index)['service'] == bp_type.value:
            roles_list.append(table_dict.get(index))
    return roles_list
