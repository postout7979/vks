- Tanzu Mission Control Self Managed는 크게 Active Directory(LDAP 포함)과 OIDC 방식 두 가지에 대한 인증 통합을 제공하고 있습니다.
- 이 가이드에는 단독형 Keycloak 오픈소스를 K8s에 배포하고, 다른 ID 공급자 연결이 아닌 독립 ID 공급자로 사용하는 방법을 제공합니다. (Production 환경에서는 keycloak 사이트의 내용을 참고하여, 가용성 유지 및 S3 스토리지 백업을 고려해야 합니다.)

### Keycloak 환경 설정

User 메뉴에서 admin user를 생성합니다.

![image](https://github.com/user-attachments/assets/05e63daa-bb26-4f3a-9639-ec8b7922e824)


Credentials 탭으로 이동하여, Password reset을 진행합니다.

![image](https://github.com/user-attachments/assets/7a77ccb2-7b05-44ba-a1de-aeced38448aa)


Role mapping 탭으로 이동해서 Assign role을 클릭합니다.

![image](https://github.com/user-attachments/assets/a2d749e8-cbe6-4356-9cce-d6578030d8ad)


“Filter by realm roles”로 변경 후, default-roles-master를 할당합니다.

![image](https://github.com/user-attachments/assets/69490aea-5306-4b62-8e02-a1c9fe78ee83)


**Client Scope 설정**

client scope로 이동하여, 신규 Client Scope을 생성합니다.

* client scopes - Create client scope
![image](https://github.com/user-attachments/assets/04fd0876-7f28-4037-8b6b-2b4cbfc3e639)



Name: groups

Type: Default

Display on consent screen: On

Include in token scope: On

![image](https://github.com/user-attachments/assets/f2518755-aefc-4a08-9a65-e347cd8beedf)


Mappers 탭을 클릭 - Add predefined mapper를 클릭

![image](https://github.com/user-attachments/assets/09fe4762-050c-4890-b8a0-0803c59f7f3c)


groups을 검색하여 추가합니다.

![image](https://github.com/user-attachments/assets/2aff6e19-ed5f-4b36-bea2-5f930cb25177)


생성한 mapper groups을 클릭하고, 아래와 같이 설정 구성합니다.

![image](https://github.com/user-attachments/assets/6e8a7a08-b16a-4a09-a9e5-0592bba1f4b0)


**Realm roles 설정**

메인 메뉴의 Realm roles을 선택하고, Create role을 클릭합니다.

![image](https://github.com/user-attachments/assets/fc6f0f83-3b2c-43af-a4b1-8a6c25dc8122)


role name으로 tmc:admin과 tmc:member를 생성합니다.

![image](https://github.com/user-attachments/assets/2d9bef59-871b-49fe-813a-9ec9cc73408b)


![image](https://github.com/user-attachments/assets/b5573839-75d6-4e63-bf3c-7833bcd6f6d4)


**Users - 사용자 추가**

메인 메뉴에서 Users를 선택하고, Add user를 클릭합니다.

![image](https://github.com/user-attachments/assets/4882cd60-a185-403a-9132-3606870402c0)


관리자 및 사용자를 추가 합니다.

- tmcadmin, tmcuser01, tmcuser02, etc…

![image](https://github.com/user-attachments/assets/bc57cc8f-d46d-41a0-af01-856af49d1d92)


사용자를 생성하고, Set password을 클릭해서 암호를 설정합니다.

![image](https://github.com/user-attachments/assets/b5b9954c-2ce5-4837-9c3d-559ec2076a8e)


![image](https://github.com/user-attachments/assets/3592d219-373f-49de-bb2c-81c36e324737)


**Groups 설정**

메인 메뉴의 Groups을 선택하고, Create group을 클릭합니다.

![image](https://github.com/user-attachments/assets/7dfd7303-7c69-4c96-b6c0-4e6e7829f133)


Group명을 tmc:admin, tmc:member로 추가 설정합니다.

- 여러 그룹을 사용할 경우, 각 그룹을 모두 생성합니다.

![image](https://github.com/user-attachments/assets/366de681-806c-4b67-b7a9-addbf7098558)


생성된 그룹에 알맞은 사용자를 Add member를 클릭하여, 추가합니다.

![image](https://github.com/user-attachments/assets/71970d75-b4ac-4efe-b898-d200bfe64e26)


사용자를 선택하고 Add 버튼을 클릭합니다.

![image](https://github.com/user-attachments/assets/4bbd16ba-9353-47ec-83e3-b43b8b8de14d)


그룹의 Role mapping 탭을 선택합니다.

![image](https://github.com/user-attachments/assets/96dd52ef-9b55-440c-8205-408c3fadcdef)


그룹명과 동일한 role mapping을 진행합니다.

![image](https://github.com/user-attachments/assets/db9e3591-a73c-4630-8027-43161d13406d)


**Client 설정**

클라이언트를 설정하기 위해 메인 메뉴에서 선택 후, Create client를 클릭합니다.

![image](https://github.com/user-attachments/assets/c87a7ff6-6453-46c2-b4c9-efd7a398f7a5)


Client ID를 정의 합니다.

![image](https://github.com/user-attachments/assets/7dc46bec-4976-4310-98e1-1922a68c1b8a)


클라이언트 인증, 인가 및 다이렉트 접근 권한을 부여 합니다.

![image](https://github.com/user-attachments/assets/04de091a-8f1c-4d02-9c3c-3c7d4b3c00e8)


tmc-sm의 domain FQDN 정보를 기반으로 아래와 같이 Home URL 및 Valid redirect URLs을 추가합니다.

**Home URL:** https://pinniped-supervisor.<tmc-dns-zone>/provider/pinniped/callback

**Valid redirect URIs:**

- https://pinniped-supervisor.<tmc-dns-zone>/provider/pinniped/callback
- https://pinniped-supervisor.<tmc-dns-zone>
- https://<tmc-dns-zone>

![image](https://github.com/user-attachments/assets/284b362f-1b63-44ab-a14b-81a18d95ebac)


Client scopes 탭으로 이동해서, 맞게 scope가 생성됐는지 확인합니다.

![image](https://github.com/user-attachments/assets/6db0a71f-7708-4dd6-a9fe-2fb747e73c8f)


Credentials 탭으로 이동해서 Client Secret 값을 복사해서 노트패드에 붙여넣기 합니다.

![image](https://github.com/user-attachments/assets/2e52e8cb-ea32-4238-9c81-71b533eddf9e)


-
