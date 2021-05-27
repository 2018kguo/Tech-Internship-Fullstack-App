from app.modules.scraper.classes import JobListing
import confuse
from confuse import Configuration
from app.modules.scraper.scrapers import LinkedInScraper, GithubScraper
from typing import List
from app.db.crud import create_jobs
from app.db.schemas import JobCreate
from datetime import datetime
from pathlib import Path
from app.db.session import get_db
from contextlib import contextmanager

def scrapeJobs():   
    p = Path(__file__)
    curDirectory = p.parent.absolute()

    #Load configuration from config.yaml
    config = confuse.Configuration('InternshipScraper', __name__)
    config.set_file(curDirectory / "job_scrape_config.yaml")
    
    #The LinkedIn scrape takes a long time if you put in a lot of locations/search terms
    linkedInScrapeEnabled = config["linkedIn"]["enabled"].get()
    githubScrapeEnabled = config["github"]["enabled"].get()

    jobsToCreate = []
    if(githubScrapeEnabled):
        jobs = scrapeGithub(config)
        if jobs is not None:
            listings = convertJobListingsToModels(jobs)
            jobsToCreate.extend(listings)
 
    if(linkedInScrapeEnabled):
        jobs = scrapeLinkedIn(config)
        if jobs is not None:
            listings = convertJobListingsToModels(jobs)
            jobsToCreate.extend(listings)
    
    #contextmanager voodoo that I don't yet quite understand to deal with yielded session
    #instead of using next() because some have reported issues with it
    with contextmanager(get_db)() as newSession:
        create_jobs(newSession, jobsToCreate)
    

def convertJobListingsToModels(jobs: List[JobListing]) -> List[JobCreate]:
    results = []
    curTime = datetime.utcnow()
    descColumnCharLimit = 5000
    linkCharLimit = 1000
    companyCharLimit = 100
    for job in jobs:
        if (job.link is not None and len(job.link) > linkCharLimit 
            or job.company is not None and len(job.company) > companyCharLimit):
            continue

        jobDesc = job.description
        if jobDesc is not None and len(jobDesc) > descColumnCharLimit:
            jobDesc = jobDesc[:descColumnCharLimit]
            
        jobCreate = JobCreate(
            company = job.company,
            link = job.link,
            description = jobDesc,
            date_posted = curTime
        )
        results.append(jobCreate)
    return results

def outputToFile(jobs: List[JobListing], fileName: str) -> None:
    newPositions = 0

    readFile = open(fileName, "r")
    existingLines = readFile.readlines()
    readFile.close()

    for job in jobs:
        jobStr = job.company + " | " + job.link + "\n"
        if jobStr not in existingLines:
            existingLines.append(jobStr)
            newPositions += 1

    existingLines.sort()
    writeNewLines(jobs, fileName, existingLines)
    print("Found {} new positions for {}".format(str(newPositions), fileName))

def writeNewLines(jobs: List[JobListing], fileName: str, existingLines: List[str]) -> None:
    writeFile = open(fileName, "w")
    for line in existingLines:
        writeFile.write(line)
    writeFile.close()

def scrapeLinkedIn(config: Configuration) -> List[JobListing]:
    queries = config["linkedIn"]["queries"].get()
    locations = config["linkedIn"]["locationsToQuery"].get()
    titles = config["linkedIn"]["desiredJobTitles"].get()
    blacklistTitles = config["linkedIn"]["blacklistJobTitles"].get()
    blacklist = config["linkedIn"]["description"]["blacklistSubstrings"].get()
    required = config["linkedIn"]["description"]["requiredSubstrings"].get()
    timespan = config["linkedIn"]["timespan"].get()
    scraper = LinkedInScraper(queries, locations, titles, blacklistTitles, blacklist, required, timespan)
    jobs = scraper.scrapeJobs()
    return jobs

def scrapeGithub(config: Configuration) -> List[JobListing]:
    repoURL = config["github"]["repoURL"].get()
    scraper = GithubScraper(repoURL)
    jobs = scraper.scrapeJobs()
    return jobs