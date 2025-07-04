- Tanzu Mission Control Self Managed는 크게 Active Directory(LDAP 포함)과 OIDC 방식 두 가지에 대한 인증 통합을 제공하고 있습니다.
- 이 가이드에는 단독형 Keycloak 오픈소스를 K8s에 배포하고, 다른 ID 공급자 연결이 아닌 독립 ID 공급자로 사용하는 방법을 제공합니다. (Production 환경에서는 keycloak 사이트의 내용을 참고하여, 가용성 유지 및 S3 스토리지 백업을 고려해야 합니다.)

### Keycloak 환경 설정

User 메뉴에서 admin user를 생성합니다.

![image.png](attachment:e5ba3937-8ea9-45bb-b345-024ba6e03632:image.png)

Credentials 탭으로 이동하여, Password reset을 진행합니다.

![image.png](attachment:b97314f6-a113-404e-a9a8-2fe95d226a4f:image.png)

Role mapping 탭으로 이동해서 Assign role을 클릭합니다.

![image.png](attachment:2f3e492b-bab0-4a0e-af7e-a91d61522c1f:image.png)

“Filter by realm roles”로 변경 후, default-roles-master를 할당합니다.

![image.png](attachment:f9b2fead-cef7-4fa8-8851-d4fe977e9b13:image.png)

**Client Scope 설정**

client scope로 이동하여, 신규 Client Scope을 생성합니다.

1. client scopes - Create client scope

![image.png](attachment:208b9f0e-fde3-480a-be4b-7e3f2773ccdb:image.png)

Name: groups

Type: Default

Display on consent screen: On

Include in token scope: On

![image.png](attachment:cbcf9654-bda3-4590-95e7-e1586b6df95d:image.png)

Mappers 탭을 클릭 - Add predefined mapper를 클릭

![image.png](attachment:ed56e10b-91af-4aa5-9b9b-5acacc7d3229:image.png)

groups을 검색하여 추가합니다.

![image.png](attachment:d3727662-c9ac-4c08-a843-93249d1f7268:image.png)

생성한 mapper groups을 클릭하고, 아래와 같이 설정 구성합니다.

![image.png](attachment:67b8d718-03c7-4f2f-b8dc-f2cc7e242e4d:image.png)

**Realm roles 설정**

1. 메인 메뉴의 Realm roles을 선택하고, Create role을 클릭합니다.

![image.png](attachment:7949106a-bb86-4630-95f3-09509d0574eb:image.png)

role name으로 tmc:admin과 tmc:member를 생성합니다.

![image.png](attachment:f8c0e393-1390-4c19-a86b-e5b76b58a3cd:image.png)

![image.png](attachment:a4eaff47-2bf6-424a-a66d-9d9e175b36fd:image.png)

**Users - 사용자 추가**

메인 메뉴에서 Users를 선택하고, Add user를 클릭합니다.

![image.png](attachment:5651f48e-ee61-484d-9a36-8b121a7a47e0:image.png)

관리자 및 사용자를 추가 합니다.

- tmcadmin, tmcuser01, tmcuser02, etc…

![image.png](attachment:c311ec2d-5e68-4857-a513-badc74e1ce67:image.png)

사용자를 생성하고, Set password을 클릭해서 암호를 설정합니다.

![image.png](attachment:afc4aa74-c9e6-4134-a276-dd18f91e5f62:image.png)

![image.png](attachment:b87e310f-bce1-4fa1-ac42-0624fc604169:image.png)

**Groups 설정**

메인 메뉴의 Groups을 선택하고, Create group을 클릭합니다.

![image.png](attachment:a78ab7aa-3e94-49ea-b27f-13fb2ddf641a:image.png)

Group명을 tmc:admin, tmc:member로 추가 설정합니다.

- 여러 그룹을 사용할 경우, 각 그룹을 모두 생성합니다.

![image.png](attachment:0a16935e-a49d-4ff7-917b-1ff6db54369f:image.png)

생성된 그룹에 알맞은 사용자를 Add member를 클릭하여, 추가합니다.

![image.png](attachment:1c799845-00ac-4cb2-b0fd-3f4e8f1a4698:image.png)

사용자를 선택하고 Add 버튼을 클릭합니다.

![image.png](attachment:2cc00ed5-202b-4469-8ae1-a60dfbcf7854:image.png)

그룹의 Role mapping 탭을 선택합니다.

![image.png](attachment:4e7a2dfe-dc64-4123-930b-4b26e85c21cd:image.png)

그룹명과 동일한 role mapping을 진행합니다.

![image.png](attachment:acce5558-97b6-4409-a97a-c9d280aaa58b:image.png)

**Client 설정**

클라이언트를 설정하기 위해 메인 메뉴에서 선택 후, Create client를 클릭합니다.

![image.png](attachment:548e0878-5023-42ea-a665-f12c23e849fb:image.png)

Client ID를 정의 합니다.

![image.png](attachment:ed083478-47f8-46d3-97b8-113ae927a003:image.png)

클라이언트 인증, 인가 및 다이렉트 접근 권한을 부여 합니다.

![image.png](attachment:12084c3a-8bbf-4d78-a507-71291b6bdc92:image.png)

tmc-sm의 domain FQDN 정보를 기반으로 아래와 같이 Home URL 및 Valid redirect URLs을 추가합니다.

**Home URL:** https://pinniped-supervisor.<tmc-dns-zone>/provider/pinniped/callback

**Valid redirect URIs:**

- https://pinniped-supervisor.<tmc-dns-zone>/provider/pinniped/callback
- https://pinniped-supervisor.<tmc-dns-zone>
- https://<tmc-dns-zone>

![image.png](attachment:ad0166e8-87e1-41c4-b682-bac3f4cb5088:image.png)

Client scopes 탭으로 이동해서, 맞게 scope가 생성됐는지 확인합니다.

![image.png](attachment:9677173f-d3e7-485a-b001-19cc623ec914:image.png)

Credentials 탭으로 이동해서 Client Secret 값을 복사해서 노트패드에 붙여넣기 합니다.

![image.png](attachment:1cf43340-73cb-40ff-83ad-5583820af451:image.png)

-
