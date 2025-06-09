from acceldata_sdk.initialiser import torch_client_credentials
from acceldata_sdk.models.asset import RelationType
from acceldata_sdk.models.datasource import CreateDataSource, DatasourceType
from acceldata_sdk.torch_client import TorchClient
from acceldata_sdk.models.create_asset import AssetMetadata
torchClient = TorchClient(url='https://torch.acceldata.local:5443', access_key='N1LTYRK630PZ', secret_key='xPeUj4Iyj4WL2Tw284s9mqsgxvbPKW')
datasource = CreateDataSource(name='Feature_bag_datasource_sdk_3', sourceType=DatasourceType(21, 'FEATURE_BAG'), description='feature bag assembly creation using python sdk', isVirtual=True)
datasourceResponse = torchClient.create_datasource(datasource)
print('Newly created datasource: ', datasource)
newSnapshotVersion = datasourceResponse.initialise_snapshot(uid='NIffc38-9daa-4842-b008-f7fb3dd8439a')
print('New snapshot version created : ', newSnapshotVersion)
metadata = [AssetMetadata('STRING', 'abcd', 'pqr', 'sds'), AssetMetadata('STRING', 'abcdq', 'pqrq', 'sqds'), AssetMetadata('STRING', 'abcddq', 'pqrqd', 'sqdds')]
assetResponse = datasourceResponse.create_asset(uid='Feature_bag_datasource_sdk.feature_sdk_1', metadata=metadata, asset_type_id=22, description='Test asset creation', name='feature_sdk_1')
print('Newly created asset response : ', assetResponse)
delete_asset = datasourceResponse.delete_asset(id=9523)
print(delete_asset)