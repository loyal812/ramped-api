from fastapi import APIRouter, HTTPException
from src.models.schemas import retrieveJobRequest
from src.utils.logging_config import CustomLogger
from src.service.job.retrieve_job import perform_retrieve_job

logger = CustomLogger().get_logger

router = APIRouter()


@router.post("/api/v1/job/retrieve_job") 
async def retrieve_job(
    request: retrieveJobRequest 
):
    logger.info(f"Received retrieve job request: {request}")
    
    try:
        result = perform_retrieve_job(request.job_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))