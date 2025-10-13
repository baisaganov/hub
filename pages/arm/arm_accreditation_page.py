import time

from base.arm_base_page import ArmBasePage
from commons.types import BusinessProccess, AccreditationRoles, AdminFuncTypes, AdminAccountChangeType, ServiceType
from config.links import Links
from services.admin_api import AdminAPI
from services.services import get_roles_list
import allure

from services.egov.sign_service import SignXml


class ArmAccreditationPage(ArmBasePage):

    def __init__(self, page, request_id, account_data: dict[str, str]):
        super().__init__(page)
        self.admin = AdminAPI()
        self.data = account_data
        self.roles_list = get_roles_list(BusinessProccess.ACCREDITATION)
        self.request_id = request_id
        self.request_id_url = Links.ARM_SERVICE_REQUEST + request_id

    def assign_leader(self):
        """
        Председатель комитета назначает ответсвенного исполнителя
        :return:
        """
        roles_id = next((i for i in self.roles_list if i['role_code'] == 'accreditation_chairman'), None)
        self.admin.change_user(change_mode=AdminAccountChangeType.IIN,
                               data=self.data,
                               user_id=roles_id['id'],
                               functinonality=AdminFuncTypes.CHANGE)

        self.auth_arm(login=roles_id['login'], password='Pass1234!')

        self.nav(self.request_id_url)

        button_list = self.get_button_list()

        assert (len(button_list) == 1 and button_list[0] != ''), self.error_info(
            msg="Нет кнопок у Председателя комитета")

        self.click_on_button(button_list[0])

        self.page.wait_for_selector('div.modal-component')

        users_list = self.get_users_list()
        assert len(users_list) != 0, self.error_info(msg="Нет списка пользователей у Председателя комитета")

        self.click_on_button('Руководитель Управления Аккредитация', 'span')

        with self.page.expect_response(
                'https://dev.astanahub.com/arm/service_request/' + self.request_id + '/process_action/') as response:
            self.click_on_button('Отправить', 'button')

        assert response.value.status == 200, self.error_info(status=response.value.status,
                                                             msg="Рук упр не назначен")
        button_list = self.get_button_list()
        self.logging.error(f"{button_list} BUTTON LIST 60 ARM")
        assert len(button_list) <= 0 or button_list[0] == '', self.error_info(msg="Кнопки остались у "
                                                                                  "Руководителя Управления")

        self.logout_arm()

    def leader_appoints_executor(self):
        """
        Рук. упр. назначает Ответсвенного исполнителя
        :return:
        """
        roles_id = next((i for i in self.roles_list if i['role_code'] == 'accreditation_department_head'), None)
        self.admin.change_user(change_mode=AdminAccountChangeType.IIN, data=self.data, user_id=roles_id['id'], functinonality=AdminFuncTypes.CHANGE)

        self.auth_arm(login=roles_id['login'], password='Pass1234!')

        self.nav(self.request_id_url)

        button_list = self.get_button_list()

        assert len(button_list) == 1 and button_list[0] != '', self.error_info(
            msg="Нет кнопок у Рук. упр.")

        self.click_on_button(button_list[0])

        self.page.wait_for_selector('div.modal-component')

        users_list = self.get_users_list()
        assert len(users_list) != 0, self.error_info(msg="Нет списка пользователей у Рук. упр.")

        self.click_on_button('Ответственный исполнитель (Аккредитация)', 'span')

        with self.page.expect_response('https://dev.astanahub.com/arm/service_request/'
                                       + self.request_id + '/process_action/') as response:
            self.click_on_button('Отправить', 'button')

        assert response.value.status == 200, self.error_info(status=response.value.status,
                                                             msg="Ошибка при назнанчении Отв. исп.")

        button_list = self.get_button_list()

        assert len(button_list) <= 1 and button_list[0] == '', self.error_info(msg="Кнопки остались")

        self.logout_arm()

    def executor_forms_act(self):
        """
        Отв. исполнитель формирует акт экспертизы на выдачу
        :return:
        """
        roles_id = next((i for i in self.roles_list if i['role_code'] == 'accreditation_executor'), None)
        self.admin.change_user(change_mode=AdminAccountChangeType.IIN, data=self.data, user_id=roles_id['id'], functinonality=AdminFuncTypes.CHANGE)

        self.auth_arm(login=roles_id['login'], password='Pass1234!')

        self.nav(self.request_id_url)

        button_list = self.get_button_list()

        assert len(button_list) == 2, self.error_info(
            msg="Нет кнопок у Отв исп")

        self.click_on_button(button_list[0])

        button_list = self.get_button_list()

        assert len(button_list) == 4, self.error_info(
            msg="Нет кнопок у Отв исп (Акт на выдачу, Акт отказа, Редкатировать, Подписать)")

        self.click_on_button(button_list[0], tag='button')

        button_list = self.get_button_list()
        self.click_on_button(button_list[-1])

        with self.page.expect_response('https://dev.astanahub.com/arm/service_request/' + self.request_id
                                       + '/process_action/') as response:
            SignXml().sign_xml()

        time.sleep(5)

        assert response.value.status == 200, self.error_info(status=response.value.status, msg="Ошибка при подписании")

        button_list = self.get_button_list()

        assert len(button_list) <= 1 and button_list[0] == '', self.error_info(msg="Кнопки остались")

        self.logout_arm()

    def leader_signs_act(self):
        """
        Рук. упр. подписывает акт
        :return:
        """
        roles_id = next((i for i in self.roles_list if i['role_code'] == 'accreditation_department_head'), None)
        self.admin.change_user(change_mode=AdminAccountChangeType.IIN, data=self.data, user_id=roles_id['id'], functinonality=AdminFuncTypes.CHANGE)

        self.auth_arm(login=roles_id['login'], password='Pass1234!')

        self.nav(self.request_id_url)

        button_list = self.get_button_list()

        assert len(button_list) == 2, self.error_info(msg="Нет кнопок у Рук. упр. (Отправить на доработку, Подписать)")

        self.click_on_button(button_list[-1])
        with self.page.expect_response('https://dev.astanahub.com/arm/service_request/' + self.request_id
                                       + '/process_action/') as response:
            SignXml().sign_xml()

        assert response.value.status == 200, self.error_info(status=response.value.status, msg="Ошибка при подписании")

        button_list = self.get_button_list()

        assert len(button_list) <= 1 and button_list[0] == '', self.error_info(msg="fКнопки остались {button_list}")

        self.logout_arm()

    def executor_forms_decree(self):
        """
        Отв. исполнитель формирует приказ о переоформлении и подписывает
        :return:
        """
        roles_id = next((i for i in self.roles_list if i['role_code'] == 'accreditation_executor'), None)
        self.admin.change_user(change_mode=AdminAccountChangeType.IIN, data=self.data, user_id=roles_id['id'], functinonality=AdminFuncTypes.CHANGE)

        self.auth_arm(login=roles_id['login'], password='Pass1234!')

        self.nav(self.request_id_url)

        button_list = self.get_button_list()

        assert len(button_list) == 1 and button_list[0] != '', self.error_info(
            msg="Нет кнопоки у Отв. исполнител (Создать приказ)")

        with self.page.expect_response(f'https://dev.astanahub.com/arm/service_request/{self.request_id}/'
                                       f'process_action/') as resp:
            self.click_on_button(button_list[0])

        assert resp.value.status == 200, self.error_info(status=resp.value.status, msg="Не удалось создать приказ")

        button_list = self.get_button_list()

        assert len(button_list) == 2 and button_list[0] != '', self.error_info(
            msg="Нет кнопоки у Отв. исп (Подписать, Редактировать)")

        with self.page.expect_response(f'https://dev.astanahub.com/arm/service_request/{self.request_id}/'
                                       f'process_action/') as resp:
            self.click_on_button(button_list[0])
            SignXml().sign_xml()

        assert resp.value.status == 200, self.error_info(status=resp.value.status, msg="Не удалось подписать")

        self.logout_arm()

    def approve_decree_by_(self, role: AccreditationRoles):
        """
        Согласование приказа разными ролями
        :param role: Роль юзера, кто должнен согласовать
        :return:
        """
        roles_id = next((i for i in self.roles_list if i['role_code'] == role.value), None)
        self.admin.change_user(change_mode=AdminAccountChangeType.IIN, data=self.data, user_id=roles_id['id'], functinonality=AdminFuncTypes.CHANGE)

        self.auth_arm(login=roles_id['login'], password='Pass1234!')

        self.nav(self.request_id_url)

        button_list = self.get_button_list()

        assert len(button_list) > 0 and button_list[0] != '', self.error_info(msg=f"Кнопок нет у {role.value}")

        with self.page.expect_response(f'https://dev.astanahub.com/arm/service_request/{self.request_id}/'
                                       f'process_action/') as resp:
            self.click_on_button(button_list[1])
            SignXml().sign_xml()

        assert resp.value.status == 200, self.error_info(status=resp.value.status,
                                                         msg=f"Не удалось подписать {role.value}")

        button_list = self.get_button_list()

        if role == role.PRED and len(button_list) == 2 and button_list[0] == 'Подписать':
            with self.page.expect_download() as download_info, \
                    self.page.expect_response(f'https://dev.astanahub.com/arm/service_request/{self.request_id}/'
                                              f'process_action/') as resp:
                self.click_on_button(button_list[-1])

            download = download_info.value

            download_path = 'docs/tmp_path/' + download.suggested_filename
            download.save_as(download_path)

            with open(download_path, "rb") as f:
                allure.attach(f.read(), name=download.suggested_filename, attachment_type=allure.attachment_type.PDF)

            assert resp.value.status == 200, self.error_info(status=resp.value.status,
                                                             msg=f"Не удалось скачать файл "
                                                                 f"при предпросмотре {role.value}")

            with self.page.expect_response(f'https://dev.astanahub.com/arm/service_request/{self.request_id}/'
                                           f'process_action/') as resp:
                self.click_on_button(button_list[0])
                SignXml().sign_xml()

            assert resp.value.status == 200, self.error_info(status=resp.value.status,
                                                             msg=f"Не удалось скачать файл "
                                                                 f"при предпросмотре {role.value}")

            button_list = self.get_button_list()
            assert len(button_list) >= 1 and button_list[0] != '', self.error_info(msg=f"Кнопок нет {role.value}")

            with self.page.expect_download() as download_info, \
                    self.page.expect_response(f'https://dev.astanahub.com/arm/service_request/{self.request_id}/'
                                              f'process_action/') as resp:
                self.click_on_button(button_list[0])

            download = download_info.value

            download_path = 'docs/tmp_path/' + download.suggested_filename
            download.save_as(download_path)

            with open(download_path, "rb") as f:
                allure.attach(f.read(), name=download.suggested_filename, attachment_type=allure.attachment_type.PDF)

            assert resp.value.status == 200, self.error_info(status=resp.value.status,
                                                             msg=f"Не удалось скачать файл при одобрении {role.value}")

        self.logout_arm()
