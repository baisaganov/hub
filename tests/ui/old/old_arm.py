import configparser
import pytest
import allure


from commons.types import AccreditationRoles, AccreditationType
from pages.arm.arm_accreditation_page import ArmAccreditationPage
from config.settings import config_path


@allure.suite("ARM")
class TestArm:
    config = configparser.ConfigParser()
    config.read(config_path)

    @allure.title("Позитивный сценарий аккредитации")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "acred_type, account_data",
        [
            (AccreditationType.RENEWAL_FL, {'iin': '990315351258'}),
            # (AccreditationType.DUBLICATE_FL, {'iin': '990315351258'})
        ],
        ids=[
            "Аккредитация Переоформление ФЛ",
            # "Аккредитация Дубликат ФЛ",
            ]
    )
    # @pytest.mark.skip("Решение проблемы с подписанием")
    def test_positive_accreditation(self, page, acred_type: AccreditationType, account_data: dict):
        self.config.clear()
        self.config.read(config_path)
        request_id = self.config['service_requests'][acred_type.value + '_id']
        arm = ArmAccreditationPage(page, request_id=request_id, account_data=account_data)

        with allure.step('0. Проверяем, есть ли заявка'):
            request_id = arm.get_request_id(acred_type)
            assert request_id != '0', f'{acred_type.value}_id: Заявки нет'

        with allure.step('1. Председатель комитета назначает на Рук. упр.'):
            arm.assign_leader()

        with allure.step('2. Рук. упр. назначает ответсвенного исполнителя'):
            arm.leader_appoints_executor()

        with allure.step('3. Отв. исполнитель формирует акт экспертизы на выдачу'):
            arm.executor_forms_act()

        with allure.step('4. Рук. упр. подписывает акт'):
            arm.leader_signs_act()

        with allure.step('5. Отв. исполнитель формирует приказ о переоформлении и подписывает'):
            arm.executor_forms_decree()

        with allure.step('6. Рук. упр. подписывает приказ'):
            arm.approve_decree_by_(AccreditationRoles.RUK_UPR)

        with allure.step('7. Зам. пред. подписывает приказ'):
            arm.approve_decree_by_(AccreditationRoles.ZAM_PRED)

        with allure.step('8. Председатель подписывает приказ'):
            arm.approve_decree_by_(AccreditationRoles.PRED)

        page.pause()
        # with allure.step('9. Очищаем ID заявки'):
        #     arm.clear_service_id(acred_type.value+'_id')
        #
        # with allure.step('10. Удаляем заявку из системы'):
        #     admin = AdminAPI()
        #     admin.delete_service_by_id(request_id)
