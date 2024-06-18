from pydantic import BaseModel, Field
#field_validator

class signupRequest(BaseModel):
    email: str = Field(default='')
    password: str = Field(default='')
    password2: str = Field(default='')

class signinRequest(BaseModel):
    email: str = Field(default='')
    password: str = Field(default='')

class retrieveJobRequest(BaseModel):
    job_name: str = Field(default='')
