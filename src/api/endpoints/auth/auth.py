from fastapi import APIRouter, HTTPException
from src.models.schemas import signupRequest, signinRequest
from src.utils.logging_config import CustomLogger
from src.service.auth.auth import perform_signup, perform_signin

logger = CustomLogger().get_logger

router = APIRouter()


@router.post("/api/v1/auth/signup") 
async def signup(
    request: signupRequest 
):
    logger.info(f"Received signup request: {request}")
    
    try:
        result = perform_signup(request.email, request.password, request.password2)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/api/v1/auth/signin") 
async def signin(
    request: signinRequest 
):
    logger.info(f"Received signin request: {request}")
    
    try:
        result = perform_signin(request.email, request.password)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))