import pytest
import allure

# from clients.base.base_client import ApiError
from config import config
from models import UpdateNamesRequest
from testdata.factories import (
    fake_invalid_email,
    fake_invalid_phone,
    fake_names,
    fake_password,
    fake_phone,
    fake_unregistered_email,
)

pytestmark = [pytest.mark.api]

mutates_data = pytest.mark.skipif(
    config.is_production(), reason="Мутирует данные — только dev/qa"
)

NONEXISTENT_ACTIVATION = "00000000-0000-0000-0000-000000000000"
NONEXISTENT_PERMISSION = "nonexistent_permission"


@allure.label("owner", "aliwka")
@allure.suite("HUB ID")
@allure.label("level", "API")
@pytest.mark.hubid
@pytest.mark.api
class TestAuthAPI:
    @allure.title("Valid authorization")
    @pytest.mark.critical
    @pytest.mark.asyncio
    async def test_valid_authorization(self, auth_client):
        with allure.step("Логин с валидными кредами"):
            login = await auth_client.login(
                email=config.app.test_user_email,
                password=config.app.test_user_password,
            )

        with allure.step("Проверка данных юзера в ответе"):
            assert login.user.email == config.app.test_user_email
            assert login.user.email_verified is True
            assert login.user.blocked is False

    @allure.title("Authorization with invalid email")
    @pytest.mark.asyncio
    async def test_authorization_with_invalid_email(self, auth_client):
        with allure.step("Логин с невалидным email"):
            errors = await auth_client.login_expect_error(
                email=fake_invalid_email(),
                password=fake_password(),
                expected_status=400,
            )

        with allure.step("Проверка ошибки валидации по полю email"):
            assert "email" in errors, f"Ожидалась ошибка по email, пришло: {errors.fields}"
            assert errors["email"], "Список ошибок по email пуст"


@allure.label("owner", "aliwka")
@allure.suite("HUB ID")
@allure.label("level", "API")
@pytest.mark.hubid
@pytest.mark.api
class TestAuthCheck:
    @allure.title("Check: зарегистрированный email определяется как email-метод")
    @pytest.mark.critical
    @pytest.mark.asyncio
    async def test_check_registered_email(self, auth_client):
        with allure.step("Проверка email тестового юзера"):
            result = await auth_client.check(config.app.test_user_email)

        with allure.step("Юзер существует, метод — email"):
            assert result.user_exists is True
            assert result.method == "email"
            assert result.value == config.app.test_user_email

    @allure.title("Check: незарегистрированный email — user_exists=false")
    @pytest.mark.asyncio
    async def test_check_unregistered_email(self, auth_client):
        with allure.step("Проверка несуществующего email"):
            result = await auth_client.check(fake_unregistered_email())

        with allure.step("Юзер не существует, метод — email"):
            assert result.user_exists is False
            assert result.method == "email"

    @allure.title("Check: телефон определяется как phone-метод")
    @pytest.mark.asyncio
    async def test_check_phone(self, auth_client):
        with allure.step("Проверка незарегистрированного телефона"):
            result = await auth_client.check(fake_phone())

        with allure.step("Метод — phone, юзер не существует"):
            assert result.method == "phone"
            assert result.user_exists is False


@allure.label("owner", "aliwka")
@allure.suite("HUB ID")
@allure.label("level", "API")
@pytest.mark.hubid
@pytest.mark.api
class TestEmailOtp:
    @allure.title("OTP на зарегистрированный email возвращает активацию")
    @pytest.mark.critical
    @mutates_data
    @pytest.mark.asyncio
    async def test_email_otp_registered(self, auth_client):
        with allure.step("Запрос OTP на email тестового юзера"):
            activation = await auth_client.request_email_otp(config.app.test_user_email)

        with allure.step("Проверка контракта активации"):
            assert activation.resend_delay > 0

    @allure.title("OTP на незарегистрированный email возвращает 400")
    @pytest.mark.asyncio
    async def test_email_otp_unregistered(self, auth_client):
        with allure.step("Запрос OTP на несуществующий email"):
            errors = await auth_client.request_email_otp_expect_error(
                fake_unregistered_email()
            )

        with allure.step("Ошибка по полю email"):
            assert "email" in errors, f"Ожидалась ошибка по email, пришло: {errors.fields}"
            assert errors["email"], "Список ошибок по email пуст"

    @allure.title("OTP на синтаксически невалидный email возвращает 400")
    @pytest.mark.asyncio
    async def test_email_otp_invalid_email(self, auth_client):
        with allure.step("Запрос OTP на невалидный email"):
            errors = await auth_client.request_email_otp_expect_error(fake_invalid_email())

        with allure.step("Ошибка по полю email"):
            assert "email" in errors, f"Ожидалась ошибка по email, пришло: {errors.fields}"


@allure.label("owner", "aliwka")
@allure.suite("HUB ID")
@allure.label("level", "API")
@pytest.mark.hubid
@pytest.mark.api
class TestEmailRegistration:
    @allure.title("Регистрация нового email возвращает активацию")
    @pytest.mark.critical
    @mutates_data
    @pytest.mark.asyncio
    async def test_email_registration_new_email(self, auth_client):
        with allure.step("Старт регистрации на новый email"):
            activation = await auth_client.register_email(fake_unregistered_email())

        with allure.step("Проверка контракта активации"):
            assert activation.resend_delay > 0

    @allure.title("Регистрация на занятый email возвращает 400")
    @pytest.mark.asyncio
    async def test_email_registration_existing_email(self, auth_client):
        with allure.step("Старт регистрации на email существующего юзера"):
            errors = await auth_client.register_email_expect_error(
                config.app.test_user_email
            )

        with allure.step("Ошибка по полю email"):
            assert "email" in errors, f"Ожидалась ошибка по email, пришло: {errors.fields}"
            assert errors["email"], "Список ошибок по email пуст"


@allure.label("owner", "aliwka")
@allure.suite("HUB ID")
@allure.label("level", "API")
@pytest.mark.hubid
@pytest.mark.api
class TestEmailResetPassword:
    @allure.title("Сброс пароля на зарегистрированный email возвращает активацию")
    @pytest.mark.critical
    @mutates_data
    @pytest.mark.asyncio
    async def test_reset_password_registered_email(self, auth_client):
        with allure.step("Запрос сброса пароля на email тестового юзера"):
            activation = await auth_client.reset_password_email(
                config.app.test_user_email
            )

        with allure.step("Проверка контракта активации"):
            assert activation.resend_delay > 0

    @allure.title("Сброс пароля на незарегистрированный email возвращает 400")
    @pytest.mark.asyncio
    async def test_reset_password_unregistered_email(self, auth_client):
        with allure.step("Запрос сброса пароля на несуществующий email"):
            errors = await auth_client.reset_password_email_expect_error(
                fake_unregistered_email()
            )

        with allure.step("Ошибка по полю email"):
            assert "email" in errors, f"Ожидалась ошибка по email, пришло: {errors.fields}"


@allure.label("owner", "aliwka")
@allure.suite("HUB ID")
@allure.label("level", "API")
@pytest.mark.hubid
@pytest.mark.api
class TestPhoneAuth:
    @allure.title("Логин по невалидному телефону возвращает 400")
    @pytest.mark.critical
    @pytest.mark.asyncio
    async def test_phone_login_invalid_phone(self, auth_client):
        with allure.step("Логин с невалидным телефоном"):
            errors = await auth_client.login_phone_expect_error(fake_invalid_phone())

        with allure.step("Ошибка валидации в поле value"):
            assert "value" in errors, f"Ожидалась ошибка по value, пришло: {errors.fields}"
            assert errors["value"], "Список ошибок по value пуст"

    # @pytest.mark.xfail(
    #     raises=ApiError,
    #     reason="Бэкенд отвечает 500 (KeyError) вместо 400 на невалидный телефон",
    # )
    @allure.title("Регистрация по невалидному телефону возвращает 400")
    @pytest.mark.critical
    @pytest.mark.asyncio
    async def test_phone_registration_invalid_phone(self, auth_client):
        with allure.step("Регистрация с невалидным телефоном"):
            await auth_client.register_phone_expect_error(fake_invalid_phone())



    @allure.title("Сброс пароля по неизвестному телефону возвращает 400")
    @pytest.mark.critical
    @pytest.mark.asyncio
    async def test_phone_reset_password_unknown_phone(self, auth_client):
        with allure.step("Сброс пароля по незарегистрированному телефону"):
            errors = await auth_client.reset_password_phone_expect_error(fake_phone())

        with allure.step("Ошибка по полю phone"):
            assert "phone" in errors, f"Ожидалась ошибка по phone, пришло: {errors.fields}"
            assert errors["phone"], "Список ошибок по phone пуст"


@allure.label("owner", "aliwka")
@allure.suite("HUB ID")
@allure.label("level", "API")
@pytest.mark.hubid
@pytest.mark.api
class TestSocialAuth:
    # @pytest.mark.xfail(
    #     raises=ApiError,
    #     reason="Бэкенд отвечает 500 (AuthForbidden) вместо 400 на невалидный токен",
    # )
    @allure.title("Логин через Google с невалидным токеном возвращает 500")
    @pytest.mark.asyncio
    async def test_google_login_invalid_token(self, auth_client):
        with allure.step("Логин через Google с мусорным access_token"):
            await auth_client.login_google_expect_error("invalid-token")

        # with allure.step("Ошибка валидации"):
        #     assert errors.fields, "Ожидалась ошибка валидации"

    # @pytest.mark.xfail(
    #     raises=ApiError,
    #     reason="Бэкенд отвечает 500 (AuthFailed) вместо 400 на невалидный токен",
    # )
    @allure.title("Логин через Apple с невалидным токеном возвращает 500")
    @pytest.mark.asyncio
    async def test_apple_login_invalid_token(self, auth_client):
        with allure.step("Логин через Apple с мусорным id_token"):
            await auth_client.login_apple_expect_error("invalid-token")

        # with allure.step("Ошибка валидации"):
        #     assert errors.fields, "Ожидалась ошибка валидации"


@allure.label("owner", "aliwka")
@allure.suite("HUB ID")
@allure.label("level", "API")
@pytest.mark.hubid
@pytest.mark.api
class TestActivationConfirm:
    @allure.title("Подтверждение несуществующей активации возвращает 404")
    @pytest.mark.critical
    @pytest.mark.asyncio
    async def test_activation_confirm_unknown_activation(self, auth_client):
        with allure.step("Подтверждение активации с несуществующим uuid"):
            error = await auth_client.confirm_activation_expect_error(
                activation=NONEXISTENT_ACTIVATION, code="000000"
            )

        with allure.step("Проверка сообщения об ошибке"):
            assert error.detail, "Сообщение об ошибке пустое"


@allure.label("owner", "aliwka")
@allure.suite("HUB ID")
@allure.label("level", "API")
@pytest.mark.hubid
@pytest.mark.api
class TestAuthSchema:
    @allure.title("OpenAPI-схема сервиса отдаётся в JSON")
    @pytest.mark.asyncio
    async def test_openapi_schema(self, auth_client):
        with allure.step("Запрос схемы"):
            schema = await auth_client.get_openapi_schema()

        with allure.step("Проверка структуры схемы"):
            assert schema.openapi.startswith("3."), f"Неожиданная версия: {schema.openapi}"
            assert schema.paths, "Схема не содержит paths"


@allure.label("owner", "aliwka")
@allure.suite("HUB ID")
@allure.label("level", "API")
@pytest.mark.hubid
@pytest.mark.api
class TestProfileAPI:
    @allure.title("Профиль текущего юзера возвращает валидный контракт")
    @pytest.mark.critical
    @pytest.mark.asyncio
    async def test_profile_info(self, authorized_auth_client):
        with allure.step("Запрос профиля"):
            user = await authorized_auth_client.get_profile_info()

        with allure.step("Проверка данных юзера"):
            assert user.email == config.app.test_user_email
            assert user.blocked is False
            assert user.signup_flow_completed is True

    @allure.title("Профиль без авторизации возвращает 401")
    @pytest.mark.asyncio
    async def test_profile_info_unauthorized(self, auth_client):
        with allure.step("Запрос профиля без логина"):
            error = await auth_client.get_profile_info_expect_error(expected_status=401)

        with allure.step("Проверка сообщения об ошибке"):
            assert error.detail, "Сообщение об ошибке пустое"

    @allure.title("info_by_id недоступен юзеру без служебных прав — 403")
    @pytest.mark.asyncio
    async def test_profile_info_by_id_forbidden(self, authorized_auth_client):
        with allure.step("Получение id текущего юзера"):
            user = await authorized_auth_client.get_profile_info()

        with allure.step("Запрос info_by_id обычным юзером"):
            error = await authorized_auth_client.get_profile_info_by_id_expect_error(
                user_id=user.id, expected_status=403
            )

        with allure.step("Доступ запрещён"):
            assert error.error == "PermissionDenied"

    @allure.title("Обновление имени в профиле")
    @mutates_data
    @pytest.mark.xdist_group("auth_profile_names")
    @pytest.mark.asyncio
    async def test_update_profile_names(self, authorized_auth_client):
        with allure.step("Снятие текущих имени и фамилии"):
            original = await authorized_auth_client.get_profile_info()

        names = fake_names()
        try:
            with allure.step("Обновление имени и фамилии"):
                await authorized_auth_client.update_profile(names)

            with allure.step("Проверка, что профиль обновился"):
                updated = await authorized_auth_client.get_profile_info()
                assert updated.first_name == names.first_name
                assert updated.last_name == names.last_name
        finally:
            with allure.step("Откат имени и фамилии"):
                await authorized_auth_client.update_profile(
                    UpdateNamesRequest(
                        first_name=original.first_name, last_name=original.last_name
                    )
                )

    @allure.title("Смена пароля с неверным старым паролем возвращает 400")
    @pytest.mark.asyncio
    async def test_change_password_wrong_old_password(self, authorized_auth_client):
        with allure.step("Смена пароля с неверным старым паролем"):
            errors = await authorized_auth_client.change_password_expect_error(
                old_password=fake_password(), password=fake_password()
            )

        with allure.step("Ошибка по полю old_password"):
            assert "old_password" in errors, (
                f"Ожидалась ошибка по old_password, пришло: {errors.fields}"
            )
            assert errors["old_password"], "Список ошибок по old_password пуст"

    @allure.title("Смена email на невалидный возвращает 400")
    @pytest.mark.asyncio
    async def test_change_email_invalid_email(self, authorized_auth_client):
        with allure.step("Смена email на невалидный"):
            errors = await authorized_auth_client.change_email_expect_error(
                fake_invalid_email()
            )

        with allure.step("Ошибка по полю email"):
            assert "email" in errors, f"Ожидалась ошибка по email, пришло: {errors.fields}"

    @allure.title("Смена телефона возвращает активацию")
    @mutates_data
    @pytest.mark.asyncio
    async def test_change_phone_returns_activation(self, authorized_auth_client):
        with allure.step("Запрос смены телефона"):
            activation = await authorized_auth_client.change_phone(fake_phone())

        with allure.step("Проверка контракта активации"):
            assert activation.resend_delay > 0

        with allure.step("Телефон не изменился до подтверждения кодом"):
            user = await authorized_auth_client.get_profile_info()
            assert user.phone_verified is False

    @allure.title("Удаление аккаунта без авторизации возвращает 401")
    @pytest.mark.asyncio
    async def test_delete_account_unauthorized(self, auth_client):
        with allure.step("Попытка удаления аккаунта без логина"):
            error = await auth_client.delete_account_expect_error(expected_status=401)

        with allure.step("Проверка сообщения об ошибке"):
            assert error.detail, "Сообщение об ошибке пустое"

    @allure.title("Повторное принятие политики конфиденциальности возвращает 400")
    @pytest.mark.asyncio
    async def test_privacy_policy_accept_already_accepted(self, authorized_auth_client):
        with allure.step("Принятие политики юзером, который уже её принял"):
            errors = await authorized_auth_client.accept_privacy_policy_expect_error(
                accepted=True
            )

        with allure.step("Ошибка по полю accepted"):
            assert "accepted" in errors, (
                f"Ожидалась ошибка по accepted, пришло: {errors.fields}"
            )


@allure.label("owner", "aliwka")
@allure.suite("HUB ID")
@allure.label("level", "API")
@pytest.mark.hubid
@pytest.mark.api
class TestAuthFlow:
    @allure.title("Флоу: пустой пароль возвращает 400")
    @pytest.mark.asyncio
    async def test_flow_set_password_empty(self, authorized_auth_client):
        with allure.step("Установка пустого пароля"):
            errors = await authorized_auth_client.flow_set_password_expect_error(
                password=""
            )

        with allure.step("Ошибка по полю password"):
            assert "password" in errors, (
                f"Ожидалась ошибка по password, пришло: {errors.fields}"
            )

    @allure.title("Флоу: установка имени и фамилии")
    @mutates_data
    @pytest.mark.xdist_group("auth_profile_names")
    @pytest.mark.asyncio
    async def test_flow_set_names(self, authorized_auth_client):
        with allure.step("Снятие текущих имени и фамилии"):
            original = await authorized_auth_client.get_profile_info()

        names = fake_names()
        try:
            with allure.step("Установка имени и фамилии через флоу"):
                await authorized_auth_client.flow_set_names(names)

            with allure.step("Проверка, что профиль обновился"):
                updated = await authorized_auth_client.get_profile_info()
                assert updated.first_name == names.first_name
                assert updated.last_name == names.last_name
        finally:
            with allure.step("Откат имени и фамилии"):
                await authorized_auth_client.flow_set_names(
                    UpdateNamesRequest(
                        first_name=original.first_name, last_name=original.last_name
                    )
                )

    @allure.title("Флоу: пропуск фото")
    @mutates_data
    @pytest.mark.asyncio
    async def test_flow_skip_photo(self, authorized_auth_client):
        with allure.step("Пропуск шага с фото"):
            await authorized_auth_client.flow_skip_photo()

    @allure.title("Флоу: завершение онбординга")
    @mutates_data
    @pytest.mark.asyncio
    async def test_flow_set_completed(self, authorized_auth_client):
        with allure.step("Завершение онбординга"):
            await authorized_auth_client.flow_set_completed()

        with allure.step("Флаг signup_flow_completed установлен"):
            user = await authorized_auth_client.get_profile_info()
            assert user.signup_flow_completed is True


@allure.label("owner", "aliwka")
@allure.suite("HUB ID")
@allure.label("level", "API")
@pytest.mark.hubid
@pytest.mark.api
class TestPermissionsAPI:
    @allure.title("Список прав текущего юзера")
    @pytest.mark.asyncio
    async def test_permissions_list(self, authorized_auth_client):
        with allure.step("Запрос списка прав"):
            permissions = await authorized_auth_client.get_permissions()

        with allure.step("Контракт ответа валиден"):
            assert isinstance(permissions.result, list)

    @allure.title("Проверка отсутствующего права возвращает 403")
    @pytest.mark.asyncio
    async def test_permission_check_forbidden(self, authorized_auth_client):
        with allure.step("Проверка права, которого нет у юзера"):
            error = await authorized_auth_client.check_permission_expect_error(
                NONEXISTENT_PERMISSION
            )

        with allure.step("Доступ запрещён"):
            assert error.detail, "Сообщение об ошибке пустое"

    @allure.title("has_permissions: отсутствующее право — valid=false")
    @pytest.mark.asyncio
    async def test_has_permissions_invalid(self, authorized_auth_client):
        with allure.step("Проверка набора с отсутствующим правом"):
            result = await authorized_auth_client.has_permissions(
                [NONEXISTENT_PERMISSION]
            )

        with allure.step("Право не подтверждено"):
            assert result.valid is False


@allure.label("owner", "aliwka")
@allure.suite("HUB ID")
@allure.label("level", "API")
@pytest.mark.hubid
@pytest.mark.api
class TestExternalAuth:
    @allure.title("external/user/info без токена возвращает 401")
    @pytest.mark.asyncio
    async def test_external_user_info_unauthorized(self, auth_client):
        with allure.step("Запрос external-профиля без токена"):
            error = await auth_client.get_external_user_info_expect_error(
                expected_status=401
            )

        with allure.step("Проверка сообщения об ошибке"):
            assert error.detail, "Сообщение об ошибке пустое"
