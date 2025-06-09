import pydantic

class WebhookResponse(pydantic.BaseModel):
    status: str

    class Config:
        title: str = 'WebhookResponse'