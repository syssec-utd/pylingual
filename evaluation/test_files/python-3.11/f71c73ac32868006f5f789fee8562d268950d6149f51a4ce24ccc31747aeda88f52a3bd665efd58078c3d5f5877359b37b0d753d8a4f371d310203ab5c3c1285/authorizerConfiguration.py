from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Extra, Field

class AuthorizerConfiguration(BaseModel):

    class Config:
        extra = Extra.forbid
    className: str = Field(..., description='Class Name for authorizer.')
    containerRequestFilter: str = Field(..., description='Filter for the request authorization')
    adminPrincipals: List[str] = Field(..., description='List of unique admin principals', unique_items=True)
    botPrincipals: List[str] = Field(..., description='List of unique bot principals', unique_items=True)
    testPrincipals: Optional[List[str]] = Field(None, description='List of unique principals used as test users. **NOTE THIS IS ONLY FOR TEST SETUP AND NOT TO BE USED IN PRODUCTION SETUP**', unique_items=True)
    allowedEmailRegistrationDomains: Optional[List[str]] = Field(None, description='List of unique email domains that are allowed to signup on the platforms', unique_items=True)
    principalDomain: str = Field(..., description='Principal Domain')
    enforcePrincipalDomain: bool = Field(..., description='Enable Enforce Principal Domain')
    enableSecureSocketConnection: bool = Field(..., description='Enable Secure Socket Connection')