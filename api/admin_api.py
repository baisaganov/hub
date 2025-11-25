from enum import Enum
import requests
from bs4 import BeautifulSoup
import logging

from commons.types import AdminAccountChangeType, AdminFuncTypes
from config import config
from os import getenv
from dotenv import load_dotenv, find_dotenv

from typing import Any


class AdminAPI:
    load_dotenv(find_dotenv())
    USERNAME = getenv("AUTH_LOGIN")
    PASSWORD = getenv("AUTH_PASSWORD")
    log = logging.getLogger(__name__)  # Подхватываем логгер

    def __init__(self):
        self.session = self.__get_cookies()
        self.auth_session = self.auth_authorization()

    def auth_authorization(self):
        session = requests.Session()

        # 1. Получаем CSRF и cookies с GET-запроса на страницу входа
        login_page = session.get(f"{config.app.app_url}/s/auth/secretadmin/login/?next=/s/auth/secretadmin/")
        soup = BeautifulSoup(login_page.text, "html.parser")
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"}).get("value")

        # 2. Подготавливаем headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
            "Referer": f"{config.app.app_url}/s/auth/secretadmin/login/?next=/s/auth/secretadmin/",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": config.app.app_url,
        }

        # 3. Подготавливаем тело POST-запроса
        data = {
            "csrfmiddlewaretoken": csrf_token,
            "username": "a.baisaganov@astanahub.com",
            "password": "Pass1234!",
            "next": "/s/auth/secretadmin/",
            "active": "on"
        }

        # 4. Авторизация
        login_response = session.post(
            f"{config.app.app_url}/s/auth/secretadmin/login/?next=/s/auth/secretadmin/",
            data=data,
            headers=headers
        )

        self.log.info(f"POST статус авторизации auth: {login_response.status_code}")

        # # 5. Доступ к защищенной странице
        protected = session.get(f"{config.app.app_url}/s/auth/secretadmin/")
        self.log.info(f"Protected статус: {protected.status_code}")
        return session

    def __get_cookies(self):
        try:
            session = requests.Session()
            login_headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/138.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Referer": f"{config.app.app_url}/ru/s/auth/login/",
                "Origin": config.app.app_url,
                "Content-Type": "application/json"
            }

            login_payload = {
                "email": self.USERNAME,
                "password": self.PASSWORD
            }

            # Авторизация Techhub
            login_url = f"{config.app.app_url}/s/auth/api/v1/auth/email/"
            login_response = session.post(login_url, json=login_payload, headers=login_headers)

            self.log.info(f"Admin: Статус авторизации:{login_response.status_code}")

            if login_response.status_code != 200:
                self.log.error("Admin: Авторизация не удалась")
                raise

            return session
        except Exception as e:
            logging.error("Admin: Авторизация не удалась")
            raise

    def __get_parsed_data(self, data: BeautifulSoup):
        info = {'iin': data.find('input', id='id_iin'),
                'email': data.find('input', id='id_email'),
                'first_name': data.find('input', id='id_first_name'),
                'last_name': data.find('input', id='id_last_name'),
                'is_email_verified': data.find('input', id='id_email_verified'),
                'phone': data.find('input', id='id_phone'),
                'is_phone_checked': data.find('input', id='id_phone_verified'),
                'role': data.find('select', id='id_role'),
                'data': data.find('textarea', id='id_data'),
                'initial_data': data.find('input', id='initial-id_data'),
                'is_staff': data.find('input', id='id_is_staff'),
                'is_active': data.find('input', id='id_is_active'),
                'is_superuser': data.find('input', id='id_is_superuser'),
                'arm_permissions': data.find('textarea', id='id_arm_permissions'),
                'csrf_token': data.select_one("input[name=csrfmiddlewaretoken]")["value"]
                }
        return info

    def __get_company_payload(self, data: BeautifulSoup):
        info = {
            "csrfmiddlewaretoken": data.select_one("input[name=csrfmiddlewaretoken]")["value"],
            "games_data": data.find('textarea', id='id_games_data_textarea'),
            "initial-games_data": data.find('input', id='initial-id_games_data'),
            "author": data.find('input', id='id_author'),
            "tin": data.find('input', id='id_tin'),
            "name": data.find('input', id='id_name'),
            "short_name": data.find('input', id='id_short_name'),
            "city_phone": data.find('input', id='id_city_phone'),
            "company_type": data.find('select', id='id_company_type').find('option', selected=True)['value'],
            "status": data.find('select', id='id_status').find('option', selected=True)['value'],
            "tag_startup": data.find('textarea', id='id_tag_startup_textarea'),
            "tag_it_company": data.find('textarea', id='id_tag_it_company_textarea'),
            "tag_ts_member": data.find('textarea', id='id_tag_ts_member_textarea'),
            "tag_techpark": data.find('textarea', id='id_tag_techpark_textarea'),
            "tag_corp_partner": data.find('textarea', id='id_tag_corp_partner_textarea'),
            "tag_nii": data.find('textarea', id='id_tag_nii_textarea'),
            "tag_nedrouser": data.find('textarea', id='id_tag_nedrouser_textarea'),
            "verified": data.find('input', id='id_verified'),
            "search_field": data.find('textarea', id='id_search_field'),
            "basic_info": data.find('textarea', id='id_basic_info_textarea'),
            "initial-basic_info": data.find('input', id='initial-id_basic_info'),
            "links": data.find('textarea', id='id_links_textarea'),
            "initial-links": data.find('input', id='initial-id_links'),
            "expertise": data.find('textarea', id='id_expertise_textarea'),
            "initial-expertise": data.find('input', id='initial-id_expertise'),
            "fundraising": data.find('textarea', id='id_fundraising_textarea'),
            "initial-fundraising": data.find('input', id='initial-id_fundraising'),
            "investments": data.find('textarea', id='id_investments_textarea'),
            "initial-investments": data.find('input', id='initial-id_investments'),
            "revenues": data.find('textarea', id='id_revenues_textarea'),
            "initial-revenues": data.find('input', id='initial-id_revenues'),
            "adoption": data.find('textarea', id='id_adoption_textarea'),
            "initial-adoption": data.find('input', id='initial-id_adoption'),
            "company_files": data.find('textarea', id='id_company_files_textarea'),
            "initial-company_files": data.find('input', id='initial-id_company_files'),
            "questions": data.find('textarea', id='id_questions_textarea'),
            "initial-questions": data.find('input', id='initial-id_questions'),
            "visibility_settings": data.find('textarea', id='id_visibility_settings_textarea'),
            "initial-visibility_settings": data.find('input', id='initial-id_visibility_settings'),
            "product_link": data.find('input', id='id_product_link'),
            "_save": "Сохранить",
            "image": data.find('input', id='id_image')

        }

        return info

    def get_code(self, uuid: str) -> str | None:
        """
            Getting registration code by UUID
        """
        try:
            session = self.auth_session
            request = session.get(f"{config.app.app_url}/s/auth/secretadmin/core/activation/{uuid}/change/")
            soup = BeautifulSoup(request.text, "html.parser")
            status_code = request.status_code
            assert status_code == 200, 'AdminAPI: Страница получения кода не загрузилась'
            for i in soup.find_all('input'):
                if i['name'] == 'code':
                    return i['value']
        except Exception as e:
            self.log.error(f"AdminPage: Getting code error [{e}]")
            assert 1 == 0, f"AdminPage: Getting code error [{e}]"

    def delete_user_by_id(self, user_id, service='auth', counts=0):
        try:
            delete_url = (f'{config.app.app_url}/s/auth/secretadmin/core/user/{user_id}/delete/'
                          if service == 'auth' else f'{config.app.app_url}/secretadmin/account/user/{user_id}/delete/')
            session = self.auth_session if service == 'auth' else self.session
            response = session.get(delete_url)

            soup = BeautifulSoup(response.text, "html.parser")
            x = (soup.find("input", {"name": "csrfmiddlewaretoken"}))
            csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"}).get("value")

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
                "Referer": delete_url,
                "Origin": config.app.app_url,
                "Content-Type": "application/x-www-form-urlencoded"
            }

            data = {
                "csrfmiddlewaretoken": csrf_token,
                "post": "yes"
            }

            delete_response = session.post(delete_url, headers=headers, data=data)

            assert delete_response.status_code in [200, 302], (f'[{delete_response.status_code}] '
                                                               f'AdminAPI: Ошибка при удалении {delete_response.text}')

        except TypeError:
            assert 1 == 0, f'AdminAPI: Не удалось удалить юзера, пустой ответ'
        except AttributeError as e:
            if counts <= 1:
                self.delete_user_by_id(user_id=user_id, service='main', counts=counts+1)

    def change_user(self,
                    change_mode: AdminAccountChangeType,
                    data: dict,
                    user_id: int,
                    functinonality: AdminFuncTypes):
        """
        Смена учетных данных юзера (При смене почты или иин, если есть убирается у учетки который есть
        и ставится новые
        :param change_mode: Как будет проводиться поиск [inn ==  иин, email == Смена email, user_id == ID юзера]
        :param data: На что нужно поменять
        :param user_id: ID юзера у кого меняем
        :param functinonality: clear = Очищаем поле, change = Меняем у юзеров
        """
        self.log.info("Started")
        functinonality = functinonality.value
        # Поиск юзера в система с такими данными
        match change_mode:
            case AdminAccountChangeType.IIN:
                reserved_user_id = self.get_user_id_by_(data['iin'])
            case AdminAccountChangeType.EMAIL:
                reserved_user_id = self.get_user_id_by_(data['email'])
            case AdminAccountChangeType.USER_ID:
                reserved_user_id = user_id
            case _:
                raise ValueError(f"Неизвестный тип поиска: {change_mode}")

        url_old = f'{config.app.app_url}/s/auth/secretadmin/core/user/{reserved_user_id}/change/'  # Старый юзер
        url_new = f'{config.app.app_url}/s/auth/secretadmin/core/user/{user_id}/change/'           # Новый юзер

        sync_url_old = (f'{config.app.app_url}/s/auth/secretadmin/core/user/{reserved_user_id}/actions'
                        f'/sync_service_providers_action/')
        sync_url_new = (f'{config.app.app_url}/s/auth/secretadmin/core/user/{user_id}/actions'
                        f'/sync_service_providers_action/')

        self.log.info("Started")

        # Если юзер с такими данными уже есть, то меняем у него, а затем заполняем другого
        if reserved_user_id is not None and (reserved_user_id != user_id or functinonality == 'clear'):
            # 1. Получение данных о пользователе и смена
            session = self.auth_session
            edit_resp = session.get(url_old)

            assert edit_resp.status_code == 200, f'AdminPage: Данные о старом аккаунте не получены'
            soup: BeautifulSoup = BeautifulSoup(edit_resp.text, 'html.parser')
            parsed_dict = self.__get_parsed_data(soup)

            payload = {
                'iin': None if 'iin' in data.keys() else parsed_dict.get('iin').attrs.get('value'),
                'email': None if 'email' in data.keys() else parsed_dict.get('email').attrs.get('value'),
                'first_name': parsed_dict.get('first_name').attrs.get('value'),
                'last_name': parsed_dict.get('last_name').attrs.get('value'),
                'email_verified': 'on' if parsed_dict.get('is_email_verified').attrs.get('checked') == '' else None,
                'phone': parsed_dict.get('phone').attrs.get('value'),
                'phone_verified': 'on' if parsed_dict.get('is_phone_checked').attrs.get('checked') == '' else None,
                'role': parsed_dict.get('role').find('option', selected=True).attrs.get('value'),
                'data': parsed_dict.get('data').text[1::],
                'initial-data': parsed_dict.get('initial_data').attrs.get('value'),
                'is_staff': 'on' if parsed_dict.get('is_staff').attrs.get('checked') == '' else None,
                'is_active': 'on' if parsed_dict.get('is_active').attrs.get('checked') == '' else None,
                'is_superuser': 'on' if parsed_dict.get('is_superuser').attrs.get('checked') == '' else None,
                'arm_permissions': parsed_dict.get('arm_permissions').text[1::],
                '_save': "Сохранить",
                "csrfmiddlewaretoken": parsed_dict.get('csrf_token')
            }

            pdate_resp = session.post(url_old, data=payload)

            assert pdate_resp.status_code == 200, 'AdminAPI: Данные в старом аккаунте не обновлены'
            self.log.info("Смена данных")
            sync_user_info = session.get(sync_url_old)

            assert sync_user_info.status_code in [200, 302], 'AdminAPI: Данные в старом аккаунте не синх-ы'

        if functinonality == 'clear':
            return

        #  Обновление переданного юзера
        session = self.auth_session
        edit_resp = session.get(url_new)
        soup: BeautifulSoup = BeautifulSoup(edit_resp.text, 'html.parser')

        assert edit_resp.status_code == 200, 'AdminPage: Данные не получены'

        parsed_dict = self.__get_parsed_data(soup)
        payload = {
            'iin': data['iin'] if 'iin' in data.keys() else parsed_dict.get('iin').attrs.get('value'),
            'email': data['email'] if 'email' in data.keys() else parsed_dict.get('email').attrs.get('value'),
            'first_name': parsed_dict.get('first_name').attrs.get('value'),
            'last_name': parsed_dict.get('last_name').attrs.get('value'),
            'email_verified': 'on' if parsed_dict.get('is_email_verified').attrs.get('checked') == '' else None,
            # 'on',
            'phone': parsed_dict.get('phone').attrs.get('value'),
            'phone_verified': 'on' if parsed_dict.get('is_phone_checked').attrs.get('checked') == '' else None,
            'role': data['role'] if 'role' in data.keys()
            else parsed_dict.get('role').find('option', selected=True).attrs.get('value'),
            'data': parsed_dict.get('data').text[1::],
            'initial-data': parsed_dict.get('initial_data').attrs.get('value'),
            'is_staff': 'on' if parsed_dict.get('is_staff').attrs.get('checked') == '' else None,
            'is_active': 'on' if parsed_dict.get('is_active').attrs.get('checked') == '' else None,
            'is_superuser': 'on' if parsed_dict.get('is_superuser').attrs.get('checked') == '' else None,
            'arm_permissions': parsed_dict.get('arm_permissions').text[1::],
            '_save': 'Сохранить',
            "csrfmiddlewaretoken": parsed_dict.get('csrf_token')
        }

        pdate_resp = session.post(url_new, data=payload)

        assert pdate_resp.status_code == 200, f'AdminPage: Данные у юзера не обновлены user_id = {user_id}'

        sync_user_info = session.get(sync_url_new)

        assert sync_user_info.status_code in [200, 302], (f'AdminPage: Синхронизация у нового юзера не удалась '
                                                          f'user_id = {user_id}')

    def get_user_id_by_(self, value):
        """
        Получение ID юзера из админки
        :param value: Любое значение для поиска
        :return: ID найденного юзера
        """
        try:
            session = self.auth_session
            response = session.get(f'{config.app.app_url}/secretadmin/account/user/?q={value}')
            soup = BeautifulSoup(response.text, "html.parser")
            try:
                user_id = soup.find('th', class_='field-id')
            except Exception as e:
                return None
            return user_id if user_id is None else user_id.text
        except AttributeError as e:
            self.log.error(f"AdminAPI:[{value}] Get user id error NoneType: {e}")
            assert 1 == 0, f"AdminAPI:[{value}] Get user id error NoneType: {e}"

    def delete_service_by_id(self, request_id):
        try:
            delete_url = f'{config.app.app_url}/s/services/secretadmin/service/servicerequest/{request_id}/delete/'
            session = self.session

            response = session.get(delete_url)

            soup = BeautifulSoup(response.text, "html.parser")
            csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"}).get("value")

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
                "Referer": delete_url,
                "Origin": config.app.app_url,
                "Content-Type": "application/x-www-form-urlencoded"
            }

            data = {
                "csrfmiddlewaretoken": csrf_token,
                "post": "yes"
            }

            delete_response = session.post(delete_url, headers=headers, data=data)

            assert delete_response.status_code in [200, 302], f"AdminAPI: Ошибка при удалении {delete_response.text}"
        except Exception as e:
            self.log.error(f"AdminPage: Не удалось удалить заявку, возникла ошибка {e}")
            assert 1 == 0, "AdminPage: Не удалось удалить заявку, возникла ошибка"

    def company_update(self, company_id, data: dict[str, Any]):
        session = self.session
        request = session.get(f"{config.app.app_url}/secretadmin/account/company/{company_id}/change/")
        soup = BeautifulSoup(request.text, 'html.parser')
        original_payload = self.__get_company_payload(soup)

        payload = {
            "csrfmiddlewaretoken": original_payload['csrfmiddlewaretoken'],
            "games_data": original_payload['games_data'].text,
            "initial-games_data": original_payload['initial-games_data'].attrs.get('value'),
            "author": original_payload['author'].attrs.get('value'),
            "tin": original_payload['tin'].attrs.get('value'),
            "name": original_payload['name'].attrs.get('value'),
            "short_name": original_payload['short_name'].attrs.get('value'),
            "city_phone": original_payload['city_phone'].attrs.get('value'),
            "company_type": original_payload['company_type'],
            "status": 'on' if original_payload['status'] == 'active' else None,
            "tag_startup": original_payload['tag_startup'].text,
            "tag_it_company": original_payload['tag_it_company'].text,
            "tag_ts_member": original_payload['tag_ts_member'].text,
            "tag_techpark": original_payload['tag_techpark'].text,
            "tag_corp_partner": original_payload['tag_corp_partner'].text,
            "tag_nii": data['tag_nii'] if 'tag_nii' in data.keys() else original_payload['tag_nii'].text[1::],
            "tag_nedrouser": original_payload['tag_nedrouser'].text,
            "verified": original_payload['verified'].attrs.get('value'),
            "search_field": original_payload['search_field'].text[1::],
            "basic_info": original_payload['basic_info'].text,
            "initial-basic_info": original_payload['initial-basic_info'].attrs.get('value'),
            "links": original_payload['links'].text,
            "initial-links": original_payload['initial-links'].attrs.get('value'),
            "expertise": original_payload['expertise'].text,
            "initial-expertise": original_payload['initial-expertise'].attrs.get('value'),
            "fundraising": original_payload['fundraising'].text,
            "initial-fundraising": original_payload['initial-fundraising'].attrs.get('value'),
            "investments": original_payload['investments'].text,
            "initial-investments": original_payload['initial-investments'].attrs.get('value'),
            "revenues": original_payload['revenues'].text,
            "initial-revenues": original_payload['initial-revenues'].attrs.get('value'),
            "adoption": original_payload['adoption'].text,
            "initial-adoption": original_payload['initial-adoption'].attrs.get('value'),
            "company_files": original_payload['company_files'].text,
            "initial-company_files": original_payload['initial-company_files'].attrs.get('value'),
            "questions": original_payload['questions'].text,
            "initial-questions": original_payload['initial-questions'].attrs.get('value'),
            "visibility_settings": original_payload['visibility_settings'].text,
            "initial-visibility_settings": original_payload['initial-visibility_settings'].attrs.get('value'),
            "product_link": original_payload['product_link'].attrs.get('value'),
            "_save": "Сохранить",
            "image": original_payload['image'].attrs.get('value'),
        }

        # files = {
        #     "profile_cover": ('', b'', 'application/octet-stream')
        # }
        #
        # session = self.__get_cookies()
        # request = session.post(f"https://dev.astanahub.com/secretadmin/account/company/{company_id}/change/",
        #                        data=payload, files=files)

        assert request.status_code in [200, 302], 'AdminAPI: Обновление компании не удалось'
        self.log.info('AdminAPI: Компания обновлена')


if __name__ == '__main__':
    adm = AdminAPI()
    d = {'iin': '990315351258'}
    # d = {'iin': '010805550740'}
    # d = {'iin': '030909650657'}
    adm.change_user(AdminAccountChangeType.IIN, data=d, user_id=60071, functinonality=AdminFuncTypes.CHANGE)


    # adm.delete_user_by_id(60143)
    # d = {'tag_nii': {}}
    # adm.company_update(6874, data=d)


# accreditation_department_head	    ruk_upr@acred.kz	    60071
# accreditation_deputy_chairman	    zam_pred@acred.kz	    60070
# accreditation_executor	        otv_ispolnitel@acred.kz	60072
# accreditation_chairman	        predsedatel@acred.hub	60093
# 1. Председатель комитета назначает на Рук. упр.
# 2. Рук. упр. назначает ответсвенного исполнителя
# 3. Отв. исполнитель формирует акт экспертизы на выдачу
# 4. Рук. упр. подписывает акт
# 5. Отв. исполнитель формирует приказ о переоформлении и подписывает
# 6. Рук. упр. подписывает приказ
# 7. Зам. пред. подписывает приказ
# 8. Председатель подписывает приказ