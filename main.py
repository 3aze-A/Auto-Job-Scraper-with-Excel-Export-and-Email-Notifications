import os
import urllib.parse
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
import excel_export
import emailer

load_dotenv()


# Define the schema with Optional types and default values
class JobListing(BaseModel):
    title: Optional[str] = Field(None, description="The job title")
    company: Optional[str] = Field(None, description="Company name")
    job: Optional[str] = Field(None, description="The job description/what the employee has to do")
    salary: Optional[str] = Field(None, description="Salary range if listed")
    location: Optional[str] = Field(None, description="City or remote status")


class JobListContainer(BaseModel):
    jobs: List[JobListing] = Field(..., description="A list of all job listings found on the page")


app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))


# Keyword Filtering
def build_url(job_title, location=""):
    base = "https://ca.indeed.com/jobs"
    params = {
        'q': job_title,
        'l': location,
        'from': 'searchOnHP'
    }
    # This automatically handles spaces and special characters
    return f"{base}?{urllib.parse.urlencode(params)}"


all_jobs = []
search_url = build_url(input('Enter job title: ').lower(), input('Enter location: ').lower())

try:
    data = app.scrape(
        url=search_url,
        formats=[{
            'type': 'json',
            'schema': JobListContainer.model_json_schema(),
            'prompt': "Extract every single job listing visible on the page into the jobs array."
        }],
        only_main_content=False,
        # wait_for=200
    )
except:
    raise Exception
else:
    # EXAMPLE JSON OUTPUT
    """
    json={
    'jobs': [
    {'title': 'Software Engineer Intern', 'company': 'Bridigix', 'job': 'Contributing to actual 
    backend systems used in production with guidance.', 'salary': '$5,000 a month', 'location': 'Remote'},
    
    {'title': 'Student Intern, AI & Analytics', 'company': 'Celestica', 'job': 'Fun intern activities 
    including celebration events and networking. Possibility of a student casual contract position after 
    completion of internship.', 'salary': '$22.50–$25.50 an hour', 'location': 'Toronto, ON'}, 
    
    {'title': 'Data Science Intern', 'company': 'Johnson & Johnson', 'job': 'Support analytics initiatives 
    across machine learning, generative AI.', 'salary': '$22–$32 an hour', 'location': 'Toronto, ON'},
    
    {'title': 'Software Engineering Intern - Kernels', 'company': 'd-Matrix', 'job': 'Developing reference implementations for accuracy verification.', 'salary': '$40–$70 an hour', 'location': 'Toronto, ON'}, {'title': 'Software Tester – Co-op/Intern', 'company': 'NOKIA', 'job': 'Development of scripts or applications (Python, Java, JavaScript).', 'salary': 'Full-time', 'location': 'Canada'}, {'title': 'Engineering Intern', 'company': 'Brim', 'job': 'Work across the full stack - from backend services.', 'salary': '$50,000–$65,000 a year', 'location': 'Remote'}, {'title': 'Engineering Intern', 'company': 'Brim', 'job': 'Work across the full stack - from backend services.', 'salary': '$50,000–$65,000 a year', 'location': 'Remote'}, {'title': 'Intern - Software/ML Engineering', 'company': 'Human Computer Lab', 'job': 'Help build the software and machine learning systems that power robot perception.', 'salary': 'Internship / Co-op', 'location': 'Toronto, ON'}, {'title': 'Robotics - Software Development Engineer Intern - 2026 - Toronto', 'company': 'Amazon Development Centre Canada ULC - K03', 'job': 'Full-time positions, and intern/co-ops should expect to work in office, Monday-Friday.', 'salary': 'Full-time', 'location': 'Toronto, ON'}, {'title': 'Fall Intern 2026 - Data Science (Toronto Office)', 'company': 'Mackenzie Financial Corporation', 'job': 'Innovate the industry and support Canadians in achieving their financial goals. Knowledge of SQL, Python, and Git.', 'salary': '$49,000–$51,000 a year', 'location': 'Greater Toronto Area, ON'}, {'title': 'Intern - Backend / Test Automation Developer', 'company': 'Lumeto', 'job': 'Hands-on experience with advanced robotic platforms. Python and/or C++ proficiency.', 'salary': '$18–$23 an hour', 'location': 'Toronto, ON'}, {'title': 'AI Development Intern', 'company': 'Organika Health Products Inc', 'job': 'Develop an AI agent capable of creating Class 1, 2, and 3 Natural.', 'salary': '$20–$21 an hour', 'location': 'Vancouver, BC'}, {'title': 'Robotics Intern', 'company': 'O’Adventure Limited', 'job': 'Hands-on experience with advanced robotic platforms, including Unitree quadruped and humanoid robots.', 'salary': '$28–$38 an hour', 'location': 'Thornhill, ON'}, {'title': 'Student Researcher, PhD, Winter/Summer 2026', 'company': 'Google', 'job': 'Intended for students pursuing a PhD degree program in Computer Science or a related field.', 'salary': '$120,000 a year', 'location': 'Toronto, ON'}, {'title': 'QA Engineer - Summer Internship', 'company': 'Prepr', 'job': 'Participate in shaping the future of work.', 'salary': '$18 an hour', 'location': 'Toronto, ON'}, {'title': 'Student Researcher, BS/MS, Winter/Summer 2026', 'company': 'Google', 'job': "Intended for students pursuing a Bachelor's or Master’s degree program in Computer Science or a related field.", 'salary': 'Full-time', 'location': 'Toronto, ON'}]} summary=None metadata=DocumentMetadata(title='Discover 100 Python Intern Jobs and Work Opportunities | Indeed', description="Search 193 Python Intern jobs now available on Indeed.com, the world's largest job site.", url='https://ca.indeed.com/jobs?q=python+intern&vjk=83db5f513749fc98', language='en', keywords=None, robots='noindex, nofollow', og_title=None, og_description=None, og_url=None, og_image=None, og_audio=None, og_determiner=None, og_locale=None, og_locale_alternate=None, og_site_name=None, og_video=None, favicon='https://ca.indeed.com/images/favicon.ico', dc_terms_created=None, dc_date_created=None, dc_date=None, dc_terms_type=None, dc_type=None, dc_terms_audience=None, dc_terms_subject=None, dc_subject=None, dc_description=None, dc_terms_keywords=None, modified_time=None, published_time=None, article_tag=None, article_section=None, source_url='https://ca.indeed.com/jobs?q=python+intern', status_code=200, scrape_id='019df045-e8d5-77c3-9f1a-40aa4b0a4606', num_pages=None, content_type='text/html; charset=utf-8', proxy_used='basic', timezone=None, cache_state='hit', cached_at='2026-05-03T23:51:04.402Z', credits_used=5, concurrency_limited=False, concurrency_queue_duration_ms=None, error=None, viewport=['width=device-width,initial-scale=1.0', 'width=device-width, initial-scale=1, maximum-scale=1'], referrer='origin-when-cross-origin', format-detection='telephone=no') links=None images=None screenshot=None audio=None actions=None answer=None warning=None change_tracking=None branding=None
    """

    if 'jobs' in data.json:
        for job in data.json['jobs']:
            all_jobs.append(list(job.values()))

    if len(all_jobs) == 0:
        print('NO JOBS FOUND!')

    # Save Data to an Excel File
    try:
        excel_export.main(all_jobs)
    except:
        raise Exception
    else:
        # Email results
        try:
            emailer.main(all_jobs)
        except:
            raise Exception
