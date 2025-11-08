from pydantic import BaseModel, ConfigDict


class TokenBase(BaseModel):
    access_token: str
    token_type: str = "Bearer"

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(TokenBase):
    refresh_token: str | None = None
    expires_in: int