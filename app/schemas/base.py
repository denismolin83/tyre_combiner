from pydantic import BaseModel, ConfigDict

# Глобальные настройки Pydantic
class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )