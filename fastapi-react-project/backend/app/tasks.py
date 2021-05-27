from app.core.celery_app import celery_app
from app.modules.scraper.output import scrapeJobs


@celery_app.task(acks_late=True)
def example_task(word: str) -> str:
    return f"test task returns {word}"


@celery_app.task(acks_late=True)
def scrape_jobs_task() -> str:
    scrapeJobs()
    return "Jobs have successfully been scraped"
