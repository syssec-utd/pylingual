from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from localcosmos_server.tests.common import test_settings, DataCreator, TEST_IMAGE_PATH, TEST_CLIENT_ID, TEST_PLATFORM, GEOJSON_POLYGON, TEST_USER_GEOMETRY_NAME
from localcosmos_server.tests.mixins import WithUser, WithApp, WithObservationForm, WithMedia, WithUserGeometry
from localcosmos_server.datasets.models import ObservationForm, Dataset, DatasetImages
from django.utils import timezone
import json

class CreatedUsersMixin:

    def setUp(self):
        super().setUp()
        self.superuser = self.create_superuser()
        self.user = self.create_user()

class TestCreateObservationForm(WithObservationForm, WithUser, WithApp, CreatedUsersMixin, APITestCase):

    @test_settings
    def test_post(self):
        uuid = self.observation_form_json['uuid']
        version = self.observation_form_json['version']
        qry = ObservationForm.objects.filter(uuid=uuid, version=version)
        self.assertFalse(qry.exists())
        url_kwargs = {'app_uuid': self.app.uuid}
        url = reverse('api_create_observation_form', kwargs=url_kwargs)
        post_data = {'definition': self.observation_form_json}
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(qry.exists())

    @test_settings
    def test_post_anonymous_observations(self):
        uuid = self.observation_form_json['uuid']
        version = self.observation_form_json['version']
        qry = ObservationForm.objects.filter(uuid=uuid, version=version)
        self.assertFalse(qry.exists())
        url_kwargs = {'app_uuid': self.ao_app.uuid}
        url = reverse('api_create_observation_form', kwargs=url_kwargs)
        post_data = {'definition': self.observation_form_json}
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(qry.exists())

class TestRetrieveObservationForm(WithObservationForm, WithUser, WithApp, CreatedUsersMixin, APITestCase):

    @test_settings
    def test_get(self):
        observation_form = self.create_observation_form()
        url_kwargs = {'app_uuid': self.app.uuid, 'observation_form_uuid': self.observation_form_json['uuid'], 'version': self.observation_form_json['version']}
        url = reverse('api_retrieve_observation_form', kwargs=url_kwargs)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['definition'], self.observation_form_json)

    @test_settings
    def test_get_anonymous_observations(self):
        observation_form = self.create_observation_form()
        url_kwargs = {'app_uuid': self.ao_app.uuid, 'observation_form_uuid': self.observation_form_json['uuid'], 'version': self.observation_form_json['version']}
        url = reverse('api_retrieve_observation_form', kwargs=url_kwargs)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['definition'], self.observation_form_json)

    @test_settings
    def test_get_fail(self):
        url_kwargs = {'app_uuid': self.ao_app.uuid, 'observation_form_uuid': self.observation_form_json['uuid'], 'version': self.observation_form_json['version']}
        url = reverse('api_retrieve_observation_form', kwargs=url_kwargs)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class WithDatasetPostData:

    def get_post_data(self, alternative_data=False):
        data_creator = DataCreator()
        dataset_data = data_creator.get_dataset_data(self.observation_form_json, alternative_data=alternative_data)
        now = timezone.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S %z')
        post_data = {'observation_form': {'uuid': self.observation_form_json['uuid'], 'version': self.observation_form_json['version']}, 'data': dataset_data, 'clientId': TEST_CLIENT_ID, 'platform': TEST_PLATFORM, 'createdAt': now_str}
        return post_data

class TestListCreateDataset(WithDatasetPostData, WithObservationForm, WithMedia, WithUser, WithApp, CreatedUsersMixin, APITestCase):

    @test_settings
    def test_post(self):
        url_kwargs = {'app_uuid': self.app.uuid}
        url = reverse('api_list_create_dataset', kwargs=url_kwargs)
        post_data = self.get_post_data()
        qry = Dataset.objects.all()
        self.assertFalse(qry.exists())
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.create_observation_form()
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(qry.exists())
        dataset = qry.first()
        self.assertEqual(dataset.user, self.user)

    @test_settings
    def test_post_ao(self):
        url_kwargs = {'app_uuid': self.ao_app.uuid}
        url = reverse('api_list_create_dataset', kwargs=url_kwargs)
        post_data = self.get_post_data()
        qry = Dataset.objects.all()
        self.assertFalse(qry.exists())
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.create_observation_form()
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(qry.exists())
        dataset = qry.first()
        self.assertIsNone(dataset.user)

    @test_settings
    def test_post_ao_no_created_at(self):
        url_kwargs = {'app_uuid': self.ao_app.uuid}
        url = reverse('api_list_create_dataset', kwargs=url_kwargs)
        post_data = self.get_post_data()
        del post_data['createdAt']
        qry = Dataset.objects.all()
        self.assertFalse(qry.exists())
        self.create_observation_form()
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(qry.exists())
        dataset = qry.first()
        self.assertIsNone(dataset.user)

    @test_settings
    def test_get_list_registered(self):
        observation_form = self.create_observation_form()
        dataset = self.create_dataset(observation_form=observation_form)
        dataset.user = self.user
        dataset.save()
        dataset_image = self.create_dataset_image(dataset)
        url_kwargs = {'app_uuid': self.app.uuid}
        url = reverse('api_list_create_dataset', kwargs=url_kwargs)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        _dataset = response.data['results'][0]
        self.assertEqual(_dataset['uuid'], str(dataset.uuid))

    @test_settings
    def test_get_list_anonymous(self):
        observation_form = self.create_observation_form()
        dataset = self.create_dataset(observation_form=observation_form)
        dataset_image = self.create_dataset_image(dataset)
        url_kwargs = {'app_uuid': self.app.uuid}
        url = reverse('api_list_create_dataset', kwargs=url_kwargs)
        url_with_client_id = '{0}?client_id={1}'.format(url, dataset.client_id)
        response = self.client.get(url_with_client_id, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        _dataset = response.data['results'][0]
        self.assertEqual(_dataset['uuid'], str(dataset.uuid))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
        dataset.user = self.user
        dataset.client_id = 'another client'
        dataset.save()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

class TestRetrieveDataset(WithDatasetPostData, WithObservationForm, WithUser, WithApp, CreatedUsersMixin, APITestCase):

    @test_settings
    def test_get(self):
        observation_form = self.create_observation_form()
        dataset = self.create_dataset(observation_form)
        url_kwargs = {'app_uuid': self.ao_app.uuid, 'uuid': str(dataset.uuid)}
        url = reverse('api_manage_dataset', kwargs=url_kwargs)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['uuid'], str(dataset.uuid))

class TestUpdateDataset(WithDatasetPostData, WithObservationForm, WithUser, WithApp, CreatedUsersMixin, APITestCase):

    @test_settings
    def test_update(self):
        observation_form = self.create_observation_form()
        dataset = self.create_dataset(observation_form)
        dataset.user = self.user
        dataset.save()
        secondary_user = self.create_secondary_user()
        self.assertEqual(dataset.user, self.user)
        url_kwargs = {'app_uuid': self.app.uuid, 'uuid': str(dataset.uuid)}
        url = reverse('api_manage_dataset', kwargs=url_kwargs)
        post_data = self.get_post_data(alternative_data=True)
        response = self.client.put(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=secondary_user)
        response = self.client.put(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        post_data['clientId'] = 'id differs from dataset'
        response = self.client.put(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dataset.refresh_from_db()
        self.assertEqual(dataset.data, post_data['data'])

    @test_settings
    def test_update_wrong_app(self):
        observation_form = self.create_observation_form()
        dataset = self.create_dataset(observation_form)
        dataset.user = self.user
        dataset.save()
        url_kwargs = {'app_uuid': self.ao_app.uuid, 'uuid': str(dataset.uuid)}
        url = reverse('api_manage_dataset', kwargs=url_kwargs)
        post_data = self.get_post_data(alternative_data=True)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @test_settings
    def test_update_ao(self):
        observation_form = self.create_observation_form()
        dataset = self.create_dataset(observation_form)
        dataset.app_uuid = self.ao_app.uuid
        dataset.save()
        url_kwargs = {'app_uuid': self.app.uuid, 'uuid': str(dataset.uuid)}
        url = reverse('api_manage_dataset', kwargs=url_kwargs)
        post_data = self.get_post_data(alternative_data=True)
        response = self.client.put(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        url_kwargs = {'app_uuid': self.ao_app.uuid, 'uuid': str(dataset.uuid)}
        url = reverse('api_manage_dataset', kwargs=url_kwargs)
        post_data = self.get_post_data(alternative_data=True)
        response = self.client.put(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dataset.refresh_from_db()
        self.assertEqual(dataset.data, post_data['data'])

class TestDeleteDataset(WithDatasetPostData, WithObservationForm, WithUser, WithApp, CreatedUsersMixin, APITestCase):

    @test_settings
    def test_destroy(self):
        observation_form = self.create_observation_form()
        secondary_user = self.create_secondary_user()
        dataset = self.create_dataset(observation_form)
        dataset.user = self.user
        dataset.save()
        url_kwargs = {'app_uuid': self.app.uuid, 'uuid': str(dataset.uuid)}
        url = reverse('api_manage_dataset', kwargs=url_kwargs)
        self.client.force_authenticate(user=secondary_user)
        response = self.client.delete(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @test_settings
    def test_destroy_ao(self):
        observation_form = self.create_observation_form()
        dataset = self.create_dataset(observation_form)
        dataset.app_uuid = self.ao_app.uuid
        dataset.save()
        url_kwargs = {'app_uuid': self.ao_app.uuid, 'uuid': str(dataset.uuid)}
        url = reverse('api_manage_dataset', kwargs=url_kwargs)
        response = self.client.delete(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        post_data = {'clientId': 'different client id'}
        response = self.client.delete(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        post_data = {'clientId': dataset.client_id}
        response = self.client.delete(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TestCreateDatasetImage(WithMedia, WithDatasetPostData, WithObservationForm, WithUser, WithApp, CreatedUsersMixin, APITestCase):

    def get_post_data(self, dataset):
        field_uuid = self.get_image_field_uuid(dataset.observation_form)
        image = SimpleUploadedFile(name='test_image.jpg', content=open(TEST_IMAGE_PATH, 'rb').read(), content_type='image/jpeg')
        post_data = {'dataset': dataset.pk, 'fieldUuid': field_uuid, 'clientId': dataset.client_id, 'image': image}
        return post_data

    @test_settings
    def test_post(self):
        observation_form = self.create_observation_form()
        dataset = self.create_dataset(observation_form=observation_form)
        dataset.user = self.user
        dataset.save()
        url_kwargs = {'app_uuid': self.app.uuid, 'uuid': str(dataset.uuid)}
        url = reverse('api_create_dataset_image', kwargs=url_kwargs)
        post_data = self.get_post_data(dataset)
        qry = DatasetImages.objects.all()
        self.assertFalse(qry.exists())
        response = self.client.post(url, post_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.user)
        post_data = self.get_post_data(dataset)
        response = self.client.post(url, post_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(qry.exists())
        dataset_image = qry.first()
        self.assertEqual(dataset_image.dataset, dataset)
        self.assertEqual(str(dataset_image.field_uuid), post_data['fieldUuid'])

    @test_settings
    def test_post_ao(self):
        observation_form = self.create_observation_form()
        dataset = self.create_dataset(observation_form=observation_form)
        url_kwargs = {'app_uuid': self.ao_app.uuid, 'uuid': str(dataset.uuid)}
        url = reverse('api_create_dataset_image', kwargs=url_kwargs)
        post_data = self.get_post_data(dataset)
        qry = DatasetImages.objects.all()
        self.assertFalse(qry.exists())
        response = self.client.post(url, post_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(qry.exists())
        dataset_image = qry.first()
        self.assertEqual(dataset_image.dataset, dataset)
        self.assertEqual(str(dataset_image.field_uuid), post_data['fieldUuid'])

class TestDestroyDatasetImage(WithMedia, WithDatasetPostData, WithObservationForm, WithUser, WithApp, CreatedUsersMixin, APITestCase):

    @test_settings
    def test_post(self):
        observation_form = self.create_observation_form()
        dataset = self.create_dataset(observation_form=observation_form)
        dataset.user = self.user
        dataset.save()
        dataset_image = self.create_dataset_image(dataset)
        qry = DatasetImages.objects.filter(dataset=dataset)
        self.assertTrue(qry.exists())
        url_kwargs = {'app_uuid': self.app.uuid, 'uuid': str(dataset.uuid), 'pk': dataset_image.pk}
        url = reverse('api_destroy_dataset_image', kwargs=url_kwargs)
        response = self.client.delete(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(qry.exists())

    @test_settings
    def test_post_ao(self):
        observation_form = self.create_observation_form()
        dataset = self.create_dataset(observation_form=observation_form)
        dataset.app_uuid = self.ao_app.uuid
        dataset.save()
        dataset_image = self.create_dataset_image(dataset)
        qry = DatasetImages.objects.filter(dataset=dataset)
        self.assertTrue(qry.exists())
        url_kwargs = {'app_uuid': self.ao_app.uuid, 'uuid': str(dataset.uuid), 'pk': dataset_image.pk}
        url = reverse('api_destroy_dataset_image', kwargs=url_kwargs)
        response = self.client.delete(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        post_data = {'clientId': 'wrong client id'}
        response = self.client.delete(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        post_data = {'clientId': dataset.client_id}
        response = self.client.delete(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TestCreateListUserGeometry(WithUserGeometry, WithUser, WithApp, CreatedUsersMixin, APITestCase):

    @test_settings
    def test_post(self):
        post_data = {'geometry': GEOJSON_POLYGON, 'name': TEST_USER_GEOMETRY_NAME}
        url_kwargs = {'app_uuid': self.app.uuid}
        url = reverse('api_create_list_user_geometry', kwargs=url_kwargs)
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @test_settings
    def test_post_maxed_out(self):
        self.client.force_authenticate(user=self.user)
        for name in ['poly1', 'poly2', 'poly3']:
            self.create_user_geometry(self.user, name=name)
        post_data = {'geometry': GEOJSON_POLYGON, 'name': TEST_USER_GEOMETRY_NAME}
        url_kwargs = {'app_uuid': self.app.uuid}
        url = reverse('api_create_list_user_geometry', kwargs=url_kwargs)
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @test_settings
    def test_get(self):
        user_geometry = self.create_user_geometry(self.user)
        url_kwargs = {'app_uuid': self.app.uuid}
        url = reverse('api_create_list_user_geometry', kwargs=url_kwargs)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        data = response.data['results'][0]
        self.assertEqual(data['id'], user_geometry.id)
        self.assertEqual(data['name'], user_geometry.name)
        self.assertEqual(dict(data['geometry']), GEOJSON_POLYGON)

class TestManageUserGeometry(WithUserGeometry, WithUser, WithApp, CreatedUsersMixin, APITestCase):

    @test_settings
    def test_get(self):
        user_geometry = self.create_user_geometry(self.user)
        url_kwargs = {'app_uuid': self.app.uuid, 'pk': user_geometry.pk}
        url = reverse('api_manage_user_geometry', kwargs=url_kwargs)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['geometry'], GEOJSON_POLYGON)
        self.assertEqual(response.data['name'], user_geometry.name)

    @test_settings
    def test_delete(self):
        user_geometry = self.create_user_geometry(self.user)
        url_kwargs = {'app_uuid': self.app.uuid, 'pk': user_geometry.pk}
        url = reverse('api_manage_user_geometry', kwargs=url_kwargs)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)