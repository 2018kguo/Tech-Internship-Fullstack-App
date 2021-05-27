from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t
from app.db.session import get_db
from app.db.crud import (
    get_jobs,
    create_job,
    delete_job,
    delete_all_jobs
)
from app.db.schemas import Job, JobCreate


jobs_router = r = APIRouter()


@r.get(
    "/jobs",
    response_model=t.List[Job],
    response_model_exclude_none=True,
)
async def jobs_list(
    response: Response,
    db=Depends(get_db)
):
    """
    Get all users
    """
    jobs = get_jobs(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(jobs)}"
    return jobs


@r.post("/jobs", response_model=Job, response_model_exclude_none=True)
async def job_create(
    request: Request,
    job: JobCreate,
    db=Depends(get_db)
):
    """
    Create a new user
    """
    return create_job(db, job)


@r.delete(
    "/jobs/{job_id}", response_model=Job, response_model_exclude_none=True
)
async def job_delete(
    request: Request,
    job_id: int,
    db=Depends(get_db)
):
    """
    Delete existing user
    """
    return delete_job(db, job_id)


@r.delete(
    "/jobs/actions/deleteAll"
)
async def job_delete(
    request: Request,
    db=Depends(get_db)
):
    """
    Delete existing user
    """
    return delete_all_jobs(db)
