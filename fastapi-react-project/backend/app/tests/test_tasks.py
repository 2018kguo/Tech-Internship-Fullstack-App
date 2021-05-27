from app.core import tasks


def test_example_task():
    task_output = tasks.example_task("Hello World")
    assert task_output == "test task returns Hello World"

def test_scrape_jobs_task():
    task_output = tasks.scrape_jobs_task()
    assert task_output == "Jobs have been scraped successfully"
