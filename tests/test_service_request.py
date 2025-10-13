import configparser

import allure
import pytest


from commons.types import AccreditationType, FormButton, AdminAccountChangeType, AdminFuncTypes
from config.settings import config_path


@allure.suite("Astanahub - Подача заявок")
class TestServiceRequest:
    config = configparser.ConfigParser()
    config.read(config_path)

    @allure.title("Подача заявки на Переоформление аккредитации ФЛ")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "email, password, expected_status, iin",
        [
            ("a.baisaganov@astanahub.com", "Pass1234!", 200, '990315351258')  # Валидный
        ],
        ids=["Валидный логин"]
    )
    @pytest.mark.skip("Решение проблемы с подписанием")
    def test_accreditation_renewal_fl(self, page, auth_page, admin, accreditation_page, email, password,
                                      expected_status, iin):
        accred_type = AccreditationType.RENEWAL_FL
        with allure.step("Подстановка ИИН пользователю"):
            user_id = admin.get_user_id_by_(email)
            admin.change_user(change_mode=AdminAccountChangeType.IIN,
                              data={'iin': iin},
                              user_id=user_id,
                              functinonality=AdminFuncTypes.CHANGE)

        with allure.step("Проверка: Нет ли активной заявки"):
            assert self.config['service_requests'][accred_type.value + '_id'] == '0', (f"{accred_type.value.capitalize()}"
                                                                                       f": Заявка уже создана")

        with allure.step("Переход на страницу авторизация"):
            auth_page.navigate()

        with allure.step("Ввод почты"):
            auth_page.input_email_or_phone(value=email)

        with allure.step("Клик по кнопке продолжить"):
            response = auth_page.click_auth_email_continue_btn()

            assert response is not None, "Ошибка при входе, пустой ответ"
            assert response.value.status == expected_status, f"Ошибка, неверный статус код: {response.value.status}"
            assert response.value.json()['user_exists'] is True, "Юзер отсутвует"

        with allure.step("Ввод пароля"):
            auth_page.input_password(password=password)

        with allure.step("Клик по кнопке продолжить"):
            auth_page.click_auth_continue_btn_2()

        with allure.step('Переход к форме заполнения заявки'):
            accreditation_page.nav_service_(accred_type)

        with allure.step('Заполнения заявки'):
            accreditation_page.fill_service_renewal_fl(
                cert_number=self.config['service_requests']['accreditation_fl_cert_number'])

        with allure.step('Сохранение заявки'):
            accreditation_page.save_and_submit_form(accred_type, FormButton.SAVE)

        with allure.step('Подписание заявки'):
            request_id = accreditation_page.save_and_submit_form(accred_type, FormButton.ECP_SUBMIT)

        with allure.step('Сохранение ID заявки в конфиг'):
            save = accreditation_page.save_service_id(service_name=accred_type.value + "_id",
                                                      service_id=request_id)

        assert save is None, save

    @allure.title("Подача заявки на Переоформление аккредитации ЮЛ")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "email, password, expected_status, iin",
        [
            ("a.baisaganov@astanahub.com", "Pass1234!", 200, '990315351258')  # Валидный
        ],
        ids=["Валидный логин"]
    )
    @pytest.mark.skip("Решение проблемы с подписанием")
    def test_accreditation_renewal_ul(self, page, admin, auth_page, accreditation_page, email, password,
                                      expected_status, iin):
        accred_type = AccreditationType.RENEWAL_UL
        user_id = admin.get_user_id_by_(email)
        admin.change_user(
            change_mode=AdminAccountChangeType.IIN,
            data={'iin': iin},
            user_id=user_id,
            functinonality=AdminFuncTypes.CHANGE
        )

        with allure.step("Проверка: Нет ли активной заявки"):
            assert self.config['service_requests'][
                       accred_type.value + '_id'] == '0', f"{accred_type.value.capitalize()}: Заявка уже создана"

        with allure.step("Переход на страницу авторизация"):
            auth_page.navigate()

        with allure.step("Ввод почты"):
            auth_page.input_email_or_phone(value=email)

        with allure.step("Клик по кнопке продолжить"):
            response = auth_page.click_auth_email_continue_btn()

            assert response is not None, "Ошибка при входе, пустой ответ"
            assert response.value.status == expected_status, f"Ошибка, неверный статус код: {response.value.status}"
            assert response.value.json()['user_exists'] is True, "Юзер отсутвует"

        with allure.step("Ввод пароля"):
            auth_page.input_password(password=password)

        with allure.step("Клик по кнопке продолжить"):
            auth_page.click_auth_continue_btn_2()

        with allure.step('Переход к форме заполнения заявки'):
            accreditation_page.nav_service_(accred_type)

        with allure.step('Заполнения заявки'):
            accreditation_page.fill_service_renewal_ul(cert_number=
                                                       self.config['service_requests']['accreditation_ul_cert_number'])

        with allure.step('Сохранение заявки'):
            accreditation_page.save_and_submit_form(accred_type, FormButton.SAVE)

        with allure.step('Подписание заявки'):
            request_id = accreditation_page.save_and_submit_form(accred_type, FormButton.ECP_SUBMIT)

        with allure.step('Сохранение ID заявки в конфиг'):
            save = accreditation_page.save_service_id(service_name=accred_type.value + "_id",
                                                      service_id=request_id)

        assert save is None, save

    @allure.title("Подача заявки на Дубликат аккредитации ФЛ")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "email, password, iin, cert_number",
        [
            ("a.baisaganov@astanahub.com", "Pass1234!", '990315351258', '00003')
        ],
        ids=["Отправка заявки валид"]
    )
    @pytest.mark.skip("Решение проблемы с подписанием")
    def test_accreditation_dublicate_fl(self, page, auth_page, accreditation_page, email, password, iin, cert_number):
        accred_type = AccreditationType.DUBLICATE_FL

        with allure.step("Проверка: Нет ли активной заявки"):
            assert self.config['service_requests'][
                       accred_type.value + '_id'] == '0', f"{accred_type.value.capitalize()}: Заявка уже создана"

        with allure.step("Переход на страницу авторизация"):
            auth_page.navigate()

        with allure.step("Ввод почты"):
            auth_page.input_email_or_phone(value=email)

        with allure.step("Клик по кнопке продолжить"):
            response = auth_page.click_auth_email_continue_btn()

            assert response is not None, "Ошибка при входе, пустой ответ"
            assert response.value.status == 200, f"Ошибка, неверный статус код: {response.value.status}"
            assert response.value.json()['user_exists'] is True, "Юзер отсутвует"

        with allure.step("Ввод пароля"):
            auth_page.input_password(password=password)

        with allure.step("Клик по кнопке продолжить"):
            auth_page.click_auth_continue_btn_2()

        with allure.step('Переход к форме заполнения заявки'):
            accreditation_page.nav_service_(accred_type)

        with allure.step('Заполнение заявки на дубликат'):
            accreditation_page.fill_service_dublicate_fl(cert_number=cert_number, iin=iin)

        with allure.step('Сохранение заявки'):
            accreditation_page.save_and_submit_form(accred_type, FormButton.SAVE)

        with allure.step('Подписание заявки'):
            request_id = accreditation_page.save_and_submit_form(accred_type, FormButton.ECP_SUBMIT)

        with allure.step('Сохранение ID заявки в конфиг'):
            save = accreditation_page.save_service_id(service_name=accred_type.value + "_id",
                                                      service_id=request_id)

        assert save is None, save

    @allure.title("Подача заявки на Регистрацию участника (БП)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "email, password, iin",
        [
            ("a.baisaganov@astanahub.com", "Pass1234!", '990315351258')
        ],
        ids=["Отправка заявки валид"]
    )
    @pytest.mark.skip(reason='Недоработанный тест')
    def test_positive_business_plan(self, auth_page, admin, business_plan_page, email, password, iin):
        with allure.step("Добавление ИИН к аккаунту"):
            user_id = admin.get_user_id_by_(email)

            assert user_id is not None, "Регистрация участника: Юзера не существует"

            admin.change_user(
                change_mode=AdminAccountChangeType.IIN,
                data={'iin': iin},
                user_id=user_id,
                functinonality=AdminFuncTypes.CHANGE
            )

        with allure.step("Авторизация"):
            auth_page.navigate()
            auth_page.email_auth(email, password)

        with allure.step("Переход к форме заполнения"):
            business_plan_page.navigate()

        with allure.step("Заполнение таба 1"):
            business_plan_page.select_company()

        with allure.step("Сохранение"):
            business_plan_page.save()

        with allure.step("Переход к табу 2"):
            pass

        with allure.step("Заполнение таба 2"):
            pass

        with allure.step("Сохранение"):
            pass

        with allure.step("Проверка есть ли данные на прошлом табе"):
            pass

        with allure.step("Переход к табу 3"):
            pass

        with allure.step("Заполнение таба 3"):
            pass

        with allure.step("Сохранение"):
            pass

        with allure.step("Проверка есть ли данные на прошлом табе"):
            pass

        with allure.step("Переход к табу 4"):
            pass

        with allure.step("Заполнение таба 4"):
            pass

        with allure.step("Сохранение"):
            pass

        with allure.step("Проверка есть ли данные на прошлом табе"):
            pass

        with allure.step("Переход к табу 5"):
            pass

        with allure.step("Заполнение таба 5"):
            pass

        with allure.step("Сохранение"):
            pass

        with allure.step("Проверка есть ли данные на прошлых табах"):
            pass

        with allure.step("Переход к табу 6"):
            pass

        with allure.step("Заполнение таба 6"):
            pass

        with allure.step("Сохранение"):
            pass

        with allure.step("Проверка есть ли данные на прошлых табах"):
            pass

        with allure.step("Подписание"):
            pass

        with allure.step("Удаление заявки"):
            pass

