# Матрица покрытия API-автотестами

Сгенерирована из `api_schema/` (04.08.2026). Одна строка = один эндпоинт.

Статусы: ✅ прямой API-тест · 🔷 задет косвенно (UI) · ❌ не покрыт

Критичность (по правилам, уточнять точечно): critical — ядро auth,
деньги/заказы, создание ключевых сущностей; high — прочие мутации;
medium — чтение ключевых сущностей; low — справочники, АРМ, internal.

Набор: **smoke** — все critical-эндпоинты (короткий прогон на деплой,
входит в регресс); **regress** — остальное.

Среда: **все** — можно на прод (GET и безопасный POST логина);
**dev/qa** — мутирует данные.


## auth — Auth API (43)

| № | Метод | Эндпоинт | Статус | Тест | Критичность | Набор | Среда | Ответственный |
|---|---|---|---|---|---|---|---|---|
| 1 | GET | `/s/auth/api/schema/` | ✅ | `test_openapi_schema` | low | regress | все | aliwka |
| 2 | GET | `/s/auth/api/v1/alem-gpt/widget-token` | ❌ |  | low | regress | все | aliwka |
| 3 | POST | `/s/auth/api/v1/auth/activation_confirm/` | ✅ | `test_activation_confirm_unknown_activation` | critical | smoke | dev/qa | aliwka |
| 4 | POST | `/s/auth/api/v1/auth/apple/` | ✅ | `test_apple_login_invalid_token` (xfail: баг 500) | high | regress | dev/qa | aliwka |
| 5 | POST | `/s/auth/api/v1/auth/check/` | ✅ | `TestAuthCheck` (3) | critical | smoke | все | aliwka |
| 6 | GET | `/s/auth/api/v1/auth/egov_sign_uri/` | ❌ |  | low | regress | все | aliwka |
| 7 | GET | `/s/auth/api/v1/auth/egov_signature_check/{uuid}/` | ❌ |  | low | regress | все | aliwka |
| 8 | POST | `/s/auth/api/v1/auth/email/` | ✅ | `test_valid_authorization`, `test_authorization_with_invalid_email` | critical | smoke | все | aliwka |
| 9 | POST | `/s/auth/api/v1/auth/email_otp/` | ✅ | `TestEmailOtp` (3) | critical | smoke | dev/qa | aliwka |
| 10 | POST | `/s/auth/api/v1/auth/email_registration/` | ✅ | `TestEmailRegistration` (2) | critical | smoke | dev/qa | aliwka |
| 11 | POST | `/s/auth/api/v1/auth/email_reset_password/` | ✅ | `TestEmailResetPassword` (2) | critical | smoke | dev/qa | aliwka |
| 12 | POST | `/s/auth/api/v1/auth/google/` | ✅ | `test_google_login_invalid_token` (xfail: баг 500) | high | regress | dev/qa | aliwka |
| 13 | POST | `/s/auth/api/v1/auth/phone/` | ✅ | `test_phone_login_invalid_phone` | critical | smoke | все | aliwka |
| 14 | POST | `/s/auth/api/v1/auth/phone_registration/` | ✅ | `test_phone_registration_invalid_phone` (xfail: баг 500) | critical | smoke | dev/qa | aliwka |
| 15 | POST | `/s/auth/api/v1/auth/phone_reset_password/` | ✅ | `test_phone_reset_password_unknown_phone` | critical | smoke | dev/qa | aliwka |
| 16 | POST | `/s/auth/api/v1/auth/privacy_policy_accept/` | ✅ | `test_privacy_policy_accept_already_accepted` | high | regress | dev/qa | aliwka |
| 17 | POST | `/s/auth/api/v1/auth/signature/` | ❌ |  | high | regress | dev/qa | aliwka |
| 18 | GET | `/s/auth/api/v1/auth/signature_xml/` | ❌ |  | low | regress | все | aliwka |
| 19 | GET | `/s/auth/api/v1/auth/{id}/egov_info/{uuid_param}/` | ❌ |  | low | regress | все | aliwka |
| 20 | GET | `/s/auth/api/v1/auth/{id}/egov_sign/{uuid_param}/` | ❌ |  | low | regress | все | aliwka |
| 21 | PUT | `/s/auth/api/v1/auth/{id}/egov_sign/{uuid_param}/` | ❌ |  | high | regress | dev/qa | aliwka |
| 22 | GET | `/s/auth/api/v1/auth/{id}/mgovSign/egov_info/{uuid_param}/` | ❌ |  | low | regress | все | aliwka |
| 23 | GET | `/s/auth/api/v1/external/token/exchange/` | ❌ |  | low | regress | все | aliwka |
| 24 | GET | `/s/auth/api/v1/external/user/info/` | ✅ | `test_external_user_info_unauthorized` | medium | regress | все | aliwka |
| 25 | POST | `/s/auth/api/v1/flow/set_community_role/` | ❌ |  | high | regress | dev/qa | aliwka |
| 26 | POST | `/s/auth/api/v1/flow/set_completed/` | ✅ | `test_flow_set_completed` | high | regress | dev/qa | aliwka |
| 27 | POST | `/s/auth/api/v1/flow/set_names/` | ✅ | `test_flow_set_names` | high | regress | dev/qa | aliwka |
| 28 | POST | `/s/auth/api/v1/flow/set_password/` | ✅ | `test_flow_set_password_empty` | high | regress | dev/qa | aliwka |
| 29 | POST | `/s/auth/api/v1/flow/set_photo/` | ✅ | `test_flow_skip_photo` | high | regress | dev/qa | aliwka |
| 30 | POST | `/s/auth/api/v1/has_permissions/` | ✅ | `test_has_permissions_invalid` | high | regress | dev/qa | aliwka |
| 31 | POST | `/s/auth/api/v1/internal/user/` | ❌ |  | low | regress | dev/qa | — |
| 32 | POST | `/s/auth/api/v1/internal/user/attach_iin/` | ❌ |  | low | regress | dev/qa | — |
| 33 | POST | `/s/auth/api/v1/internal/verify/` | ❌ |  | low | regress | dev/qa | — |
| 34 | GET | `/s/auth/api/v1/permissions/` | ✅ | `test_permissions_list` | low | regress | все | aliwka |
| 35 | GET | `/s/auth/api/v1/permissions/check/{permission}/` | ✅ | `test_permission_check_forbidden` | low | regress | все | aliwka |
| 36 | POST | `/s/auth/api/v1/profile/change_email/` | ✅ | `test_change_email_invalid_email` | high | regress | dev/qa | aliwka |
| 37 | POST | `/s/auth/api/v1/profile/change_password/` | ✅ | `test_change_password_wrong_old_password` | high | regress | dev/qa | aliwka |
| 38 | POST | `/s/auth/api/v1/profile/change_phone/` | ✅ | `test_change_phone_returns_activation` | high | regress | dev/qa | aliwka |
| 39 | POST | `/s/auth/api/v1/profile/delete_account/` | ✅ | `test_delete_account_unauthorized` | high | regress | dev/qa | aliwka |
| 40 | GET | `/s/auth/api/v1/profile/info/` | ✅ | `test_profile_info`, `test_profile_info_unauthorized` | low | regress | все | aliwka |
| 41 | GET | `/s/auth/api/v1/profile/info_by_id/` | ✅ | `test_profile_info_by_id_forbidden` | low | regress | все | aliwka |
| 42 | POST | `/s/auth/api/v1/profile/update_profile/` | ✅ | `test_update_profile_names` | high | regress | dev/qa | aliwka |
| 43 | POST | `/s/auth/api/v1/profile/verify/` | ❌ |  | high | regress | dev/qa | aliwka |

## techhub — публичное API (70)

| № | Метод | Эндпоинт | Статус | Тест | Критичность | Набор | Среда | Ответственный |
|---|---|---|---|---|---|---|---|---|
| 44 | GET | `/api/article/` | ❌ |  | medium | regress | все | madina |
| 45 | GET | `/api/article/{id}/` | ❌ |  | medium | regress | все | madina |
| 46 | GET | `/api/article/{id}/favorite_add/` | ❌ |  | medium | regress | все | madina |
| 47 | GET | `/api/article/{id}/favorite_remove/` | ❌ |  | medium | regress | все | madina |
| 48 | GET | `/api/article/{id}/reaction_down/` | ❌ |  | medium | regress | все | madina |
| 49 | GET | `/api/article/{id}/reaction_up/` | ❌ |  | medium | regress | все | madina |
| 50 | GET | `/api/blog-v2/` | ❌ |  | medium | regress | все | madina |
| 51 | GET | `/api/blog-v2/{id}/` | ❌ |  | medium | regress | все | madina |
| 52 | GET | `/api/blog/` | ❌ |  | medium | regress | все | madina |
| 53 | GET | `/api/blog/{id}/` | ❌ |  | medium | regress | все | madina |
| 54 | GET | `/api/blog/{id}/favorite_add/` | ❌ |  | medium | regress | все | madina |
| 55 | GET | `/api/blog/{id}/favorite_remove/` | ❌ |  | medium | regress | все | madina |
| 56 | GET | `/api/blog/{id}/reaction_down/` | ❌ |  | medium | regress | все | madina |
| 57 | GET | `/api/blog/{id}/reaction_up/` | ❌ |  | medium | regress | все | madina |
| 58 | GET | `/api/category/` | ❌ |  | low | regress | все | aliwka |
| 59 | GET | `/api/category/{id}/` | ❌ |  | low | regress | все | aliwka |
| 60 | GET | `/api/category/{id}/follow/` | ❌ |  | low | regress | все | aliwka |
| 61 | GET | `/api/category/{id}/top_authors/` | ❌ |  | low | regress | все | aliwka |
| 62 | GET | `/api/category/{id}/unfollow/` | ❌ |  | low | regress | все | aliwka |
| 63 | GET | `/api/city/` | ❌ |  | low | regress | все | aliwka |
| 64 | GET | `/api/city/{id}/` | ❌ |  | low | regress | все | aliwka |
| 65 | GET | `/api/comment/` | ❌ |  | low | regress | все | madina |
| 66 | POST | `/api/comment/` | ❌ |  | high | regress | dev/qa | madina |
| 67 | GET | `/api/comment/{id}/` | ❌ |  | low | regress | все | madina |
| 68 | PUT | `/api/comment/{id}/` | ❌ |  | high | regress | dev/qa | madina |
| 69 | PATCH | `/api/comment/{id}/` | ❌ |  | high | regress | dev/qa | madina |
| 70 | GET | `/api/comment/{id}/delete/` | ❌ |  | low | regress | все | madina |
| 71 | GET | `/api/comment/{id}/reaction_down/` | ❌ |  | low | regress | все | madina |
| 72 | GET | `/api/comment/{id}/reaction_up/` | ❌ |  | low | regress | все | madina |
| 73 | GET | `/api/discussion/` | ❌ |  | low | regress | все | madina |
| 74 | GET | `/api/discussion/{id}/` | ❌ |  | low | regress | все | madina |
| 75 | GET | `/api/discussion/{id}/favorite_add/` | ❌ |  | low | regress | все | madina |
| 76 | GET | `/api/discussion/{id}/favorite_remove/` | ❌ |  | low | regress | все | madina |
| 77 | GET | `/api/discussion/{id}/reaction_down/` | ❌ |  | low | regress | все | madina |
| 78 | GET | `/api/discussion/{id}/reaction_up/` | ❌ |  | low | regress | все | madina |
| 79 | POST | `/api/elabs-document/{id}/generate_pdf/` | ❌ |  | high | regress | dev/qa | aliwka |
| 80 | GET | `/api/event/` | ✅ | `test_events_list_active_true` | medium | regress | все | madina |
| 81 | GET | `/api/event/slug/{slug}/` | ❌ |  | medium | regress | все | madina |
| 82 | GET | `/api/event/{id}/` | ❌ |  | medium | regress | все | madina |
| 83 | GET | `/api/event/{id}/favorite_add/` | ❌ |  | medium | regress | все | madina |
| 84 | GET | `/api/event/{id}/favorite_remove/` | ❌ |  | medium | regress | все | madina |
| 85 | GET | `/api/event/{id}/qr/` | ❌ |  | medium | regress | все | madina |
| 86 | GET | `/api/event/{id}/qrcode/` | ❌ |  | medium | regress | все | madina |
| 87 | GET | `/api/feed/` | ❌ |  | medium | regress | все | madina |
| 88 | GET | `/api/feed/{id}/` | ❌ |  | medium | regress | все | madina |
| 89 | GET | `/api/games/badge_info_v2/` | ❌ |  | low | regress | все | madina |
| 90 | GET | `/api/games/history/` | ❌ |  | low | regress | все | madina |
| 91 | GET | `/api/games/players/rating/` | ❌ |  | low | regress | все | madina |
| 92 | GET | `/api/innovation-infrastructure-v2/` | ❌ |  | low | regress | все | frederick |
| 93 | GET | `/api/innovation-infrastructure-v2/{id}/` | ❌ |  | low | regress | все | frederick |
| 94 | GET | `/api/innovation-infrastructure/` | ❌ |  | low | regress | все | frederick |
| 95 | GET | `/api/innovation-infrastructure/{id}/` | ❌ |  | low | regress | все | frederick |
| 96 | POST | `/api/nps-result/` | ❌ |  | high | regress | dev/qa | aliwka |
| 97 | POST | `/api/nps-result/dismiss/` | ❌ |  | high | regress | dev/qa | aliwka |
| 98 | GET | `/api/project-registry/` | ❌ |  | low | regress | все | aliwka |
| 99 | GET | `/api/project-registry/context/gov_body/` | ❌ |  | low | regress | все | aliwka |
| 100 | GET | `/api/project-registry/context/industry/` | ❌ |  | low | regress | все | aliwka |
| 101 | GET | `/api/project-registry/context/status/` | ❌ |  | low | regress | все | aliwka |
| 102 | GET | `/api/project-registry/{id}/` | ❌ |  | low | regress | все | aliwka |
| 103 | GET | `/api/schema/` | ❌ |  | low | regress | все | aliwka |
| 104 | GET | `/api/tech_task/` | ❌ |  | medium | regress | все | aidar |
| 105 | GET | `/api/tech_task/{id}/` | ❌ |  | medium | regress | все | aidar |
| 106 | GET | `/api/tech_task/{id}/favorite_add/` | ❌ |  | medium | regress | все | aidar |
| 107 | GET | `/api/tech_task/{id}/favorite_remove/` | ❌ |  | medium | regress | все | aidar |
| 108 | GET | `/api/user/{id}/education_experience/` | ❌ |  | medium | regress | все | frederick |
| 109 | GET | `/api/vacancy/` | ❌ |  | medium | regress | все | aidar |
| 110 | GET | `/api/vacancy/context/` | ❌ |  | medium | regress | все | aidar |
| 111 | GET | `/api/vacancy/{id}/` | ❌ |  | medium | regress | все | aidar |
| 112 | GET | `/api/vacancy/{id}/favorite_add/` | ❌ |  | medium | regress | все | aidar |
| 113 | GET | `/api/vacancy/{id}/favorite_remove/` | ❌ |  | medium | regress | все | aidar |

## techhub — кабинет (/account/api/) (199)

| № | Метод | Эндпоинт | Статус | Тест | Критичность | Набор | Среда | Ответственный |
|---|---|---|---|---|---|---|---|---|
| 114 | GET | `/account/api/action_log/` | ❌ |  | low | regress | все | aliwka |
| 115 | GET | `/account/api/action_log/{id}/` | ❌ |  | low | regress | все | aliwka |
| 116 | PUT | `/account/api/application_form/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 117 | PATCH | `/account/api/application_form/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 118 | PATCH | `/account/api/application_form/{id}/decline_application_form/` | ❌ |  | high | regress | dev/qa | frederick |
| 119 | PATCH | `/account/api/application_form/{id}/miss_round/` | ❌ |  | high | regress | dev/qa | frederick |
| 120 | POST | `/account/api/article/` | ❌ |  | high | regress | dev/qa | madina |
| 121 | PUT | `/account/api/article/{id}/` | ❌ |  | high | regress | dev/qa | madina |
| 122 | PATCH | `/account/api/article/{id}/` | ❌ |  | high | regress | dev/qa | madina |
| 123 | GET | `/account/api/article/{id}/delete/` | ❌ |  | medium | regress | все | madina |
| 124 | GET | `/account/api/article/{id}/send/` | ❌ |  | medium | regress | все | madina |
| 125 | POST | `/account/api/blog/` | ❌ |  | high | regress | dev/qa | madina |
| 126 | PUT | `/account/api/blog/{id}/` | ❌ |  | high | regress | dev/qa | madina |
| 127 | PATCH | `/account/api/blog/{id}/` | ❌ |  | high | regress | dev/qa | madina |
| 128 | GET | `/account/api/blog/{id}/delete/` | ❌ |  | medium | regress | все | madina |
| 129 | GET | `/account/api/blog/{id}/send/` | ❌ |  | medium | regress | все | madina |
| 130 | POST | `/account/api/booking/` | ❌ |  | high | regress | dev/qa | frederick |
| 131 | GET | `/account/api/booking/validate_user/` | ❌ |  | medium | regress | все | frederick |
| 132 | PUT | `/account/api/booking/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 133 | PATCH | `/account/api/booking/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 134 | GET | `/account/api/booking/{id}/deactivate/` | ❌ |  | low | regress | все | frederick |
| 135 | POST | `/account/api/booking/{id}/finish_early/` | ❌ |  | high | regress | dev/qa | frederick |
| 136 | GET | `/account/api/bug-report/` | ❌ |  | low | regress | все | aliwka |
| 137 | POST | `/account/api/bug-report/` | ❌ |  | high | regress | dev/qa | aliwka |
| 138 | GET | `/account/api/bug-report/{id}/` | ❌ |  | low | regress | все | aliwka |
| 139 | GET | `/account/api/company/{id}/` | ❌ |  | medium | regress | все | frederick |
| 140 | GET | `/account/api/company_api/` | 🔷 | UI `test_create_company` | medium | regress | все | frederick |
| 141 | POST | `/account/api/company_api/` | 🔷 | UI `test_create_company` | critical | smoke | dev/qa | frederick |
| 142 | POST | `/account/api/company_api/add/` | ❌ |  | high | regress | dev/qa | frederick |
| 143 | GET | `/account/api/company_api/egov_company_info/{user_pk}/{uuid_param}/` | ❌ |  | medium | regress | все | frederick |
| 144 | GET | `/account/api/company_api/egov_company_sign/{user_pk}/{uuid_param}/` | ❌ |  | medium | regress | все | frederick |
| 145 | PUT | `/account/api/company_api/egov_company_sign/{user_pk}/{uuid_param}/` | ❌ |  | high | regress | dev/qa | frederick |
| 146 | GET | `/account/api/company_api/egov_company_sign_check/{uuid_param}/` | ❌ |  | medium | regress | все | frederick |
| 147 | GET | `/account/api/company_api/egov_company_sign_uri/` | ❌ |  | medium | regress | все | frederick |
| 148 | POST | `/account/api/company_api/signature_create/` | ❌ |  | high | regress | dev/qa | frederick |
| 149 | GET | `/account/api/company_api/{id}/` | ❌ |  | medium | regress | все | frederick |
| 150 | PUT | `/account/api/company_api/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 151 | POST | `/account/api/company_api/{id}/delete_user_company/` | ❌ |  | high | regress | dev/qa | frederick |
| 152 | GET | `/account/api/company_api/{id}/follow/` | ❌ |  | medium | regress | все | frederick |
| 153 | GET | `/account/api/company_api/{id}/get_tag_data/` | ❌ |  | medium | regress | все | frederick |
| 154 | POST | `/account/api/company_api/{id}/invite_users/` | ❌ |  | high | regress | dev/qa | frederick |
| 155 | POST | `/account/api/company_api/{id}/set_author/` | ❌ |  | high | regress | dev/qa | frederick |
| 156 | POST | `/account/api/company_api/{id}/tag_deactivate/` | ❌ |  | high | regress | dev/qa | frederick |
| 157 | POST | `/account/api/company_api/{id}/tag_nii_update/` | ❌ |  | high | regress | dev/qa | frederick |
| 158 | POST | `/account/api/company_api/{id}/tag_update/` | ❌ |  | high | regress | dev/qa | frederick |
| 159 | GET | `/account/api/company_api/{id}/unfollow/` | ❌ |  | medium | regress | все | frederick |
| 160 | POST | `/account/api/complaint/` | ❌ |  | high | regress | dev/qa | aliwka |
| 161 | POST | `/account/api/contact_press/` | ❌ |  | high | regress | dev/qa | aliwka |
| 162 | POST | `/account/api/contact_request/` | ❌ |  | high | regress | dev/qa | aliwka |
| 163 | GET | `/account/api/course_application/{id}/` | ❌ |  | low | regress | все | frederick |
| 164 | PUT | `/account/api/course_application/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 165 | PATCH | `/account/api/course_application/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 166 | PATCH | `/account/api/course_application/{id}/accept_course/` | ❌ |  | high | regress | dev/qa | frederick |
| 167 | GET | `/account/api/course_application/{id}/assessment/` | ❌ |  | low | regress | все | frederick |
| 168 | PATCH | `/account/api/course_application/{id}/assessment_passed/` | ❌ |  | high | regress | dev/qa | frederick |
| 169 | GET | `/account/api/course_application/{id}/egov_info/{uuid_param}/` | ❌ |  | low | regress | все | frederick |
| 170 | GET | `/account/api/course_application/{id}/egov_sign/{uuid_param}/` | ❌ |  | low | regress | все | frederick |
| 171 | PUT | `/account/api/course_application/{id}/egov_sign/{uuid_param}/` | ❌ |  | high | regress | dev/qa | frederick |
| 172 | GET | `/account/api/course_application/{id}/egov_sign_uri/` | ❌ |  | low | regress | все | frederick |
| 173 | POST | `/account/api/course_application/{id}/sign/` | ❌ |  | high | regress | dev/qa | frederick |
| 174 | GET | `/account/api/course_application/{id}/xml/` | ❌ |  | low | regress | все | frederick |
| 175 | GET | `/account/api/course_application_stats/get_stats/` | ❌ |  | low | regress | все | frederick |
| 176 | POST | `/account/api/discussion/` | ❌ |  | high | regress | dev/qa | madina |
| 177 | PUT | `/account/api/discussion/{id}/` | ❌ |  | high | regress | dev/qa | madina |
| 178 | PATCH | `/account/api/discussion/{id}/` | ❌ |  | high | regress | dev/qa | madina |
| 179 | GET | `/account/api/discussion/{id}/delete/` | ❌ |  | low | regress | все | madina |
| 180 | POST | `/account/api/discussion/{id}/sign/` | ❌ |  | high | regress | dev/qa | madina |
| 181 | POST | `/account/api/discussion/{id}/vote/` | ❌ |  | high | regress | dev/qa | madina |
| 182 | GET | `/account/api/discussion/{id}/xml/` | ❌ |  | low | regress | все | madina |
| 183 | PUT | `/account/api/elabs_announcement/{id}/` | ❌ |  | high | regress | dev/qa | aliwka |
| 184 | PATCH | `/account/api/elabs_announcement/{id}/` | ❌ |  | high | regress | dev/qa | aliwka |
| 185 | POST | `/account/api/elabs_announcement/{id}/send_email/` | ❌ |  | high | regress | dev/qa | aliwka |
| 186 | POST | `/account/api/email_digest/` | ❌ |  | high | regress | dev/qa | aliwka |
| 187 | GET | `/account/api/event/` | 🔷 | UI `test_event_send` | medium | regress | все | madina |
| 188 | POST | `/account/api/event/` | 🔷 | UI `test_event_send` | critical | smoke | dev/qa | madina |
| 189 | POST | `/account/api/event/check_participate/` | ❌ |  | high | regress | dev/qa | madina |
| 190 | POST | `/account/api/event/participate/` | ❌ |  | high | regress | dev/qa | madina |
| 191 | POST | `/account/api/event/scan_qr/` | ❌ |  | high | regress | dev/qa | madina |
| 192 | GET | `/account/api/event/{id}/` | ❌ |  | medium | regress | все | madina |
| 193 | PUT | `/account/api/event/{id}/` | ❌ |  | high | regress | dev/qa | madina |
| 194 | PATCH | `/account/api/event/{id}/` | ❌ |  | high | regress | dev/qa | madina |
| 195 | GET | `/account/api/event/{id}/delete/` | ❌ |  | medium | regress | все | madina |
| 196 | POST | `/account/api/event/{id}/generate_pdf/` | ❌ |  | high | regress | dev/qa | madina |
| 197 | GET | `/account/api/event/{id}/participant_xlsx/` | ❌ |  | medium | regress | все | madina |
| 198 | GET | `/account/api/event/{id}/send/` | 🔷 | UI `test_event_send` | medium | regress | все | madina |
| 199 | GET | `/account/api/event_participant/` | ❌ |  | medium | regress | все | madina |
| 200 | GET | `/account/api/event_participant/{id}/` | ❌ |  | medium | regress | все | madina |
| 201 | GET | `/account/api/external/companies/` | ❌ |  | low | regress | все | aliwka |
| 202 | GET | `/account/api/external/companies/{id}/` | ❌ |  | low | regress | все | aliwka |
| 203 | POST | `/account/api/external/company_create/` | ❌ |  | high | regress | dev/qa | frederick |
| 204 | GET | `/account/api/external/event_participant/` | ❌ |  | medium | regress | все | madina |
| 205 | POST | `/account/api/external/event_qr_scan/` | ❌ |  | high | regress | dev/qa | madina |
| 206 | POST | `/account/api/external/media_file/` | ❌ |  | high | regress | dev/qa | aliwka |
| 207 | POST | `/account/api/external/protected_media_file/` | ❌ |  | high | regress | dev/qa | aliwka |
| 208 | GET | `/account/api/external/{id}/companies/` | ❌ |  | low | regress | все | aliwka |
| 209 | POST | `/account/api/infrastructure/` | ❌ |  | high | regress | dev/qa | frederick |
| 210 | PUT | `/account/api/infrastructure/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 211 | PATCH | `/account/api/infrastructure/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 212 | GET | `/account/api/infrastructure/{id}/delete/` | ❌ |  | low | regress | все | frederick |
| 213 | GET | `/account/api/infrastructure/{id}/favorite_add/` | ❌ |  | low | regress | все | frederick |
| 214 | GET | `/account/api/infrastructure/{id}/favorite_remove/` | ❌ |  | low | regress | все | frederick |
| 215 | GET | `/account/api/infrastructure/{id}/send/` | ❌ |  | low | regress | все | frederick |
| 216 | POST | `/account/api/infrastructure/{id}/sign/` | ❌ |  | high | regress | dev/qa | frederick |
| 217 | GET | `/account/api/infrastructure/{id}/xml/` | ❌ |  | low | regress | все | frederick |
| 218 | POST | `/account/api/infrastructure_images/` | ❌ |  | high | regress | dev/qa | frederick |
| 219 | PUT | `/account/api/infrastructure_images/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 220 | DELETE | `/account/api/infrastructure_images/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 221 | POST | `/account/api/infrastructure_request/` | ❌ |  | high | regress | dev/qa | frederick |
| 222 | PUT | `/account/api/infrastructure_request/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 223 | PATCH | `/account/api/infrastructure_request/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 224 | POST | `/account/api/media_file/` | 🔷 | UI-загрузка обложки | high | regress | dev/qa | aliwka |
| 225 | GET | `/account/api/notification/` | ❌ |  | low | regress | все | aliwka |
| 226 | GET | `/account/api/notification/{id}/` | ❌ |  | low | regress | все | aliwka |
| 227 | POST | `/account/api/protected_media_file/` | ❌ |  | high | regress | dev/qa | aliwka |
| 228 | GET | `/account/api/protected_media_file/{id}/` | ❌ |  | low | regress | все | aliwka |
| 229 | POST | `/account/api/school_course_application/bulk_update_status/` | ❌ |  | high | regress | dev/qa | frederick |
| 230 | PATCH | `/account/api/school_course_application/confirm_applications/` | ❌ |  | high | regress | dev/qa | frederick |
| 231 | GET | `/account/api/school_course_application/report/` | ❌ |  | low | regress | все | frederick |
| 232 | PUT | `/account/api/school_course_application/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 233 | PATCH | `/account/api/school_course_application/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 234 | PATCH | `/account/api/school_course_application/{id}/grant/` | ❌ |  | high | regress | dev/qa | frederick |
| 235 | PATCH | `/account/api/school_course_application/{id}/reject/` | ❌ |  | high | regress | dev/qa | frederick |
| 236 | PATCH | `/account/api/school_course_application/{id}/waiting_list/` | ❌ |  | high | regress | dev/qa | frederick |
| 237 | GET | `/account/api/school_course_application_stats/get_stats/` | ❌ |  | low | regress | все | frederick |
| 238 | POST | `/account/api/tech_task/` | ❌ |  | critical | smoke | dev/qa | aidar |
| 239 | PUT | `/account/api/tech_task/{id}/` | ❌ |  | high | regress | dev/qa | aidar |
| 240 | PATCH | `/account/api/tech_task/{id}/` | ❌ |  | high | regress | dev/qa | aidar |
| 241 | GET | `/account/api/tech_task/{id}/delete/` | ❌ |  | medium | regress | все | aidar |
| 242 | GET | `/account/api/tech_task/{id}/done/` | ❌ |  | medium | regress | все | aidar |
| 243 | GET | `/account/api/tech_task/{id}/prolong/` | ❌ |  | medium | regress | все | aidar |
| 244 | GET | `/account/api/tech_task/{id}/send/` | ❌ |  | medium | regress | все | aidar |
| 245 | GET | `/account/api/tech_task/{id}/solution_xls/` | ❌ |  | medium | regress | все | aidar |
| 246 | POST | `/account/api/tech_task_solution/` | ❌ |  | high | regress | dev/qa | aidar |
| 247 | PUT | `/account/api/tech_task_solution/{id}/` | ❌ |  | high | regress | dev/qa | aidar |
| 248 | PATCH | `/account/api/tech_task_solution/{id}/` | ❌ |  | high | regress | dev/qa | aidar |
| 249 | GET | `/account/api/tech_task_solution/{id}/approve/` | ❌ |  | medium | regress | все | aidar |
| 250 | GET | `/account/api/tech_task_solution/{id}/delete/` | ❌ |  | medium | regress | все | aidar |
| 251 | POST | `/account/api/tech_task_solution/{id}/reject/` | ❌ |  | high | regress | dev/qa | aidar |
| 252 | GET | `/account/api/tech_task_solution/{id}/send/` | ❌ |  | medium | regress | все | aidar |
| 253 | GET | `/account/api/user/` | ❌ |  | medium | regress | все | frederick |
| 254 | GET | `/account/api/user/education_experience/` | ❌ |  | medium | regress | все | frederick |
| 255 | GET | `/account/api/user/egov_sign_uri/` | ❌ |  | medium | regress | все | frederick |
| 256 | GET | `/account/api/user/info/` | ❌ |  | medium | regress | все | frederick |
| 257 | GET | `/account/api/user/info_by_id/` | ❌ |  | medium | regress | все | frederick |
| 258 | POST | `/account/api/user/tag_deactivate/` | ❌ |  | high | regress | dev/qa | frederick |
| 259 | POST | `/account/api/user/tag_update/` | ❌ |  | high | regress | dev/qa | frederick |
| 260 | POST | `/account/api/user/tips_viewed/` | ❌ |  | high | regress | dev/qa | frederick |
| 261 | POST | `/account/api/user/update_certificate/` | ❌ |  | high | regress | dev/qa | frederick |
| 262 | POST | `/account/api/user/update_company_profile/` | ❌ |  | high | regress | dev/qa | frederick |
| 263 | POST | `/account/api/user/update_course/` | ❌ |  | high | regress | dev/qa | frederick |
| 264 | POST | `/account/api/user/update_education/` | ❌ |  | high | regress | dev/qa | frederick |
| 265 | POST | `/account/api/user/update_experience/` | ❌ |  | high | regress | dev/qa | frederick |
| 266 | POST | `/account/api/user/update_profile/` | ✅ | `test_user_settings.py` (2) | high | regress | dev/qa | frederick |
| 267 | POST | `/account/api/user/xml_data/` | ❌ |  | high | regress | dev/qa | frederick |
| 268 | GET | `/account/api/user/{id}/` | ❌ |  | medium | regress | все | frederick |
| 269 | GET | `/account/api/user/{id}/egov_info/{uuid_param}/` | ❌ |  | medium | regress | все | frederick |
| 270 | GET | `/account/api/user/{id}/egov_sign/{uuid_param}/` | ❌ |  | medium | regress | все | frederick |
| 271 | PUT | `/account/api/user/{id}/egov_sign/{uuid_param}/` | ❌ |  | high | regress | dev/qa | frederick |
| 272 | GET | `/account/api/user/{id}/iin_check/` | ❌ |  | medium | regress | все | frederick |
| 273 | GET | `/account/api/user_company/company-employees/` | ❌ |  | medium | regress | все | frederick |
| 274 | PUT | `/account/api/user_company/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 275 | GET | `/account/api/user_company/{id}/delete/` | ❌ |  | medium | regress | все | frederick |
| 276 | GET | `/account/api/user_company_invitation/` | ❌ |  | medium | regress | все | frederick |
| 277 | POST | `/account/api/user_company_invitation/` | ❌ |  | high | regress | dev/qa | frederick |
| 278 | GET | `/account/api/user_company_invitation/{id}/` | ❌ |  | medium | regress | все | frederick |
| 279 | GET | `/account/api/user_company_invitation/{id}/accept/` | ❌ |  | medium | regress | все | frederick |
| 280 | GET | `/account/api/user_company_invitation/{id}/delete/` | ❌ |  | medium | regress | все | frederick |
| 281 | GET | `/account/api/user_company_invitation/{id}/reject/` | ❌ |  | medium | regress | все | frederick |
| 282 | GET | `/account/api/user_company_request/{id}/reject/` | ❌ |  | medium | regress | все | frederick |
| 283 | GET | `/account/api/user_company_request/{id}/verify/` | ❌ |  | medium | regress | все | frederick |
| 284 | POST | `/account/api/v2/flow/set_company_names/` | ❌ |  | high | regress | dev/qa | frederick |
| 285 | POST | `/account/api/v2/flow/set_company_tag/` | ❌ |  | high | regress | dev/qa | frederick |
| 286 | POST | `/account/api/v2/flow/set_goals/` | ❌ |  | high | regress | dev/qa | aliwka |
| 287 | POST | `/account/api/v2/flow/set_image/` | ❌ |  | high | regress | dev/qa | aliwka |
| 288 | POST | `/account/api/v2/flow/set_names/` | 🔷 | UI-регистрация (skip) | high | regress | dev/qa | aliwka |
| 289 | POST | `/account/api/v2/flow/set_tag/` | ❌ |  | high | regress | dev/qa | aliwka |
| 290 | POST | `/account/api/v2/onboarding/set_community_role/` | ❌ |  | high | regress | dev/qa | madina |
| 291 | POST | `/account/api/v2/onboarding/set_photo/` | ❌ |  | high | regress | dev/qa | aliwka |
| 292 | GET | `/account/api/v2/onboarding/status/` | ❌ |  | low | regress | все | aliwka |
| 293 | GET | `/account/api/vacancy/` | 🔷 | UI `test_vacancy_create_post_page` | medium | regress | все | aidar |
| 294 | POST | `/account/api/vacancy/` | 🔷 | UI `test_vacancy_create_post_page` | critical | smoke | dev/qa | aidar |
| 295 | POST | `/account/api/vacancy/apply/` | ❌ |  | high | regress | dev/qa | aidar |
| 296 | GET | `/account/api/vacancy/candidate/seeker/` | ❌ |  | medium | regress | все | aidar |
| 297 | GET | `/account/api/vacancy/candidate/seeker/count/` | ❌ |  | medium | regress | все | aidar |
| 298 | GET | `/account/api/vacancy/candidate/seeker/{id}/` | ❌ |  | medium | regress | все | aidar |
| 299 | GET | `/account/api/vacancy/count_candidates/` | ❌ |  | medium | regress | все | aidar |
| 300 | GET | `/account/api/vacancy/{id}/` | ❌ |  | medium | regress | все | aidar |
| 301 | PUT | `/account/api/vacancy/{id}/` | ❌ |  | high | regress | dev/qa | aidar |
| 302 | PATCH | `/account/api/vacancy/{id}/` | ❌ |  | high | regress | dev/qa | aidar |
| 303 | GET | `/account/api/vacancy/{id}/delete/` | ❌ |  | medium | regress | все | aidar |
| 304 | PUT | `/account/api/vacancy/{id}/restore/` | ❌ |  | high | regress | dev/qa | aidar |
| 305 | GET | `/account/api/vacancy/{id}/send/` | ❌ |  | medium | regress | все | aidar |
| 306 | GET | `/account/api/vacancy/{vacancy_pk}/candidates/` | ❌ |  | medium | regress | все | aidar |
| 307 | GET | `/account/api/vacancy/{vacancy_pk}/candidates/my/` | ❌ |  | medium | regress | все | aidar |
| 308 | GET | `/account/api/vacancy/{vacancy_pk}/candidates/{id}/` | ❌ |  | medium | regress | все | aidar |
| 309 | PATCH | `/account/api/vacancy/{vacancy_pk}/candidates/{id}/offer/` | ❌ |  | high | regress | dev/qa | aidar |
| 310 | PATCH | `/account/api/vacancy/{vacancy_pk}/candidates/{id}/reject_recruiter/` | ❌ |  | high | regress | dev/qa | aidar |
| 311 | PATCH | `/account/api/vacancy/{vacancy_pk}/candidates/{id}/reject_seeker/` | ❌ |  | high | regress | dev/qa | aidar |
| 312 | PATCH | `/account/api/vacancy/{vacancy_pk}/candidates/{id}/status_change/` | ❌ |  | high | regress | dev/qa | aidar |

## techhub — прочие модули (95)

| № | Метод | Эндпоинт | Статус | Тест | Критичность | Набор | Среда | Ответственный |
|---|---|---|---|---|---|---|---|---|
| 313 | POST | `/api_gateway/` | ❌ |  | high | regress | dev/qa | aliwka |
| 314 | GET | `/community/api/blog/` | ❌ |  | medium | regress | все | madina |
| 315 | GET | `/community/api/blog/{id}/` | ❌ |  | medium | regress | все | madina |
| 316 | GET | `/community/api/blog/{id}/favorite_add/` | ❌ |  | medium | regress | все | madina |
| 317 | GET | `/community/api/blog/{id}/favorite_remove/` | ❌ |  | medium | regress | все | madina |
| 318 | GET | `/community/api/blog/{id}/reaction_down/` | ❌ |  | medium | regress | все | madina |
| 319 | GET | `/community/api/blog/{id}/reaction_up/` | ❌ |  | medium | regress | все | madina |
| 320 | POST | `/community/api/blog/{id}/read/` | ❌ |  | high | regress | dev/qa | madina |
| 321 | GET | `/community/api/company/` | ❌ |  | medium | regress | все | madina |
| 322 | GET | `/community/api/company/{id}/` | ❌ |  | medium | regress | все | madina |
| 323 | GET | `/community/api/company_follow/` | ❌ |  | medium | regress | все | madina |
| 324 | POST | `/community/api/company_follow/follow/` | ❌ |  | high | regress | dev/qa | madina |
| 325 | POST | `/community/api/company_follow/unfollow/` | ❌ |  | high | regress | dev/qa | madina |
| 326 | GET | `/community/api/company_follow/{id}/` | ❌ |  | medium | regress | все | madina |
| 327 | GET | `/community/api/company_follow/{id}/followers/` | ❌ |  | medium | regress | все | madina |
| 328 | GET | `/community/api/company_follow/{id}/following/` | ❌ |  | medium | regress | все | madina |
| 329 | GET | `/community/api/user/` | ❌ |  | medium | regress | все | madina |
| 330 | GET | `/community/api/user/{id}/` | ❌ |  | medium | regress | все | madina |
| 331 | GET | `/community/api/user_follow/` | ❌ |  | medium | regress | все | madina |
| 332 | POST | `/community/api/user_follow/follow/` | ❌ |  | high | regress | dev/qa | madina |
| 333 | POST | `/community/api/user_follow/unfollow/` | ❌ |  | high | regress | dev/qa | madina |
| 334 | GET | `/community/api/user_follow/{id}/` | ❌ |  | medium | regress | все | madina |
| 335 | GET | `/community/api/user_follow/{id}/followers/` | ❌ |  | medium | regress | все | madina |
| 336 | GET | `/community/api/user_follow/{id}/following/` | ❌ |  | medium | regress | все | madina |
| 337 | GET | `/community/api/user_short_list/` | ❌ |  | medium | regress | все | madina |
| 338 | GET | `/community/api/user_short_list/{id}/` | ❌ |  | medium | regress | все | madina |
| 339 | GET | `/feedback/api/form/` | ❌ |  | medium | regress | все | madina |
| 340 | GET | `/feedback/api/form/{slug}/` | ❌ |  | medium | regress | все | madina |
| 341 | POST | `/feedback/api/form/{slug}/submit/` | ❌ |  | high | regress | dev/qa | madina |
| 342 | POST | `/fortune-wheel/api/{id}/spin/` | ❌ |  | high | regress | dev/qa | madina |
| 343 | GET | `/fortune-wheel/api/{id}/status/` | ❌ |  | low | regress | все | madina |
| 344 | GET | `/games/company/history/{id}/` | ❌ |  | medium | regress | все | madina |
| 345 | GET | `/games/company/player/rating/{id}/` | ❌ |  | medium | regress | все | madina |
| 346 | GET | `/games/company/rating/{id}/` | ❌ |  | medium | regress | все | madina |
| 347 | POST | `/games/company/set_modal_viewed/{id}/` | ❌ |  | high | regress | dev/qa | madina |
| 348 | GET | `/games/get_last_badge/` | ❌ |  | low | regress | все | madina |
| 349 | GET | `/games/main/` | ❌ |  | low | regress | все | madina |
| 350 | GET | `/games/rating/` | ❌ |  | low | regress | все | madina |
| 351 | POST | `/games/set_modal_viewed/` | ❌ |  | high | regress | dev/qa | madina |
| 352 | GET | `/games/v2/faq/` | ❌ |  | low | regress | все | madina |
| 353 | GET | `/games/v2/history/` | ❌ |  | low | regress | все | madina |
| 354 | GET | `/games/v2/history/modal/` | ❌ |  | low | regress | все | madina |
| 355 | GET | `/games/v2/history/set_history_viewed/{id}/` | ❌ |  | low | regress | все | madina |
| 356 | GET | `/games/v2/main/` | ❌ |  | low | regress | все | madina |
| 357 | GET | `/games/v2/player/` | ❌ |  | low | regress | все | madina |
| 358 | GET | `/games/v2/rating/` | ❌ |  | low | regress | все | madina |
| 359 | POST | `/games/webhook/history/` | ❌ |  | high | regress | dev/qa | madina |
| 360 | POST | `/has_permissions/` | ❌ |  | high | regress | dev/qa | aliwka |
| 361 | GET | `/integrations/api/contacts/` | ❌ |  | low | regress | все | aliwka |
| 362 | GET | `/integrations/api/customer-support/` | ❌ |  | low | regress | все | aliwka |
| 363 | GET | `/integrations/api/faq/` | ❌ |  | low | regress | все | aliwka |
| 364 | GET | `/integrations/api/gamification/` | ❌ |  | low | regress | все | aliwka |
| 365 | POST | `/journey-map/api/activate_step/` | ❌ |  | high | regress | dev/qa | frederick |
| 366 | POST | `/journey-map/api/complete_question/` | ❌ |  | high | regress | dev/qa | frederick |
| 367 | POST | `/journey-map/api/complete_step/` | ❌ |  | high | regress | dev/qa | frederick |
| 368 | POST | `/journey-map/api/complete_task/` | ❌ |  | high | regress | dev/qa | frederick |
| 369 | POST | `/journey-map/api/deactivate_step/` | ❌ |  | high | regress | dev/qa | frederick |
| 370 | GET | `/journey-map/api/display/expertise_tags/` | ❌ |  | low | regress | все | frederick |
| 371 | GET | `/journey-map/api/display/{id}/journey_map/` | ❌ |  | low | regress | все | frederick |
| 372 | GET | `/journey-map/api/display/{id}/questions/` | ❌ |  | low | regress | все | frederick |
| 373 | GET | `/journey-map/api/display/{id}/recommendations/{recommendation_type}/` | ❌ |  | low | regress | все | frederick |
| 374 | GET | `/journey-map/api/display/{id}/stage2_info/` | ❌ |  | low | regress | все | frederick |
| 375 | GET | `/journey-map/api/display/{id}/steps/` | ❌ |  | low | regress | все | frederick |
| 376 | GET | `/journey-map/api/display/{id}/tasks/` | ❌ |  | low | regress | все | frederick |
| 377 | POST | `/journey-map/api/skip_step/` | ❌ |  | high | regress | dev/qa | frederick |
| 378 | POST | `/journey-map/api/top-performers/{id}/dismiss/` | ❌ |  | high | regress | dev/qa | frederick |
| 379 | GET | `/journey-map/api/top-performers/{id}/top_performers/` | ❌ |  | low | regress | все | frederick |
| 380 | GET | `/journey-map/api/top-performers/{id}/win_state/` | ❌ |  | low | regress | все | frederick |
| 381 | POST | `/journey-map/api/unlock_step/` | ❌ |  | high | regress | dev/qa | frederick |
| 382 | GET | `/matchmaking/api/matchmaking/get_history/` | ❌ |  | low | regress | все | madina |
| 383 | GET | `/matchmaking/api/matchmaking/get_matches/` | ❌ |  | low | regress | все | frederick |
| 384 | GET | `/matchmaking/api/matchmaking/has_matches/` | ❌ |  | low | regress | все | frederick |
| 385 | GET | `/matchmaking/api/profile/` | ❌ |  | low | regress | все | frederick |
| 386 | POST | `/matchmaking/api/profile/` | ❌ |  | high | regress | dev/qa | frederick |
| 387 | GET | `/matchmaking/api/profile/deactivate_profile/` | ❌ |  | low | regress | все | frederick |
| 388 | PUT | `/matchmaking/api/profile/update_profile/` | ❌ |  | high | regress | dev/qa | frederick |
| 389 | GET | `/matchmaking/api/profile/{id}/` | ❌ |  | low | regress | все | frederick |
| 390 | POST | `/ru/set-cookie-policy/` | ❌ |  | high | regress | dev/qa | aliwka |
| 391 | GET | `/search/` | ❌ |  | medium | regress | все | aliwka |
| 392 | GET | `/search/v2/` | ❌ |  | medium | regress | все | aliwka |
| 393 | GET | `/search/v3/` | ❌ |  | medium | regress | все | aliwka |
| 394 | GET | `/shared/api/context_data/` | ❌ |  | low | regress | все | aliwka |
| 395 | GET | `/shared/api/context_data/{code}/` | ❌ |  | low | regress | все | aliwka |
| 396 | GET | `/sponsorship/api/sponsorship/mrp/` | ❌ |  | low | regress | все | aliwka |
| 397 | GET | `/sponsorship/api/sponsorship/{id}/calculate/` | ❌ |  | low | regress | все | aliwka |
| 398 | GET | `/sponsorship/api/sponsorship/{id}/company_context/` | ❌ |  | medium | regress | все | frederick |
| 399 | GET | `/techorda/api/external/course/` | ❌ |  | low | regress | все | frederick |
| 400 | POST | `/techorda/api/external/course_application/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 401 | POST | `/techorda/api/external/course_application/pre_check/` | ❌ |  | high | regress | dev/qa | frederick |
| 402 | POST | `/techorda/api/external/course_application/xml/` | ❌ |  | high | regress | dev/qa | frederick |
| 403 | GET | `/techorda/api/external/course_application/{id}/` | ❌ |  | low | regress | все | frederick |
| 404 | GET | `/techorda/api/external/school/` | ❌ |  | low | regress | все | frederick |
| 405 | GET | `/techorda/api/favorites/{id}/add_to_favorite/` | ❌ |  | low | regress | все | frederick |
| 406 | GET | `/techorda/api/favorites/{id}/remove_from_favorite/` | ❌ |  | low | regress | все | frederick |
| 407 | POST | `/translate/` | 🔷 | UI `test_vacancy_create_post_page` | high | regress | dev/qa | aliwka |

## techhub — АРМ (админка) (216)

| № | Метод | Эндпоинт | Статус | Тест | Критичность | Набор | Среда | Ответственный |
|---|---|---|---|---|---|---|---|---|
| 408 | GET | `/arm/action_log/` | ❌ |  | low | regress | все | — |
| 409 | GET | `/arm/action_log/{id}/` | ❌ |  | low | regress | все | — |
| 410 | GET | `/arm/article/` | ❌ |  | low | regress | все | — |
| 411 | POST | `/arm/article/create/` | ❌ |  | low | regress | dev/qa | — |
| 412 | GET | `/arm/article/xls/` | ❌ |  | low | regress | все | — |
| 413 | GET | `/arm/article/{id}/` | ❌ |  | low | regress | все | — |
| 414 | GET | `/arm/article/{id}/approve/` | ❌ |  | low | regress | все | — |
| 415 | POST | `/arm/article/{id}/correction/` | ❌ |  | low | regress | dev/qa | — |
| 416 | DELETE | `/arm/article/{id}/delete/` | ❌ |  | low | regress | dev/qa | — |
| 417 | GET | `/arm/article/{id}/publish/` | ❌ |  | low | regress | все | — |
| 418 | POST | `/arm/article/{id}/reject/` | ❌ |  | low | regress | dev/qa | — |
| 419 | GET | `/arm/article/{id}/show_in_feed/` | ❌ |  | low | regress | все | — |
| 420 | GET | `/arm/article/{id}/unpublish/` | ❌ |  | low | regress | все | — |
| 421 | GET | `/arm/article/{id}/unshow_in_feed/` | ❌ |  | low | regress | все | — |
| 422 | PUT | `/arm/article/{id}/update/` | ❌ |  | low | regress | dev/qa | — |
| 423 | GET | `/arm/blog/` | ❌ |  | low | regress | все | — |
| 424 | POST | `/arm/blog/` | ❌ |  | low | regress | dev/qa | — |
| 425 | GET | `/arm/blog/xls/` | ❌ |  | low | regress | все | — |
| 426 | GET | `/arm/blog/{id}/` | ❌ |  | low | regress | все | — |
| 427 | PUT | `/arm/blog/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 428 | PATCH | `/arm/blog/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 429 | DELETE | `/arm/blog/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 430 | GET | `/arm/blog/{id}/approve/` | ❌ |  | low | regress | все | — |
| 431 | POST | `/arm/blog/{id}/correction/` | ❌ |  | low | regress | dev/qa | — |
| 432 | GET | `/arm/blog/{id}/publish/` | ❌ |  | low | regress | все | — |
| 433 | POST | `/arm/blog/{id}/reject/` | ❌ |  | low | regress | dev/qa | — |
| 434 | POST | `/arm/blog/{id}/run_ai_moderation/` | ❌ |  | low | regress | dev/qa | — |
| 435 | GET | `/arm/blog/{id}/show_in_feed/` | ❌ |  | low | regress | все | — |
| 436 | GET | `/arm/blog/{id}/unpublish/` | ❌ |  | low | regress | все | — |
| 437 | GET | `/arm/blog/{id}/unshow_in_feed/` | ❌ |  | low | regress | все | — |
| 438 | GET | `/arm/booking/` | ❌ |  | low | regress | все | — |
| 439 | GET | `/arm/booking/xls/` | ❌ |  | low | regress | все | — |
| 440 | GET | `/arm/booking/{id}/` | ❌ |  | low | regress | все | — |
| 441 | POST | `/arm/booking/{id}/correction/` | ❌ |  | low | regress | dev/qa | — |
| 442 | POST | `/arm/booking/{id}/deactivate/` | ❌ |  | low | regress | dev/qa | — |
| 443 | GET | `/arm/booking_company/` | ❌ |  | low | regress | все | — |
| 444 | POST | `/arm/booking_company/activate/` | ❌ |  | low | regress | dev/qa | — |
| 445 | POST | `/arm/booking_company/deactivate/` | ❌ |  | low | regress | dev/qa | — |
| 446 | GET | `/arm/booking_company/{id}/` | ❌ |  | low | regress | все | — |
| 447 | GET | `/arm/bug_report/` | ❌ |  | low | regress | все | — |
| 448 | GET | `/arm/bug_report/{id}/` | ❌ |  | low | regress | все | — |
| 449 | POST | `/arm/bug_report/{id}/approve/` | ❌ |  | low | regress | dev/qa | — |
| 450 | POST | `/arm/bug_report/{id}/reject/` | ❌ |  | low | regress | dev/qa | — |
| 451 | GET | `/arm/category/` | ❌ |  | low | regress | все | — |
| 452 | GET | `/arm/cett-monitoring-archives/` | ❌ |  | low | regress | все | — |
| 453 | GET | `/arm/cett-monitoring-archives/{id}/` | ❌ |  | low | regress | все | — |
| 454 | GET | `/arm/cett-monitoring-archives/{id}/download/` | ❌ |  | low | regress | все | — |
| 455 | GET | `/arm/city/` | ❌ |  | low | regress | все | — |
| 456 | GET | `/arm/comment/` | ❌ |  | low | regress | все | — |
| 457 | GET | `/arm/comment/{id}/` | ❌ |  | low | regress | все | — |
| 458 | GET | `/arm/comment/{id}/delete/` | ❌ |  | low | regress | все | — |
| 459 | GET | `/arm/company/` | ❌ |  | low | regress | все | — |
| 460 | GET | `/arm/company/{id}/` | ❌ |  | low | regress | все | — |
| 461 | GET | `/arm/complaint/` | ❌ |  | low | regress | все | — |
| 462 | GET | `/arm/complaint/{id}/` | ❌ |  | low | regress | все | — |
| 463 | POST | `/arm/component/create/` | ❌ |  | low | regress | dev/qa | — |
| 464 | DELETE | `/arm/component/{id}/delete/` | ❌ |  | low | regress | dev/qa | — |
| 465 | GET | `/arm/component/{id}/move/down/` | ❌ |  | low | regress | все | — |
| 466 | GET | `/arm/component/{id}/move/up/` | ❌ |  | low | regress | все | — |
| 467 | PUT | `/arm/component/{id}/update/` | ❌ |  | low | regress | dev/qa | — |
| 468 | GET | `/arm/context/` | ❌ |  | low | regress | все | — |
| 469 | POST | `/arm/dashboard/` | ❌ |  | low | regress | dev/qa | — |
| 470 | GET | `/arm/discussion/` | ❌ |  | low | regress | все | — |
| 471 | POST | `/arm/discussion/` | ❌ |  | low | regress | dev/qa | — |
| 472 | GET | `/arm/discussion/{id}/` | ❌ |  | low | regress | все | — |
| 473 | PUT | `/arm/discussion/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 474 | PATCH | `/arm/discussion/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 475 | DELETE | `/arm/discussion/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 476 | GET | `/arm/discussion/{id}/approve/` | ❌ |  | low | regress | все | — |
| 477 | POST | `/arm/discussion/{id}/correction/` | ❌ |  | low | regress | dev/qa | — |
| 478 | POST | `/arm/discussion/{id}/edit_status/` | ❌ |  | low | regress | dev/qa | — |
| 479 | GET | `/arm/discussion/{id}/publish/` | ❌ |  | low | regress | все | — |
| 480 | POST | `/arm/discussion/{id}/reject/` | ❌ |  | low | regress | dev/qa | — |
| 481 | POST | `/arm/discussion/{id}/set_status/` | ❌ |  | low | regress | dev/qa | — |
| 482 | GET | `/arm/discussion/{id}/show_in_feed/` | ❌ |  | low | regress | все | — |
| 483 | GET | `/arm/discussion/{id}/unpublish/` | ❌ |  | low | regress | все | — |
| 484 | GET | `/arm/discussion/{id}/unshow_in_feed/` | ❌ |  | low | regress | все | — |
| 485 | GET | `/arm/discussion/{id}/votes/` | ❌ |  | low | regress | все | — |
| 486 | GET | `/arm/ecosystem_company/` | ❌ |  | low | regress | все | — |
| 487 | POST | `/arm/ecosystem_company/` | ❌ |  | low | regress | dev/qa | — |
| 488 | GET | `/arm/ecosystem_company/context/` | ❌ |  | low | regress | все | — |
| 489 | GET | `/arm/ecosystem_company/{id}/` | ❌ |  | low | regress | все | — |
| 490 | PUT | `/arm/ecosystem_company/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 491 | PATCH | `/arm/ecosystem_company/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 492 | GET | `/arm/ecosystem_company/{id}/deactivate/` | ❌ |  | low | regress | все | — |
| 493 | POST | `/arm/ecosystem_company/{id}/tag_activate/` | ❌ |  | low | regress | dev/qa | — |
| 494 | POST | `/arm/ecosystem_company/{id}/tag_correction/` | ❌ |  | low | regress | dev/qa | — |
| 495 | POST | `/arm/ecosystem_company/{id}/tag_deactivate/` | ❌ |  | low | regress | dev/qa | — |
| 496 | POST | `/arm/ecosystem_company/{id}/tag_update/` | ❌ |  | low | regress | dev/qa | — |
| 497 | GET | `/arm/ecosystem_user/` | ❌ |  | low | regress | все | — |
| 498 | POST | `/arm/ecosystem_user/` | ❌ |  | low | regress | dev/qa | — |
| 499 | GET | `/arm/ecosystem_user/context/` | ❌ |  | low | regress | все | — |
| 500 | GET | `/arm/ecosystem_user/{id}/` | ❌ |  | low | regress | все | — |
| 501 | PUT | `/arm/ecosystem_user/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 502 | PATCH | `/arm/ecosystem_user/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 503 | GET | `/arm/ecosystem_user/{id}/deactivate/` | ❌ |  | low | regress | все | — |
| 504 | POST | `/arm/ecosystem_user/{id}/tag_activate/` | ❌ |  | low | regress | dev/qa | — |
| 505 | POST | `/arm/ecosystem_user/{id}/tag_correction/` | ❌ |  | low | regress | dev/qa | — |
| 506 | POST | `/arm/ecosystem_user/{id}/tag_deactivate/` | ❌ |  | low | regress | dev/qa | — |
| 507 | POST | `/arm/ecosystem_user/{id}/tag_update/` | ❌ |  | low | regress | dev/qa | — |
| 508 | GET | `/arm/elabs_announcement/` | ❌ |  | low | regress | все | — |
| 509 | GET | `/arm/elabs_announcement/{id}/` | ❌ |  | low | regress | все | — |
| 510 | GET | `/arm/elabs_announcement/{id}/activate/` | ❌ |  | low | regress | все | — |
| 511 | GET | `/arm/elabs_announcement/{id}/deactivate/` | ❌ |  | low | regress | все | — |
| 512 | GET | `/arm/event/` | ❌ |  | low | regress | все | — |
| 513 | POST | `/arm/event/` | ❌ |  | low | regress | dev/qa | — |
| 514 | GET | `/arm/event/{id}/` | ❌ |  | low | regress | все | — |
| 515 | PUT | `/arm/event/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 516 | PATCH | `/arm/event/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 517 | DELETE | `/arm/event/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 518 | GET | `/arm/event/{id}/approve/` | ❌ |  | low | regress | все | — |
| 519 | GET | `/arm/event/{id}/available/` | ❌ |  | low | regress | все | — |
| 520 | POST | `/arm/event/{id}/correction/` | ❌ |  | low | regress | dev/qa | — |
| 521 | GET | `/arm/event/{id}/history/` | ❌ |  | low | regress | все | — |
| 522 | GET | `/arm/event/{id}/participant_report/` | ❌ |  | low | regress | все | — |
| 523 | GET | `/arm/event/{id}/publish/` | ❌ |  | low | regress | все | — |
| 524 | POST | `/arm/event/{id}/reject/` | ❌ |  | low | regress | dev/qa | — |
| 525 | GET | `/arm/event/{id}/unavailable/` | ❌ |  | low | regress | все | — |
| 526 | GET | `/arm/event/{id}/unpublish/` | ❌ |  | low | regress | все | — |
| 527 | GET | `/arm/event_participant/` | ❌ |  | low | regress | все | — |
| 528 | POST | `/arm/event_participant/cancel/` | ❌ |  | low | regress | dev/qa | — |
| 529 | POST | `/arm/event_participant/scan_qr/` | ❌ |  | low | regress | dev/qa | — |
| 530 | GET | `/arm/event_participant/status/` | ❌ |  | low | regress | все | — |
| 531 | GET | `/arm/event_participant/{id}/` | ❌ |  | low | regress | все | — |
| 532 | GET | `/arm/feedback/` | ❌ |  | low | regress | все | — |
| 533 | GET | `/arm/feedback/{id}/` | ❌ |  | low | regress | все | — |
| 534 | POST | `/arm/feedback/{id}/assign/` | ❌ |  | low | regress | dev/qa | — |
| 535 | POST | `/arm/feedback/{id}/change_status/` | ❌ |  | low | regress | dev/qa | — |
| 536 | GET | `/arm/get/` | ❌ |  | low | regress | все | — |
| 537 | GET | `/arm/infrastructure/` | ❌ |  | low | regress | все | — |
| 538 | POST | `/arm/infrastructure/` | ❌ |  | low | regress | dev/qa | — |
| 539 | GET | `/arm/infrastructure/{id}/` | ❌ |  | low | regress | все | — |
| 540 | PUT | `/arm/infrastructure/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 541 | PATCH | `/arm/infrastructure/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 542 | GET | `/arm/infrastructure/{id}/approve/` | ❌ |  | low | regress | все | — |
| 543 | POST | `/arm/infrastructure/{id}/correction/` | ❌ |  | low | regress | dev/qa | — |
| 544 | GET | `/arm/infrastructure/{id}/publish/` | ❌ |  | low | regress | все | — |
| 545 | POST | `/arm/infrastructure/{id}/reject/` | ❌ |  | low | regress | dev/qa | — |
| 546 | POST | `/arm/infrastructure/{id}/set_status/` | ❌ |  | low | regress | dev/qa | — |
| 547 | GET | `/arm/infrastructure/{id}/unpublish/` | ❌ |  | low | regress | все | — |
| 548 | GET | `/arm/media_file/` | ❌ |  | low | regress | все | — |
| 549 | POST | `/arm/media_file/create/` | ❌ |  | low | regress | dev/qa | — |
| 550 | GET | `/arm/notification/` | ❌ |  | low | regress | все | — |
| 551 | GET | `/arm/notification/{id}/` | ❌ |  | low | regress | все | — |
| 552 | GET | `/arm/page/` | ❌ |  | low | regress | все | — |
| 553 | POST | `/arm/page/create/` | ❌ |  | low | regress | dev/qa | — |
| 554 | GET | `/arm/page/media_file/` | ❌ |  | low | regress | все | — |
| 555 | POST | `/arm/page/media_file/create/` | ❌ |  | low | regress | dev/qa | — |
| 556 | GET | `/arm/page/{id}/` | ❌ |  | low | regress | все | — |
| 557 | POST | `/arm/page/{id}/copy/` | ❌ |  | low | regress | dev/qa | — |
| 558 | GET | `/arm/page/{id}/publish/` | ❌ |  | low | regress | все | — |
| 559 | GET | `/arm/page/{id}/unpublish/` | ❌ |  | low | regress | все | — |
| 560 | PUT | `/arm/page/{id}/update/` | ❌ |  | low | regress | dev/qa | — |
| 561 | POST | `/arm/pdf/generate/` | ❌ |  | low | regress | dev/qa | — |
| 562 | GET | `/arm/project_registry/` | ❌ |  | low | regress | все | — |
| 563 | POST | `/arm/project_registry/` | ❌ |  | low | regress | dev/qa | — |
| 564 | GET | `/arm/project_registry/context/status/` | ❌ |  | low | regress | все | — |
| 565 | POST | `/arm/project_registry/import_excel/` | ❌ |  | low | regress | dev/qa | — |
| 566 | GET | `/arm/project_registry/{id}/` | ❌ |  | low | regress | все | — |
| 567 | PUT | `/arm/project_registry/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 568 | PATCH | `/arm/project_registry/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 569 | DELETE | `/arm/project_registry/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 570 | POST | `/arm/protected_media_file/create/` | ❌ |  | low | regress | dev/qa | — |
| 571 | GET | `/arm/role_monitorning/` | ❌ |  | low | regress | все | — |
| 572 | GET | `/arm/role_monitorning/context/` | ❌ |  | low | regress | все | — |
| 573 | GET | `/arm/role_monitorning/xls/` | ❌ |  | low | regress | все | — |
| 574 | GET | `/arm/role_monitorning/{id}/` | ❌ |  | low | regress | все | — |
| 575 | POST | `/arm/section/create/` | ❌ |  | low | regress | dev/qa | — |
| 576 | DELETE | `/arm/section/{id}/delete/` | ❌ |  | low | regress | dev/qa | — |
| 577 | PUT | `/arm/section/{id}/update/` | ❌ |  | low | regress | dev/qa | — |
| 578 | GET | `/arm/tech_task/` | ❌ |  | low | regress | все | — |
| 579 | POST | `/arm/tech_task/` | ❌ |  | low | regress | dev/qa | — |
| 580 | GET | `/arm/tech_task/xls/` | ❌ |  | low | regress | все | — |
| 581 | GET | `/arm/tech_task/{id}/` | ❌ |  | low | regress | все | — |
| 582 | PUT | `/arm/tech_task/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 583 | PATCH | `/arm/tech_task/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 584 | GET | `/arm/tech_task/{id}/approve/` | ❌ |  | low | regress | все | — |
| 585 | POST | `/arm/tech_task/{id}/correction/` | ❌ |  | low | regress | dev/qa | — |
| 586 | GET | `/arm/tech_task/{id}/pdf/` | ❌ |  | low | regress | все | — |
| 587 | GET | `/arm/tech_task/{id}/publish/` | ❌ |  | low | regress | все | — |
| 588 | POST | `/arm/tech_task/{id}/reject/` | ❌ |  | low | regress | dev/qa | — |
| 589 | POST | `/arm/tech_task/{id}/run_ai_moderation/` | ❌ |  | low | regress | dev/qa | — |
| 590 | POST | `/arm/tech_task/{id}/set_status/` | ❌ |  | low | regress | dev/qa | — |
| 591 | GET | `/arm/tech_task/{id}/show_in_feed/` | ❌ |  | low | regress | все | — |
| 592 | GET | `/arm/tech_task/{id}/solution/` | ❌ |  | low | regress | все | — |
| 593 | GET | `/arm/tech_task/{id}/solution_xls/` | ❌ |  | low | regress | все | — |
| 594 | GET | `/arm/tech_task/{id}/unpublish/` | ❌ |  | low | regress | все | — |
| 595 | GET | `/arm/tech_task/{id}/unshow_in_feed/` | ❌ |  | low | regress | все | — |
| 596 | GET | `/arm/techorda_course/` | ❌ |  | low | regress | все | — |
| 597 | GET | `/arm/techorda_course/xls/` | ❌ |  | low | regress | все | — |
| 598 | GET | `/arm/techorda_course/{id}/` | ❌ |  | low | regress | все | — |
| 599 | GET | `/arm/techorda_course_application/` | ❌ |  | low | regress | все | — |
| 600 | GET | `/arm/techorda_course_application/send_techorda_notifications/` | ❌ |  | low | regress | все | — |
| 601 | GET | `/arm/techorda_course_application/xls/` | ❌ |  | low | regress | все | — |
| 602 | GET | `/arm/techorda_course_application/{id}/` | ❌ |  | low | regress | все | — |
| 603 | GET | `/arm/techorda_school/` | ❌ |  | low | regress | все | — |
| 604 | GET | `/arm/techorda_school/xls/` | ❌ |  | low | regress | все | — |
| 605 | GET | `/arm/techorda_school/{id}/` | ❌ |  | low | regress | все | — |
| 606 | GET | `/arm/user/` | ❌ |  | low | regress | все | — |
| 607 | GET | `/arm/user/{id}/` | ❌ |  | low | regress | все | — |
| 608 | GET | `/arm/vacancy/` | ❌ |  | low | regress | все | — |
| 609 | POST | `/arm/vacancy/` | ❌ |  | low | regress | dev/qa | — |
| 610 | GET | `/arm/vacancy/context/` | ❌ |  | low | regress | все | — |
| 611 | GET | `/arm/vacancy/{id}/` | ❌ |  | low | regress | все | — |
| 612 | PUT | `/arm/vacancy/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 613 | PATCH | `/arm/vacancy/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 614 | DELETE | `/arm/vacancy/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 615 | GET | `/arm/vacancy/{id}/approve/` | ❌ |  | low | regress | все | — |
| 616 | POST | `/arm/vacancy/{id}/correction/` | ❌ |  | low | regress | dev/qa | — |
| 617 | GET | `/arm/vacancy/{id}/history/` | ❌ |  | low | regress | все | — |
| 618 | GET | `/arm/vacancy/{id}/publish/` | ❌ |  | low | regress | все | — |
| 619 | POST | `/arm/vacancy/{id}/reject/` | ❌ |  | low | regress | dev/qa | — |
| 620 | POST | `/arm/vacancy/{id}/run_ai_moderation/` | ❌ |  | low | regress | dev/qa | — |
| 621 | GET | `/arm/vacancy/{id}/unpublish/` | ❌ |  | low | regress | все | — |
| 622 | GET | `/arm/vacancy_candidate/` | ❌ |  | low | regress | все | — |
| 623 | GET | `/arm/vacancy_candidate/{id}/` | ❌ |  | low | regress | все | — |

## marketplace — Hub Market (152)

| № | Метод | Эндпоинт | Статус | Тест | Критичность | Набор | Среда | Ответственный |
|---|---|---|---|---|---|---|---|---|
| 624 | GET | `/api/arm/orders/` | ❌ |  | low | regress | все | — |
| 625 | GET | `/api/arm/orders/all/` | ❌ |  | low | regress | все | — |
| 626 | GET | `/api/arm/orders/{id}/` | ❌ |  | low | regress | все | — |
| 627 | GET | `/api/arm/orders/{id}/all/` | ❌ |  | low | regress | все | — |
| 628 | POST | `/api/arm/orders/{id}/process_action/` | ❌ |  | low | regress | dev/qa | — |
| 629 | GET | `/api/arm/products/` | ❌ |  | low | regress | все | — |
| 630 | POST | `/api/arm/products/` | ❌ |  | low | regress | dev/qa | — |
| 631 | GET | `/api/arm/products/{id}/` | ❌ |  | low | regress | все | — |
| 632 | PATCH | `/api/arm/products/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 633 | POST | `/api/arm/products/{id}/process_action/` | ❌ |  | low | regress | dev/qa | — |
| 634 | POST | `/api/basket/add/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 635 | POST | `/api/basket/remove/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 636 | POST | `/api/basket/set/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 637 | GET | `/api/boost_campaign/` | ❌ |  | low | regress | все | frederick |
| 638 | POST | `/api/boost_campaign/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 639 | GET | `/api/boost_campaign/eligible_products/` | ❌ |  | medium | regress | все | frederick |
| 640 | GET | `/api/boost_campaign/slot_availability/` | ❌ |  | low | regress | все | frederick |
| 641 | GET | `/api/boost_campaign/{id}/` | ❌ |  | low | regress | все | frederick |
| 642 | POST | `/api/boost_campaign/{id}/stop/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 643 | GET | `/api/boost_package/` | ❌ |  | low | regress | все | frederick |
| 644 | GET | `/api/boost_package/{id}/` | ❌ |  | low | regress | все | frederick |
| 645 | GET | `/api/category/` | ❌ |  | low | regress | все | frederick |
| 646 | GET | `/api/category/{slug}/` | ❌ |  | low | regress | все | frederick |
| 647 | POST | `/api/improvement-suggestions/` | ❌ |  | high | regress | dev/qa | frederick |
| 648 | GET | `/api/my_favorites/` | ❌ |  | low | regress | все | frederick |
| 649 | GET | `/api/my_favorites/{id}/` | ❌ |  | low | regress | все | frederick |
| 650 | GET | `/api/my_listings/` | ❌ |  | medium | regress | все | frederick |
| 651 | POST | `/api/my_listings/` | ❌ |  | high | regress | dev/qa | frederick |
| 652 | GET | `/api/my_listings/is_first_listing/` | ❌ |  | medium | regress | все | frederick |
| 653 | GET | `/api/my_listings/{id}/` | ❌ |  | medium | regress | все | frederick |
| 654 | PUT | `/api/my_listings/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 655 | PATCH | `/api/my_listings/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 656 | POST | `/api/my_listings/{id}/deactivate/` | ❌ |  | high | regress | dev/qa | frederick |
| 657 | POST | `/api/my_listings/{id}/manage_price/` | ❌ |  | high | regress | dev/qa | frederick |
| 658 | POST | `/api/my_listings/{id}/publish/` | ❌ |  | high | regress | dev/qa | frederick |
| 659 | POST | `/api/my_listings/{id}/stop_campaign/` | ❌ |  | high | regress | dev/qa | frederick |
| 660 | GET | `/api/my_purchases/` | ❌ |  | low | regress | все | frederick |
| 661 | GET | `/api/my_purchases/cancel_reasons/` | ❌ |  | low | regress | все | frederick |
| 662 | GET | `/api/my_purchases/is_first_purchase/` | ❌ |  | low | regress | все | frederick |
| 663 | GET | `/api/my_purchases/{id}/` | ❌ |  | low | regress | все | frederick |
| 664 | POST | `/api/my_purchases/{id}/add_discussion_message/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 665 | POST | `/api/my_purchases/{id}/cancel/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 666 | GET | `/api/my_purchases/{id}/discussion_messages/` | ❌ |  | low | regress | все | frederick |
| 667 | GET | `/api/my_purchases/{id}/status_logs/` | ❌ |  | low | regress | все | frederick |
| 668 | GET | `/api/my_sales/` | ❌ |  | low | regress | все | frederick |
| 669 | GET | `/api/my_sales/all_statuses/` | ❌ |  | low | regress | все | frederick |
| 670 | GET | `/api/my_sales/cancel_reasons/` | ❌ |  | low | regress | все | frederick |
| 671 | GET | `/api/my_sales/has_sales/` | ❌ |  | low | regress | все | frederick |
| 672 | GET | `/api/my_sales/{id}/` | ❌ |  | low | regress | все | frederick |
| 673 | POST | `/api/my_sales/{id}/accept/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 674 | POST | `/api/my_sales/{id}/add_discussion_message/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 675 | POST | `/api/my_sales/{id}/complete/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 676 | POST | `/api/my_sales/{id}/decline/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 677 | GET | `/api/my_sales/{id}/discussion_messages/` | ❌ |  | low | regress | все | frederick |
| 678 | POST | `/api/my_sales/{id}/send_confirmation_code/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 679 | GET | `/api/my_sales/{id}/status_logs/` | ❌ |  | low | regress | все | frederick |
| 680 | POST | `/api/order/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 681 | POST | `/api/order/confirm/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 682 | POST | `/api/order/create_v2/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 683 | GET | `/api/pickup_location/` | ❌ |  | low | regress | все | frederick |
| 684 | GET | `/api/pickup_location/{id}/` | ❌ |  | low | regress | все | frederick |
| 685 | GET | `/api/product/` | ❌ |  | medium | regress | все | frederick |
| 686 | GET | `/api/product/available_count/` | ❌ |  | medium | regress | все | frederick |
| 687 | GET | `/api/product/{slug}/` | ❌ |  | medium | regress | все | frederick |
| 688 | GET | `/api/product_image/` | ❌ |  | medium | regress | все | frederick |
| 689 | POST | `/api/product_image/` | ❌ |  | high | regress | dev/qa | frederick |
| 690 | GET | `/api/product_image/{id}/` | ❌ |  | medium | regress | все | frederick |
| 691 | GET | `/api/product_like/{id}/dislike/` | ❌ |  | medium | regress | все | frederick |
| 692 | GET | `/api/product_like/{id}/like/` | 🔷 | UI `test_add_popular_listing_to_favorite` | medium | regress | все | frederick |
| 693 | GET | `/api/review/` | ❌ |  | low | regress | все | frederick |
| 694 | POST | `/api/review/` | ❌ |  | high | regress | dev/qa | frederick |
| 695 | POST | `/api/review/create_reply/` | ❌ |  | high | regress | dev/qa | frederick |
| 696 | POST | `/api/review/mark_as_available_in_profile/` | ❌ |  | high | regress | dev/qa | frederick |
| 697 | GET | `/api/review/{id}/` | ❌ |  | low | regress | все | frederick |
| 698 | PUT | `/api/review/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 699 | PATCH | `/api/review/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 700 | GET | `/s/marketplace/api/arm/orders/` | ❌ |  | low | regress | все | — |
| 701 | GET | `/s/marketplace/api/arm/orders/all/` | ❌ |  | low | regress | все | — |
| 702 | GET | `/s/marketplace/api/arm/orders/{id}/` | ❌ |  | low | regress | все | — |
| 703 | GET | `/s/marketplace/api/arm/orders/{id}/all/` | ❌ |  | low | regress | все | — |
| 704 | POST | `/s/marketplace/api/arm/orders/{id}/process_action/` | ❌ |  | low | regress | dev/qa | — |
| 705 | GET | `/s/marketplace/api/arm/products/` | ❌ |  | low | regress | все | — |
| 706 | POST | `/s/marketplace/api/arm/products/` | ❌ |  | low | regress | dev/qa | — |
| 707 | GET | `/s/marketplace/api/arm/products/{id}/` | ❌ |  | low | regress | все | — |
| 708 | PATCH | `/s/marketplace/api/arm/products/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 709 | POST | `/s/marketplace/api/arm/products/{id}/process_action/` | ❌ |  | low | regress | dev/qa | — |
| 710 | POST | `/s/marketplace/api/basket/add/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 711 | POST | `/s/marketplace/api/basket/remove/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 712 | POST | `/s/marketplace/api/basket/set/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 713 | GET | `/s/marketplace/api/boost_campaign/` | ❌ |  | low | regress | все | frederick |
| 714 | POST | `/s/marketplace/api/boost_campaign/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 715 | GET | `/s/marketplace/api/boost_campaign/eligible_products/` | ❌ |  | medium | regress | все | frederick |
| 716 | GET | `/s/marketplace/api/boost_campaign/slot_availability/` | ❌ |  | low | regress | все | frederick |
| 717 | GET | `/s/marketplace/api/boost_campaign/{id}/` | ❌ |  | low | regress | все | frederick |
| 718 | POST | `/s/marketplace/api/boost_campaign/{id}/stop/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 719 | GET | `/s/marketplace/api/boost_package/` | ❌ |  | low | regress | все | frederick |
| 720 | GET | `/s/marketplace/api/boost_package/{id}/` | ❌ |  | low | regress | все | frederick |
| 721 | GET | `/s/marketplace/api/category/` | ❌ |  | low | regress | все | frederick |
| 722 | GET | `/s/marketplace/api/category/{slug}/` | ❌ |  | low | regress | все | frederick |
| 723 | POST | `/s/marketplace/api/improvement-suggestions/` | ❌ |  | high | regress | dev/qa | frederick |
| 724 | GET | `/s/marketplace/api/my_favorites/` | ❌ |  | low | regress | все | frederick |
| 725 | GET | `/s/marketplace/api/my_favorites/{id}/` | ❌ |  | low | regress | все | frederick |
| 726 | GET | `/s/marketplace/api/my_listings/` | ❌ |  | medium | regress | все | frederick |
| 727 | POST | `/s/marketplace/api/my_listings/` | ❌ |  | high | regress | dev/qa | frederick |
| 728 | GET | `/s/marketplace/api/my_listings/is_first_listing/` | ❌ |  | medium | regress | все | frederick |
| 729 | GET | `/s/marketplace/api/my_listings/{id}/` | ❌ |  | medium | regress | все | frederick |
| 730 | PUT | `/s/marketplace/api/my_listings/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 731 | PATCH | `/s/marketplace/api/my_listings/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 732 | POST | `/s/marketplace/api/my_listings/{id}/deactivate/` | ❌ |  | high | regress | dev/qa | frederick |
| 733 | POST | `/s/marketplace/api/my_listings/{id}/manage_price/` | ❌ |  | high | regress | dev/qa | frederick |
| 734 | POST | `/s/marketplace/api/my_listings/{id}/publish/` | ❌ |  | high | regress | dev/qa | frederick |
| 735 | POST | `/s/marketplace/api/my_listings/{id}/stop_campaign/` | ❌ |  | high | regress | dev/qa | frederick |
| 736 | GET | `/s/marketplace/api/my_purchases/` | ❌ |  | low | regress | все | frederick |
| 737 | GET | `/s/marketplace/api/my_purchases/cancel_reasons/` | ❌ |  | low | regress | все | frederick |
| 738 | GET | `/s/marketplace/api/my_purchases/is_first_purchase/` | ❌ |  | low | regress | все | frederick |
| 739 | GET | `/s/marketplace/api/my_purchases/{id}/` | ❌ |  | low | regress | все | frederick |
| 740 | POST | `/s/marketplace/api/my_purchases/{id}/add_discussion_message/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 741 | POST | `/s/marketplace/api/my_purchases/{id}/cancel/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 742 | GET | `/s/marketplace/api/my_purchases/{id}/discussion_messages/` | ❌ |  | low | regress | все | frederick |
| 743 | GET | `/s/marketplace/api/my_purchases/{id}/status_logs/` | ❌ |  | low | regress | все | frederick |
| 744 | GET | `/s/marketplace/api/my_sales/` | ❌ |  | low | regress | все | frederick |
| 745 | GET | `/s/marketplace/api/my_sales/all_statuses/` | ❌ |  | low | regress | все | frederick |
| 746 | GET | `/s/marketplace/api/my_sales/cancel_reasons/` | ❌ |  | low | regress | все | frederick |
| 747 | GET | `/s/marketplace/api/my_sales/has_sales/` | ❌ |  | low | regress | все | frederick |
| 748 | GET | `/s/marketplace/api/my_sales/{id}/` | ❌ |  | low | regress | все | frederick |
| 749 | POST | `/s/marketplace/api/my_sales/{id}/accept/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 750 | POST | `/s/marketplace/api/my_sales/{id}/add_discussion_message/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 751 | POST | `/s/marketplace/api/my_sales/{id}/complete/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 752 | POST | `/s/marketplace/api/my_sales/{id}/decline/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 753 | GET | `/s/marketplace/api/my_sales/{id}/discussion_messages/` | ❌ |  | low | regress | все | frederick |
| 754 | POST | `/s/marketplace/api/my_sales/{id}/send_confirmation_code/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 755 | GET | `/s/marketplace/api/my_sales/{id}/status_logs/` | ❌ |  | low | regress | все | frederick |
| 756 | POST | `/s/marketplace/api/order/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 757 | POST | `/s/marketplace/api/order/confirm/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 758 | POST | `/s/marketplace/api/order/create_v2/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 759 | GET | `/s/marketplace/api/pickup_location/` | ❌ |  | low | regress | все | frederick |
| 760 | GET | `/s/marketplace/api/pickup_location/{id}/` | ❌ |  | low | regress | все | frederick |
| 761 | GET | `/s/marketplace/api/product/` | ❌ |  | medium | regress | все | frederick |
| 762 | GET | `/s/marketplace/api/product/available_count/` | ❌ |  | medium | regress | все | frederick |
| 763 | GET | `/s/marketplace/api/product/{slug}/` | ❌ |  | medium | regress | все | frederick |
| 764 | GET | `/s/marketplace/api/product_image/` | ❌ |  | medium | regress | все | frederick |
| 765 | POST | `/s/marketplace/api/product_image/` | ❌ |  | high | regress | dev/qa | frederick |
| 766 | GET | `/s/marketplace/api/product_image/{id}/` | ❌ |  | medium | regress | все | frederick |
| 767 | GET | `/s/marketplace/api/product_like/{id}/dislike/` | ❌ |  | medium | regress | все | frederick |
| 768 | GET | `/s/marketplace/api/product_like/{id}/like/` | 🔷 | UI `test_add_popular_listing_to_favorite` | medium | regress | все | frederick |
| 769 | GET | `/s/marketplace/api/review/` | ❌ |  | low | regress | все | frederick |
| 770 | POST | `/s/marketplace/api/review/` | ❌ |  | high | regress | dev/qa | frederick |
| 771 | POST | `/s/marketplace/api/review/create_reply/` | ❌ |  | high | regress | dev/qa | frederick |
| 772 | POST | `/s/marketplace/api/review/mark_as_available_in_profile/` | ❌ |  | high | regress | dev/qa | frederick |
| 773 | GET | `/s/marketplace/api/review/{id}/` | ❌ |  | low | regress | все | frederick |
| 774 | PUT | `/s/marketplace/api/review/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 775 | PATCH | `/s/marketplace/api/review/{id}/` | ❌ |  | high | regress | dev/qa | frederick |

## games — геймификация (78)

| № | Метод | Эндпоинт | Статус | Тест | Критичность | Набор | Среда | Ответственный |
|---|---|---|---|---|---|---|---|---|
| 776 | GET | `/api/badge_info/v2/{external_id}/` | ❌ |  | low | regress | все | madina |
| 777 | GET | `/api/badges/v2/` | ❌ |  | low | regress | все | madina |
| 778 | GET | `/api/badges/v2/player/{external_id}/get_displayed/` | ❌ |  | low | regress | все | madina |
| 779 | GET | `/api/badges/v2/remove_from_displayed/{badge_id}/` | ❌ |  | low | regress | все | madina |
| 780 | GET | `/api/badges/v2/set_displayed/{badge_id}/` | ❌ |  | low | regress | все | madina |
| 781 | GET | `/api/brightness/company/{external_id}/` | ❌ |  | medium | regress | все | madina |
| 782 | GET | `/api/brightness/company/{external_id}/top_performers/` | ❌ |  | medium | regress | все | madina |
| 783 | GET | `/api/brightness/player/{external_id}/` | ❌ |  | low | regress | все | madina |
| 784 | GET | `/api/brightness/player/{external_id}/top_performers/` | ❌ |  | low | regress | все | madina |
| 785 | POST | `/api/company/create/` | ❌ |  | high | regress | dev/qa | madina |
| 786 | GET | `/api/company/history/{company_external_id}/{year}/` | ❌ |  | medium | regress | все | madina |
| 787 | GET | `/api/company/leaderboard/` | ❌ |  | medium | regress | все | madina |
| 788 | GET | `/api/company/rating/` | ❌ |  | medium | regress | все | madina |
| 789 | GET | `/api/company/{external_id}/` | ❌ |  | medium | regress | все | madina |
| 790 | GET | `/api/company/{external_id}/statistics/` | ❌ |  | medium | regress | все | madina |
| 791 | GET | `/api/company_player/rating/` | ❌ |  | medium | regress | все | madina |
| 792 | GET | `/api/daily_contribution/info/` | ❌ |  | low | regress | все | madina |
| 793 | GET | `/api/daily_streak/` | ❌ |  | low | regress | все | madina |
| 794 | GET | `/api/daily_streak/claim/` | ❌ |  | low | regress | все | madina |
| 795 | POST | `/api/event/` | ❌ |  | high | regress | dev/qa | madina |
| 796 | GET | `/api/history/{external_id}/` | ❌ |  | low | regress | все | madina |
| 797 | GET | `/api/history/{external_id}/{id}/set_badge_level_viewed/` | ❌ |  | low | regress | все | madina |
| 798 | GET | `/api/history/{external_id}/{id}/set_viewed/` | ❌ |  | low | regress | все | madina |
| 799 | GET | `/api/level_info/` | ❌ |  | low | regress | все | madina |
| 800 | GET | `/api/levels/` | ❌ |  | low | regress | все | madina |
| 801 | GET | `/api/players/` | ❌ |  | low | regress | все | madina |
| 802 | POST | `/api/players/create/` | ❌ |  | high | regress | dev/qa | madina |
| 803 | GET | `/api/players/current_rating/` | ❌ |  | low | regress | все | madina |
| 804 | GET | `/api/players/info/` | ❌ |  | low | regress | все | madina |
| 805 | GET | `/api/players/leaderboard/` | ❌ |  | low | regress | все | madina |
| 806 | GET | `/api/players/rating/` | ❌ |  | low | regress | все | madina |
| 807 | GET | `/api/players/{external_id}/` | ❌ |  | low | regress | все | madina |
| 808 | GET | `/api/quests/` | ❌ |  | low | regress | все | madina |
| 809 | POST | `/api/quests/remove/` | ❌ |  | high | regress | dev/qa | madina |
| 810 | GET | `/api/quests/{quest_id}/claim/` | ❌ |  | low | regress | все | madina |
| 811 | GET | `/api/shine/leaderboard/` | ❌ |  | low | regress | все | madina |
| 812 | GET | `/api/weekly_contribution/` | ❌ |  | low | regress | все | madina |
| 813 | GET | `/api/weekly_contribution/share-coins/` | ❌ |  | low | regress | все | madina |
| 814 | POST | `/api/weekly_contribution/share-coins/` | ❌ |  | high | regress | dev/qa | madina |
| 815 | GET | `/s/games/api/badge_info/v2/{external_id}/` | ❌ |  | low | regress | все | madina |
| 816 | GET | `/s/games/api/badges/v2/` | ❌ |  | low | regress | все | madina |
| 817 | GET | `/s/games/api/badges/v2/player/{external_id}/get_displayed/` | ❌ |  | low | regress | все | madina |
| 818 | GET | `/s/games/api/badges/v2/remove_from_displayed/{badge_id}/` | ❌ |  | low | regress | все | madina |
| 819 | GET | `/s/games/api/badges/v2/set_displayed/{badge_id}/` | ❌ |  | low | regress | все | madina |
| 820 | GET | `/s/games/api/brightness/company/{external_id}/` | ❌ |  | medium | regress | все | madina |
| 821 | GET | `/s/games/api/brightness/company/{external_id}/top_performers/` | ❌ |  | medium | regress | все | madina |
| 822 | GET | `/s/games/api/brightness/player/{external_id}/` | ❌ |  | low | regress | все | madina |
| 823 | GET | `/s/games/api/brightness/player/{external_id}/top_performers/` | ❌ |  | low | regress | все | madina |
| 824 | POST | `/s/games/api/company/create/` | ❌ |  | high | regress | dev/qa | madina |
| 825 | GET | `/s/games/api/company/history/{company_external_id}/{year}/` | ❌ |  | medium | regress | все | madina |
| 826 | GET | `/s/games/api/company/leaderboard/` | ❌ |  | medium | regress | все | madina |
| 827 | GET | `/s/games/api/company/rating/` | ❌ |  | medium | regress | все | madina |
| 828 | GET | `/s/games/api/company/{external_id}/` | ❌ |  | medium | regress | все | madina |
| 829 | GET | `/s/games/api/company/{external_id}/statistics/` | ❌ |  | medium | regress | все | madina |
| 830 | GET | `/s/games/api/company_player/rating/` | ❌ |  | medium | regress | все | madina |
| 831 | GET | `/s/games/api/daily_contribution/info/` | ❌ |  | low | regress | все | madina |
| 832 | GET | `/s/games/api/daily_streak/` | ❌ |  | low | regress | все | madina |
| 833 | GET | `/s/games/api/daily_streak/claim/` | ❌ |  | low | regress | все | madina |
| 834 | POST | `/s/games/api/event/` | ❌ |  | high | regress | dev/qa | madina |
| 835 | GET | `/s/games/api/history/{external_id}/` | ❌ |  | low | regress | все | madina |
| 836 | GET | `/s/games/api/history/{external_id}/{id}/set_badge_level_viewed/` | ❌ |  | low | regress | все | madina |
| 837 | GET | `/s/games/api/history/{external_id}/{id}/set_viewed/` | ❌ |  | low | regress | все | madina |
| 838 | GET | `/s/games/api/level_info/` | ❌ |  | low | regress | все | madina |
| 839 | GET | `/s/games/api/levels/` | ❌ |  | low | regress | все | madina |
| 840 | GET | `/s/games/api/players/` | ❌ |  | low | regress | все | madina |
| 841 | POST | `/s/games/api/players/create/` | ❌ |  | high | regress | dev/qa | madina |
| 842 | GET | `/s/games/api/players/current_rating/` | ❌ |  | low | regress | все | madina |
| 843 | GET | `/s/games/api/players/info/` | ❌ |  | low | regress | все | madina |
| 844 | GET | `/s/games/api/players/leaderboard/` | ❌ |  | low | regress | все | madina |
| 845 | GET | `/s/games/api/players/rating/` | ❌ |  | low | regress | все | madina |
| 846 | GET | `/s/games/api/players/{external_id}/` | ❌ |  | low | regress | все | madina |
| 847 | GET | `/s/games/api/quests/` | ❌ |  | low | regress | все | madina |
| 848 | POST | `/s/games/api/quests/remove/` | ❌ |  | high | regress | dev/qa | madina |
| 849 | GET | `/s/games/api/quests/{quest_id}/claim/` | ❌ |  | low | regress | все | madina |
| 850 | GET | `/s/games/api/shine/leaderboard/` | ❌ |  | low | regress | все | madina |
| 851 | GET | `/s/games/api/weekly_contribution/` | ❌ |  | low | regress | все | madina |
| 852 | GET | `/s/games/api/weekly_contribution/share-coins/` | ❌ |  | low | regress | все | madina |
| 853 | POST | `/s/games/api/weekly_contribution/share-coins/` | ❌ |  | high | regress | dev/qa | madina |

## services — программы (234)

| № | Метод | Эндпоинт | Статус | Тест | Критичность | Набор | Среда | Ответственный |
|---|---|---|---|---|---|---|---|---|
| 854 | GET | `/ru/s/services/service/company-accreditation-requests/` | ❌ |  | medium | regress | все | frederick |
| 855 | GET | `/ru/s/services/service/company-accreditation-requests/{id}/` | ❌ |  | medium | regress | все | frederick |
| 856 | POST | `/ru/s/services/service/external/reconciliation-acts-register/` | ❌ |  | high | regress | dev/qa | frederick |
| 857 | GET | `/ru/s/services/service/external/service_request/` | ❌ |  | medium | regress | все | frederick |
| 858 | POST | `/ru/s/services/service/external/service_request/` | ❌ |  | high | regress | dev/qa | frederick |
| 859 | POST | `/ru/s/services/service/external/service_request/draft/` | ❌ |  | high | regress | dev/qa | frederick |
| 860 | POST | `/ru/s/services/service/external/service_request/xml/` | ❌ |  | high | regress | dev/qa | frederick |
| 861 | GET | `/ru/s/services/service/external/service_request/{id}/` | ❌ |  | medium | regress | все | frederick |
| 862 | PUT | `/ru/s/services/service/external/service_request/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 863 | POST | `/ru/s/services/service/external/service_request/{id}/process/` | ❌ |  | high | regress | dev/qa | frederick |
| 864 | GET | `/ru/s/services/service/favorites/{code}/add_to_favorite/` | ❌ |  | medium | regress | все | frederick |
| 865 | GET | `/ru/s/services/service/favorites/{code}/remove_from_favorite/` | ❌ |  | medium | regress | все | frederick |
| 866 | GET | `/ru/s/services/service/fl-accreditation-requests/` | ❌ |  | medium | regress | все | frederick |
| 867 | GET | `/ru/s/services/service/fl-accreditation-requests/{id}/` | ❌ |  | medium | regress | все | frederick |
| 868 | GET | `/ru/s/services/service/internal-business-process/filter_assignees/` | ❌ |  | low | regress | все | — |
| 869 | GET | `/ru/s/services/service/internal-service-requests/{id}/detail_page_context/` | ❌ |  | low | regress | все | — |
| 870 | GET | `/ru/s/services/service/internal-services/get_field_templates/` | ❌ |  | low | regress | все | — |
| 871 | GET | `/ru/s/services/service/internal-services/{id}/get/` | ❌ |  | low | regress | все | — |
| 872 | POST | `/ru/s/services/service/internal-services/{id}/initial_validation/` | ❌ |  | low | regress | dev/qa | — |
| 873 | GET | `/ru/s/services/service/internal-sr-report/{id}/dispatch_report/` | ❌ |  | low | regress | все | — |
| 874 | POST | `/ru/s/services/service/lerna/subscribe_to_course/` | ❌ |  | high | regress | dev/qa | frederick |
| 875 | GET | `/ru/s/services/service/service/` | ❌ |  | medium | regress | все | frederick |
| 876 | GET | `/ru/s/services/service/service/context/` | ❌ |  | medium | regress | все | frederick |
| 877 | GET | `/ru/s/services/service/service/{code}/` | ❌ |  | medium | regress | все | frederick |
| 878 | GET | `/ru/s/services/service/service/{code}/favorite_add/` | ❌ |  | medium | regress | все | frederick |
| 879 | GET | `/ru/s/services/service/service/{code}/favorite_remove/` | ❌ |  | medium | regress | все | frederick |
| 880 | GET | `/ru/s/services/service/sponsorship/{id}/config/` | ❌ |  | medium | regress | все | frederick |
| 881 | GET | `/ru/s/services/service/techorda-sr-internal/get/` | ❌ |  | medium | regress | все | frederick |
| 882 | GET | `/ru/s/services/service/techpark-internal/` | ❌ |  | medium | regress | все | frederick |
| 883 | GET | `/ru/s/services/service/techpark-startapps/xlsx/` | ❌ |  | medium | regress | все | frederick |
| 884 | PUT | `/s/services/account/api/gup_purchase_application/{id}/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 885 | PATCH | `/s/services/account/api/gup_purchase_application/{id}/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 886 | GET | `/s/services/account/api/gup_purchase_application/{id}/send/` | ❌ |  | medium | regress | все | frederick |
| 887 | PUT | `/s/services/account/api/gup_purchase_plan/{id}/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 888 | PATCH | `/s/services/account/api/gup_purchase_plan/{id}/` | ❌ |  | critical | smoke | dev/qa | frederick |
| 889 | GET | `/s/services/account/api/gup_purchase_plan/{id}/send/` | ❌ |  | medium | regress | все | frederick |
| 890 | PUT | `/s/services/account/api/gup_report/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 891 | PATCH | `/s/services/account/api/gup_report/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 892 | GET | `/s/services/account/api/gup_report/{id}/send/` | ❌ |  | medium | regress | все | frederick |
| 893 | POST | `/s/services/account/api/protected_media_file/` | ❌ |  | high | regress | dev/qa | frederick |
| 894 | GET | `/s/services/account/api/protected_media_file/{id}/` | ❌ |  | medium | regress | все | frederick |
| 895 | POST | `/s/services/account/api/report/` | ❌ |  | high | regress | dev/qa | frederick |
| 896 | PUT | `/s/services/account/api/report/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 897 | PATCH | `/s/services/account/api/report/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 898 | DELETE | `/s/services/account/api/report/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 899 | POST | `/s/services/account/api/report/{id}/sign/` | ❌ |  | high | regress | dev/qa | frederick |
| 900 | GET | `/s/services/account/api/report/{id}/xml/` | ❌ |  | medium | regress | все | frederick |
| 901 | PUT | `/s/services/account/api/seed_money_report/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 902 | PATCH | `/s/services/account/api/seed_money_report/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 903 | POST | `/s/services/account/api/seed_money_report/{id}/sign/` | ❌ |  | high | regress | dev/qa | frederick |
| 904 | GET | `/s/services/account/api/seed_money_report/{id}/xml/` | ❌ |  | medium | regress | все | frederick |
| 905 | GET | `/s/services/account/api/service_request/` | ❌ |  | medium | regress | все | frederick |
| 906 | POST | `/s/services/account/api/service_request/` | ❌ |  | high | regress | dev/qa | frederick |
| 907 | GET | `/s/services/account/api/service_request/{id}/` | ❌ |  | medium | regress | все | frederick |
| 908 | PUT | `/s/services/account/api/service_request/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 909 | PATCH | `/s/services/account/api/service_request/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 910 | GET | `/s/services/account/api/service_request/{id}/certificate/` | ❌ |  | medium | regress | все | frederick |
| 911 | GET | `/s/services/account/api/service_request/{id}/delete/` | ❌ |  | medium | regress | все | frederick |
| 912 | GET | `/s/services/account/api/service_request/{id}/egov_info/{uuid_param}/` | ❌ |  | medium | regress | все | frederick |
| 913 | GET | `/s/services/account/api/service_request/{id}/egov_sign/{uuid_param}/` | ❌ |  | medium | regress | все | frederick |
| 914 | PUT | `/s/services/account/api/service_request/{id}/egov_sign/{uuid_param}/` | ❌ |  | high | regress | dev/qa | frederick |
| 915 | GET | `/s/services/account/api/service_request/{id}/egov_sign_uri/` | ❌ |  | medium | regress | все | frederick |
| 916 | GET | `/s/services/account/api/service_request/{id}/pdf/` | ❌ |  | medium | regress | все | frederick |
| 917 | GET | `/s/services/account/api/service_request/{id}/revoke/` | ❌ |  | medium | regress | все | frederick |
| 918 | GET | `/s/services/account/api/service_request/{id}/send/` | ❌ |  | medium | regress | все | frederick |
| 919 | POST | `/s/services/account/api/service_request/{id}/sign/` | ❌ |  | high | regress | dev/qa | frederick |
| 920 | GET | `/s/services/account/api/service_request/{id}/xml/` | ❌ |  | medium | regress | все | frederick |
| 921 | PUT | `/s/services/account/api/techorda_report/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 922 | PATCH | `/s/services/account/api/techorda_report/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 923 | DELETE | `/s/services/account/api/techorda_report/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 924 | POST | `/s/services/account/api/techorda_report/{id}/sign/` | ❌ |  | high | regress | dev/qa | frederick |
| 925 | GET | `/s/services/account/api/techorda_report/{id}/xml/` | ❌ |  | medium | regress | все | frederick |
| 926 | PUT | `/s/services/account/api/techorda_report_student/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 927 | PATCH | `/s/services/account/api/techorda_report_student/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 928 | POST | `/s/services/account/api/techorda_report_student/{id}/sign/` | ❌ |  | high | regress | dev/qa | frederick |
| 929 | GET | `/s/services/account/api/techorda_report_student/{id}/xml/` | ❌ |  | medium | regress | все | frederick |
| 930 | GET | `/s/services/arm/dashboard/techpark-monitoring/` | ❌ |  | low | regress | все | — |
| 931 | POST | `/s/services/arm/expert_document/` | ❌ |  | low | regress | dev/qa | — |
| 932 | GET | `/s/services/arm/expertise/` | ❌ |  | low | regress | все | — |
| 933 | GET | `/s/services/arm/expertise/{id}/` | ❌ |  | low | regress | все | — |
| 934 | GET | `/s/services/arm/expertise/{id}/correction/` | ❌ |  | low | regress | все | — |
| 935 | GET | `/s/services/arm/expertise/{id}/verify/` | ❌ |  | low | regress | все | — |
| 936 | GET | `/s/services/arm/external_document/` | ❌ |  | low | regress | все | — |
| 937 | POST | `/s/services/arm/external_document/` | ❌ |  | low | regress | dev/qa | — |
| 938 | GET | `/s/services/arm/external_document/correspondents/` | ❌ |  | low | regress | все | — |
| 939 | GET | `/s/services/arm/external_document/{external_id}/` | ❌ |  | low | regress | все | — |
| 940 | GET | `/s/services/arm/external_document/{external_id}/refresh/` | ❌ |  | low | regress | все | — |
| 941 | GET | `/s/services/arm/extra_document/` | ❌ |  | low | regress | все | — |
| 942 | POST | `/s/services/arm/extra_document/` | ❌ |  | low | regress | dev/qa | — |
| 943 | GET | `/s/services/arm/extra_document/{id}/` | ❌ |  | low | regress | все | — |
| 944 | GET | `/s/services/arm/gup_purchase_application/` | ❌ |  | low | regress | все | — |
| 945 | GET | `/s/services/arm/gup_purchase_application/{id}/` | ❌ |  | low | regress | все | — |
| 946 | PUT | `/s/services/arm/gup_purchase_application/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 947 | PATCH | `/s/services/arm/gup_purchase_application/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 948 | POST | `/s/services/arm/gup_purchase_application/{id}/approve/` | ❌ |  | low | regress | dev/qa | — |
| 949 | POST | `/s/services/arm/gup_purchase_application/{id}/correction/` | ❌ |  | low | regress | dev/qa | — |
| 950 | GET | `/s/services/arm/gup_purchase_application/{id}/download/` | ❌ |  | low | regress | все | — |
| 951 | GET | `/s/services/arm/gup_purchase_application/{id}/xls/` | ❌ |  | low | regress | все | — |
| 952 | GET | `/s/services/arm/gup_purchase_plan/` | ❌ |  | low | regress | все | — |
| 953 | GET | `/s/services/arm/gup_purchase_plan/{id}/` | ❌ |  | low | regress | все | — |
| 954 | GET | `/s/services/arm/gup_purchase_plan/{id}/approve/` | ❌ |  | low | regress | все | — |
| 955 | POST | `/s/services/arm/gup_purchase_plan/{id}/correction/` | ❌ |  | low | regress | dev/qa | — |
| 956 | GET | `/s/services/arm/gup_purchase_plan/{id}/xls/` | ❌ |  | low | regress | все | — |
| 957 | GET | `/s/services/arm/gup_report/` | ❌ |  | low | regress | все | — |
| 958 | GET | `/s/services/arm/gup_report/{id}/` | ❌ |  | low | regress | все | — |
| 959 | POST | `/s/services/arm/gup_report/{id}/approve/` | ❌ |  | low | regress | dev/qa | — |
| 960 | POST | `/s/services/arm/gup_report/{id}/correction/` | ❌ |  | low | regress | dev/qa | — |
| 961 | GET | `/s/services/arm/gup_report/{id}/download/` | ❌ |  | low | regress | все | — |
| 962 | GET | `/s/services/arm/hub_form/` | ❌ |  | low | regress | все | — |
| 963 | POST | `/s/services/arm/hub_form/` | ❌ |  | low | regress | dev/qa | — |
| 964 | GET | `/s/services/arm/hub_form/{id}/` | ❌ |  | low | regress | все | — |
| 965 | PUT | `/s/services/arm/hub_form/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 966 | PATCH | `/s/services/arm/hub_form/{id}/` | ❌ |  | low | regress | dev/qa | — |
| 967 | POST | `/s/services/arm/hub_form/{id}/copy/` | ❌ |  | low | regress | dev/qa | — |
| 968 | GET | `/s/services/arm/hub_form/{id}/export_form/` | ❌ |  | low | regress | все | — |
| 969 | POST | `/s/services/arm/hub_form/{id}/import_form/` | ❌ |  | low | regress | dev/qa | — |
| 970 | POST | `/s/services/arm/login/` | ❌ |  | low | regress | dev/qa | — |
| 971 | GET | `/s/services/arm/niokr_executors/` | ❌ |  | low | regress | все | — |
| 972 | GET | `/s/services/arm/niokr_executors/{id}/` | ❌ |  | low | regress | все | — |
| 973 | GET | `/s/services/arm/niokr_notifications/` | ❌ |  | low | regress | все | — |
| 974 | GET | `/s/services/arm/niokr_notifications/{id}/` | ❌ |  | low | regress | все | — |
| 975 | GET | `/s/services/arm/niokr_projects/` | ❌ |  | low | regress | все | — |
| 976 | GET | `/s/services/arm/niokr_projects/{id}/` | ❌ |  | low | regress | все | — |
| 977 | GET | `/s/services/arm/niokr_subsoil_companies/` | ❌ |  | low | regress | все | — |
| 978 | GET | `/s/services/arm/niokr_subsoil_companies/by-bin/{tin}/projects/` | ❌ |  | low | regress | все | — |
| 979 | GET | `/s/services/arm/niokr_subsoil_companies/{id}/` | ❌ |  | low | regress | все | — |
| 980 | GET | `/s/services/arm/protocol/` | ❌ |  | low | regress | все | — |
| 981 | GET | `/s/services/arm/protocol/info/` | ❌ |  | low | regress | все | — |
| 982 | GET | `/s/services/arm/protocol/initiate/` | ❌ |  | low | regress | все | — |
| 983 | GET | `/s/services/arm/protocol/{id}/` | ❌ |  | low | regress | все | — |
| 984 | POST | `/s/services/arm/protocol/{id}/load_algorythm/` | ❌ |  | low | regress | dev/qa | — |
| 985 | GET | `/s/services/arm/protocol/{id}/pdf/` | ❌ |  | low | regress | все | — |
| 986 | POST | `/s/services/arm/protocol/{id}/sign/` | ❌ |  | low | regress | dev/qa | — |
| 987 | GET | `/s/services/arm/protocol/{id}/xml/` | ❌ |  | low | regress | все | — |
| 988 | GET | `/s/services/arm/reconciliation-acts-register/` | ❌ |  | low | regress | все | — |
| 989 | GET | `/s/services/arm/reconciliation-acts-register/export-csv/` | ❌ |  | low | regress | все | — |
| 990 | POST | `/s/services/arm/reconciliation-acts-register/export-zip/` | ❌ |  | low | regress | dev/qa | — |
| 991 | GET | `/s/services/arm/reconciliation-acts-register/{id}/` | ❌ |  | low | regress | все | — |
| 992 | POST | `/s/services/arm/reconciliation-acts-register/{id}/upload-file/` | ❌ |  | low | regress | dev/qa | — |
| 993 | GET | `/s/services/arm/report/` | ❌ |  | low | regress | все | — |
| 994 | POST | `/s/services/arm/report/xls/` | ❌ |  | low | regress | dev/qa | — |
| 995 | GET | `/s/services/arm/report/{id}/` | ❌ |  | low | regress | все | — |
| 996 | GET | `/s/services/arm/seed_money_report/` | ❌ |  | low | regress | все | — |
| 997 | GET | `/s/services/arm/seed_money_report/xls/` | ❌ |  | low | regress | все | — |
| 998 | GET | `/s/services/arm/seed_money_report/{id}/` | ❌ |  | low | regress | все | — |
| 999 | GET | `/s/services/arm/seed_money_report/{id}/approve/` | ❌ |  | low | regress | все | — |
| 1000 | POST | `/s/services/arm/seed_money_report/{id}/correction/` | ❌ |  | low | regress | dev/qa | — |
| 1001 | POST | `/s/services/arm/seed_money_report/{id}/reject/` | ❌ |  | low | regress | dev/qa | — |
| 1002 | GET | `/s/services/arm/service/` | ❌ |  | low | regress | все | — |
| 1003 | POST | `/s/services/arm/service/` | ❌ |  | low | regress | dev/qa | — |
| 1004 | GET | `/s/services/arm/service/context/` | ❌ |  | low | regress | все | — |
| 1005 | GET | `/s/services/arm/service/{code}/` | ❌ |  | low | regress | все | — |
| 1006 | PUT | `/s/services/arm/service/{code}/` | ❌ |  | low | regress | dev/qa | — |
| 1007 | PATCH | `/s/services/arm/service/{code}/` | ❌ |  | low | regress | dev/qa | — |
| 1008 | GET | `/s/services/arm/service/{code}/available/` | ❌ |  | low | regress | все | — |
| 1009 | GET | `/s/services/arm/service/{code}/default_actions/` | ❌ |  | low | regress | все | — |
| 1010 | POST | `/s/services/arm/service/{code}/default_actions/` | ❌ |  | low | regress | dev/qa | — |
| 1011 | GET | `/s/services/arm/service/{code}/export_techpark_votes/` | ❌ |  | low | regress | все | — |
| 1012 | GET | `/s/services/arm/service/{code}/export_xls_by_action/` | ❌ |  | low | regress | все | — |
| 1013 | GET | `/s/services/arm/service/{code}/publish/` | ❌ |  | low | regress | все | — |
| 1014 | POST | `/s/services/arm/service/{code}/report/` | ❌ |  | low | regress | dev/qa | — |
| 1015 | GET | `/s/services/arm/service/{code}/unavailable/` | ❌ |  | low | regress | все | — |
| 1016 | GET | `/s/services/arm/service/{code}/unpublish/` | ❌ |  | low | regress | все | — |
| 1017 | GET | `/s/services/arm/service_monitorning/` | ❌ |  | low | regress | все | — |
| 1018 | GET | `/s/services/arm/service_monitorning/xls/` | ❌ |  | low | regress | все | — |
| 1019 | GET | `/s/services/arm/service_monitorning/{code}/` | ❌ |  | low | regress | все | — |
| 1020 | GET | `/s/services/arm/service_note/` | ❌ |  | low | regress | все | — |
| 1021 | POST | `/s/services/arm/service_note/` | ❌ |  | low | regress | dev/qa | — |
| 1022 | GET | `/s/services/arm/service_note/{id}/` | ❌ |  | low | regress | все | — |
| 1023 | GET | `/s/services/arm/service_request/` | ❌ |  | low | regress | все | — |
| 1024 | POST | `/s/services/arm/service_request/send_notifications/` | ❌ |  | low | regress | dev/qa | — |
| 1025 | POST | `/s/services/arm/service_request/set_pitching/` | ❌ |  | low | regress | dev/qa | — |
| 1026 | POST | `/s/services/arm/service_request/validate_companies/` | ❌ |  | low | regress | dev/qa | — |
| 1027 | GET | `/s/services/arm/service_request/{id}/` | ❌ |  | low | regress | все | — |
| 1028 | GET | `/s/services/arm/service_request/{id}/download/` | ❌ |  | low | regress | все | — |
| 1029 | GET | `/s/services/arm/service_request/{id}/pdf/` | ❌ |  | low | regress | все | — |
| 1030 | POST | `/s/services/arm/service_request/{id}/process_action/` | ❌ |  | low | regress | dev/qa | — |
| 1031 | GET | `/s/services/arm/service_request/{id}/related_service_requests/` | ❌ |  | low | regress | все | — |
| 1032 | POST | `/s/services/arm/service_request/{id}/reveal_hidden_field/` | ❌ |  | low | regress | dev/qa | — |
| 1033 | POST | `/s/services/arm/service_request/{id}/run_ai_moderation/` | ❌ |  | low | regress | dev/qa | — |
| 1034 | POST | `/s/services/arm/service_roles/{code}/add_role_user/` | ❌ |  | low | regress | dev/qa | — |
| 1035 | POST | `/s/services/arm/service_roles/{code}/change_role_user/` | ❌ |  | low | regress | dev/qa | — |
| 1036 | POST | `/s/services/arm/service_roles/{code}/remove_role_user/` | ❌ |  | low | regress | dev/qa | — |
| 1037 | GET | `/s/services/arm/service_roles/{code}/roles/` | ❌ |  | low | regress | все | — |
| 1038 | GET | `/s/services/arm/service_roles/{code}/users/` | ❌ |  | low | regress | все | — |
| 1039 | GET | `/s/services/arm/techorda_report/` | ❌ |  | low | regress | все | — |
| 1040 | GET | `/s/services/arm/techorda_report/xls/` | ❌ |  | low | regress | все | — |
| 1041 | GET | `/s/services/arm/techorda_report/{id}/` | ❌ |  | low | regress | все | — |
| 1042 | GET | `/s/services/arm/techorda_report/{id}/approve/` | ❌ |  | low | regress | все | — |
| 1043 | POST | `/s/services/arm/techorda_report/{id}/correction/` | ❌ |  | low | regress | dev/qa | — |
| 1044 | GET | `/s/services/arm/techorda_report_student/` | ❌ |  | low | regress | все | — |
| 1045 | GET | `/s/services/arm/techorda_report_student/{id}/` | ❌ |  | low | regress | все | — |
| 1046 | GET | `/s/services/arm/techorda_student/` | ❌ |  | low | regress | все | — |
| 1047 | POST | `/s/services/arm/techorda_student/delete/` | ❌ |  | low | regress | dev/qa | — |
| 1048 | POST | `/s/services/arm/techorda_student/upload_csv/` | ❌ |  | low | regress | dev/qa | — |
| 1049 | POST | `/s/services/arm/techorda_student/upload_xls/` | ❌ |  | low | regress | dev/qa | — |
| 1050 | GET | `/s/services/arm/techorda_student/xls/` | ❌ |  | low | regress | все | — |
| 1051 | GET | `/s/services/arm/techorda_student/{id}/` | ❌ |  | low | regress | все | — |
| 1052 | GET | `/s/services/arm/user/` | ❌ |  | low | regress | все | — |
| 1053 | GET | `/s/services/arm/user/{id}/` | ❌ |  | low | regress | все | — |
| 1054 | POST | `/s/services/niokr/upload_projects/` | ❌ |  | high | regress | dev/qa | frederick |
| 1055 | GET | `/s/services/service/api/company-accreditation-requests/` | ❌ |  | medium | regress | все | frederick |
| 1056 | GET | `/s/services/service/api/company-accreditation-requests/{id}/` | ❌ |  | medium | regress | все | frederick |
| 1057 | POST | `/s/services/service/api/external/reconciliation-acts-register/` | ❌ |  | high | regress | dev/qa | frederick |
| 1058 | GET | `/s/services/service/api/external/service_request/` | ❌ |  | medium | regress | все | frederick |
| 1059 | POST | `/s/services/service/api/external/service_request/` | ❌ |  | high | regress | dev/qa | frederick |
| 1060 | POST | `/s/services/service/api/external/service_request/draft/` | ❌ |  | high | regress | dev/qa | frederick |
| 1061 | POST | `/s/services/service/api/external/service_request/xml/` | ❌ |  | high | regress | dev/qa | frederick |
| 1062 | GET | `/s/services/service/api/external/service_request/{id}/` | ❌ |  | medium | regress | все | frederick |
| 1063 | PUT | `/s/services/service/api/external/service_request/{id}/` | ❌ |  | high | regress | dev/qa | frederick |
| 1064 | POST | `/s/services/service/api/external/service_request/{id}/process/` | ❌ |  | high | regress | dev/qa | frederick |
| 1065 | GET | `/s/services/service/api/favorites/{code}/add_to_favorite/` | ❌ |  | medium | regress | все | frederick |
| 1066 | GET | `/s/services/service/api/favorites/{code}/remove_from_favorite/` | ❌ |  | medium | regress | все | frederick |
| 1067 | GET | `/s/services/service/api/fl-accreditation-requests/` | ❌ |  | medium | regress | все | frederick |
| 1068 | GET | `/s/services/service/api/fl-accreditation-requests/{id}/` | ❌ |  | medium | regress | все | frederick |
| 1069 | GET | `/s/services/service/api/internal-business-process/filter_assignees/` | ❌ |  | low | regress | все | — |
| 1070 | GET | `/s/services/service/api/internal-service-requests/{id}/detail_page_context/` | ❌ |  | low | regress | все | — |
| 1071 | GET | `/s/services/service/api/internal-services/get_field_templates/` | ❌ |  | low | regress | все | — |
| 1072 | GET | `/s/services/service/api/internal-services/{id}/get/` | ❌ |  | low | regress | все | — |
| 1073 | POST | `/s/services/service/api/internal-services/{id}/initial_validation/` | ❌ |  | low | regress | dev/qa | — |
| 1074 | GET | `/s/services/service/api/internal-sr-report/{id}/dispatch_report/` | ❌ |  | low | regress | все | — |
| 1075 | POST | `/s/services/service/api/lerna/subscribe_to_course/` | ❌ |  | high | regress | dev/qa | frederick |
| 1076 | GET | `/s/services/service/api/service/` | ❌ |  | medium | regress | все | frederick |
| 1077 | GET | `/s/services/service/api/service/context/` | ❌ |  | medium | regress | все | frederick |
| 1078 | GET | `/s/services/service/api/service/{code}/` | ❌ |  | medium | regress | все | frederick |
| 1079 | GET | `/s/services/service/api/service/{code}/favorite_add/` | ❌ |  | medium | regress | все | frederick |
| 1080 | GET | `/s/services/service/api/service/{code}/favorite_remove/` | ❌ |  | medium | regress | все | frederick |
| 1081 | GET | `/s/services/service/api/sponsorship/{id}/config/` | ❌ |  | medium | regress | все | frederick |
| 1082 | GET | `/s/services/service/api/techorda-sr-internal/get/` | ❌ |  | medium | regress | все | frederick |
| 1083 | GET | `/s/services/service/api/techpark-internal/` | ❌ |  | medium | regress | все | frederick |
| 1084 | GET | `/s/services/service/api/techpark-startapps/xlsx/` | ❌ |  | medium | regress | все | frederick |
| 1085 | GET | `/s/services/shared/api/context_data/` | ❌ |  | medium | regress | все | frederick |
| 1086 | GET | `/s/services/shared/api/context_data/{code}/` | ❌ |  | medium | regress | все | frederick |
| 1087 | POST | `/s/services/shared/convert-excel-to-json/` | ❌ |  | high | regress | dev/qa | frederick |

## mobihub — мобильное приложение (62)

| № | Метод | Эндпоинт | Статус | Тест | Критичность | Набор | Среда | Ответственный |
|---|---|---|---|---|---|---|---|---|
| 1088 | GET | `/s/mobihub/api/bottom-sheets/` | ❌ |  | low | regress | все | aidar |
| 1089 | GET | `/s/mobihub/api/bottom-sheets/{id}/` | ❌ |  | low | regress | все | aidar |
| 1090 | POST | `/s/mobihub/api/bottom-sheets/{id}/view/` | ❌ |  | high | regress | dev/qa | aidar |
| 1091 | GET | `/s/mobihub/api/events/` | ❌ |  | medium | regress | все | aidar |
| 1092 | GET | `/s/mobihub/api/events/{event_code}/` | ❌ |  | medium | regress | все | aidar |
| 1093 | GET | `/s/mobihub/api/events/{event_code}/broadcasts/` | ❌ |  | medium | regress | все | aidar |
| 1094 | GET | `/s/mobihub/api/events/{event_code}/broadcasts/{id}/` | ❌ |  | medium | regress | все | aidar |
| 1095 | GET | `/s/mobihub/api/events/{event_code}/companies/` | ❌ |  | medium | regress | все | aidar |
| 1096 | GET | `/s/mobihub/api/events/{event_code}/companies/{id}/` | ❌ |  | medium | regress | все | aidar |
| 1097 | POST | `/s/mobihub/api/events/{event_code}/companies/{id}/favorite_add/` | ❌ |  | high | regress | dev/qa | aidar |
| 1098 | POST | `/s/mobihub/api/events/{event_code}/companies/{id}/favorite_remove/` | ❌ |  | high | regress | dev/qa | aidar |
| 1099 | GET | `/s/mobihub/api/events/{event_code}/company-categories/` | ❌ |  | medium | regress | все | aidar |
| 1100 | GET | `/s/mobihub/api/events/{event_code}/company-categories/{id}/` | ❌ |  | medium | regress | все | aidar |
| 1101 | GET | `/s/mobihub/api/events/{event_code}/instruction/` | ❌ |  | medium | regress | все | aidar |
| 1102 | GET | `/s/mobihub/api/events/{event_code}/program-categories/` | ❌ |  | medium | regress | все | aidar |
| 1103 | GET | `/s/mobihub/api/events/{event_code}/program-categories/{id}/` | ❌ |  | medium | regress | все | aidar |
| 1104 | GET | `/s/mobihub/api/events/{event_code}/programs/` | ❌ |  | medium | regress | все | aidar |
| 1105 | GET | `/s/mobihub/api/events/{event_code}/programs/filter-options/` | ❌ |  | medium | regress | все | aidar |
| 1106 | GET | `/s/mobihub/api/events/{event_code}/programs/{id}/` | ❌ |  | medium | regress | все | aidar |
| 1107 | POST | `/s/mobihub/api/events/{event_code}/programs/{id}/favorite_add/` | ❌ |  | high | regress | dev/qa | aidar |
| 1108 | POST | `/s/mobihub/api/events/{event_code}/programs/{id}/favorite_remove/` | ❌ |  | high | regress | dev/qa | aidar |
| 1109 | GET | `/s/mobihub/api/events/{event_code}/rooms/` | ❌ |  | medium | regress | все | aidar |
| 1110 | GET | `/s/mobihub/api/events/{event_code}/rooms/{id}/` | ❌ |  | medium | regress | все | aidar |
| 1111 | GET | `/s/mobihub/api/events/{event_code}/schemas/` | ❌ |  | medium | regress | все | aidar |
| 1112 | GET | `/s/mobihub/api/events/{event_code}/schemas/{id}/` | ❌ |  | medium | regress | все | aidar |
| 1113 | GET | `/s/mobihub/api/events/{event_code}/speakers/` | ❌ |  | medium | regress | все | aidar |
| 1114 | GET | `/s/mobihub/api/events/{event_code}/speakers/{id}/` | ❌ |  | medium | regress | все | aidar |
| 1115 | POST | `/s/mobihub/api/events/{event_code}/speakers/{id}/favorite_add/` | ❌ |  | high | regress | dev/qa | aidar |
| 1116 | POST | `/s/mobihub/api/events/{event_code}/speakers/{id}/favorite_remove/` | ❌ |  | high | regress | dev/qa | aidar |
| 1117 | GET | `/s/mobihub/api/events/{event_code}/sponsor-groups/` | ❌ |  | medium | regress | все | aidar |
| 1118 | GET | `/s/mobihub/api/events/{event_code}/sponsor-groups/{id}/` | ❌ |  | medium | regress | все | aidar |
| 1119 | GET | `/s/mobihub/api/game/` | ❌ |  | low | regress | все | aidar |
| 1120 | GET | `/s/mobihub/api/game/{id}/` | ❌ |  | low | regress | все | aidar |
| 1121 | GET | `/s/mobihub/api/game/{id}/accrual_history/` | ❌ |  | low | regress | все | aidar |
| 1122 | GET | `/s/mobihub/api/game/{id}/check_registration/` | ❌ |  | low | regress | все | aidar |
| 1123 | GET | `/s/mobihub/api/game/{id}/game_result/` | ❌ |  | low | regress | все | aidar |
| 1124 | GET | `/s/mobihub/api/game/{id}/knowledge_base/` | ❌ |  | low | regress | все | aidar |
| 1125 | GET | `/s/mobihub/api/game/{id}/leaderboard/` | ❌ |  | low | regress | все | aidar |
| 1126 | GET | `/s/mobihub/api/game/{id}/onboarding/` | ❌ |  | low | regress | все | aidar |
| 1127 | POST | `/s/mobihub/api/game/{id}/onboarding/view/` | ❌ |  | high | regress | dev/qa | aidar |
| 1128 | GET | `/s/mobihub/api/game/{id}/progress/` | ❌ |  | low | regress | все | aidar |
| 1129 | GET | `/s/mobihub/api/game/{id}/quiz_backgrounds/` | ❌ |  | low | regress | все | aidar |
| 1130 | GET | `/s/mobihub/api/game/{id}/referrals/` | ❌ |  | low | regress | все | aidar |
| 1131 | POST | `/s/mobihub/api/game/{id}/referrals/activate/` | ❌ |  | high | regress | dev/qa | aidar |
| 1132 | GET | `/s/mobihub/api/game/{id}/referrals/config/` | ❌ |  | low | regress | все | aidar |
| 1133 | POST | `/s/mobihub/api/game/{id}/referrals/validate/` | ❌ |  | high | regress | dev/qa | aidar |
| 1134 | POST | `/s/mobihub/api/game/{id}/register/` | ❌ |  | high | regress | dev/qa | aidar |
| 1135 | GET | `/s/mobihub/api/game/{id}/rules/` | ❌ |  | low | regress | все | aidar |
| 1136 | GET | `/s/mobihub/api/home-banners/` | ❌ |  | low | regress | все | aidar |
| 1137 | GET | `/s/mobihub/api/qr/make/` | ❌ |  | low | regress | все | aidar |
| 1138 | GET | `/s/mobihub/api/quiz/` | ❌ |  | low | regress | все | aidar |
| 1139 | GET | `/s/mobihub/api/quiz/{id}/` | ❌ |  | low | regress | все | aidar |
| 1140 | POST | `/s/mobihub/api/quiz/{id}/complete_quiz/` | ❌ |  | high | regress | dev/qa | aidar |
| 1141 | GET | `/s/mobihub/api/quiz/{quiz_pk}/questions/` | ❌ |  | low | regress | все | aidar |
| 1142 | GET | `/s/mobihub/api/quiz/{quiz_pk}/questions/{id}/` | ❌ |  | low | regress | все | aidar |
| 1143 | POST | `/s/mobihub/api/quiz/{quiz_pk}/questions/{id}/store_answer/` | ❌ |  | high | regress | dev/qa | aidar |
| 1144 | GET | `/s/mobihub/api/schema/` | ❌ |  | low | regress | все | aidar |
| 1145 | GET | `/s/mobihub/api/shared/context_data/` | ❌ |  | low | regress | все | aidar |
| 1146 | GET | `/s/mobihub/api/shared/context_data/{key}/` | ❌ |  | low | regress | все | aidar |
| 1147 | GET | `/s/mobihub/api/story-groups/` | ❌ |  | low | regress | все | aidar |
| 1148 | GET | `/s/mobihub/api/story-groups/{id}/` | ❌ |  | low | regress | все | aidar |
| 1149 | POST | `/s/mobihub/api/story-groups/{id}/view/` | ❌ |  | high | regress | dev/qa | aidar |

---

## Итого

| Раздел | Эндпоинтов | ✅ | 🔷 | ❌ |
|---|---|---|---|---|
| auth — Auth API | 43 | 1 | 5 | 37 |
| techhub — публичное API | 70 | 1 | 0 | 69 |
| techhub — кабинет (/account/api/) | 199 | 1 | 9 | 189 |
| techhub — прочие модули | 95 | 0 | 1 | 94 |
| techhub — АРМ (админка) | 216 | 0 | 0 | 216 |
| marketplace — Hub Market | 152 | 0 | 2 | 150 |
| games — геймификация | 78 | 0 | 0 | 78 |
| services — программы | 234 | 0 | 0 | 234 |
| mobihub — мобильное приложение | 62 | 0 | 0 | 62 |
| **Всего** | **1149** | **3** | **17** | **1129** |

По критичности: critical — 48 (= smoke-набор) · high — 247 · medium — 238 · low — 616

АРМ (`—` в ответственных) — отдельный скоуп: нужен админ-токен.
Соцлогины (google/apple) и ЭЦП/eGov требуют внешних зависимостей.
