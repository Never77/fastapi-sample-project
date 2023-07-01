"""
I know, nothing of this purpose is present in the mongodb of our app, but it's for example purpose.
"""
from pydantic import BaseModel, Field
from netcore.database import PyObjectId
from bson import ObjectId

class Post(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    content: str = Field(...)  # That means this field is mandatory
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "content": "Lorem ipsum"
            }
        }

class UpdatePost(BaseModel):
    # If there is multiple field you can set all of them as Optional and put only fields you want to update.
    # Here you put only field that you allow to change, and all of them. If the field never changes like id, don't put it here.
    content: str = Field(...)  
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "content": "Lorem ipsum"
            }
        }