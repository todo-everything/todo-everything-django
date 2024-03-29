import pytest
from accounts import models as accounts_models
from django.core.management import call_command
from organizations import api as organizations_api
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIRequestFactory, force_authenticate


# Tests here require the initial users fixture so we run that here.
# Running this at the top-level (tests/conftest.py) seems to cause issues,
# but it works when it's app-level. *shrug*
@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        print("django db setup???")
        call_command("loaddata", "initial_users")
        call_command("loaddata", "initial_orgs")


def test_organizations_unauthorized():
    view = organizations_api.OrganizationViewSet.as_view({"get": "list"})
    factory = APIRequestFactory()
    request = factory.get("/api/organizations")
    response = view(request)
    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_organizations_is_staff():
    view = organizations_api.OrganizationViewSet.as_view({"get": "list"})
    factory = APIRequestFactory()
    user = accounts_models.Account.objects.get(pk=1)
    assert user.is_staff
    request = factory.get("/api/organizations")
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_organizations_is_org_admin():
    view = organizations_api.OrganizationViewSet.as_view({"get": "list"})
    factory = APIRequestFactory()
    user = accounts_models.Account.objects.get(pk=2)
    assert not user.is_staff
    assert not user.is_superuser
    request = factory.get("/api/organizations")
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 1
