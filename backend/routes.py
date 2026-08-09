from fastapi import APIRouter, HTTPException
import logging
import traceback

from backend.models import PredictionRequest
from backend.services import PipelineService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/run")
def run_pipeline(request: PredictionRequest):

    try:

        logger.info("=" * 60)
        logger.info("AI-DS OS PIPELINE REQUEST")
        logger.info("Dataset: %s", request.dataset_path)
        logger.info("Target: %s", request.target)
        logger.info("=" * 60)

        # ==================================================
        # RUN EXISTING LANGGRAPH PIPELINE
        # ==================================================

        result = PipelineService.execute(
            request.dataset_path,
            request.target
        )

        logger.info("=" * 60)
        logger.info("AI-DS OS PIPELINE COMPLETED")
        logger.info("=" * 60)

        return result

    except Exception as e:

        logger.error("=" * 60)
        logger.error("AI-DS OS PIPELINE FAILED")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.error("=" * 60)

        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "type": type(e).__name__,
                "traceback": traceback.format_exc()
            }
        )