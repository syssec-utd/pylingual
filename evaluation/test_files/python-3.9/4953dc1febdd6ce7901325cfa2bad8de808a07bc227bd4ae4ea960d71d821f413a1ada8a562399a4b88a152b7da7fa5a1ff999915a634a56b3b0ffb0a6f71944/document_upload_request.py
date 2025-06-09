from attr import s
from typing import Optional
from jstruct import JStruct

@s(auto_attribs=True)
class ServiceAccessTokenType:
    AccessLicenseNumber: Optional[str] = None

@s(auto_attribs=True)
class UsernameTokenType:
    Username: Optional[str] = None
    Password: Optional[str] = None

@s(auto_attribs=True)
class UPSSecurityType:
    UsernameToken: Optional[UsernameTokenType] = JStruct[UsernameTokenType]
    ServiceAccessToken: Optional[ServiceAccessTokenType] = JStruct[ServiceAccessTokenType]

@s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: Optional[str] = None

@s(auto_attribs=True)
class RequestType:
    TransactionReference: Optional[TransactionReferenceType] = JStruct[TransactionReferenceType]

@s(auto_attribs=True)
class UserCreatedFormType:
    UserCreatedFormFileName: Optional[str] = None
    UserCreatedFormFileFormat: Optional[str] = None
    UserCreatedFormDocumentType: Optional[str] = None
    UserCreatedFormFile: Optional[str] = None

@s(auto_attribs=True)
class UploadRequestType:
    ShipperNumber: Optional[str] = None
    Request: Optional[RequestType] = JStruct[RequestType]
    UserCreatedForm: Optional[UserCreatedFormType] = JStruct[UserCreatedFormType]

@s(auto_attribs=True)
class DocumentUploadRequestType:
    UPSSecurity: Optional[UPSSecurityType] = JStruct[UPSSecurityType]
    UploadRequest: Optional[UploadRequestType] = JStruct[UploadRequestType]