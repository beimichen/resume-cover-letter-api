from pprint import pprint

import requests

# before running, start flask development server.
# Change to True see output

print_output = True
local = True

run_create_job_application = True
run_multiple_create_job_application = False
run_mass_create_job_application = False
run_coverletter_html = False
run_stylize_resume = False
run_job_match = True

# create-job-application

create_job_application_payload = {
    "candidate_name": "anne laura",
    "parsed_resume": None,
    "resume_file_link": None,
    "hiring_manager_name": None,
    # "raw_job_title": "waiter",
    "raw_job_title": "business manager",
    "job_ad_description": "There was a python coding job with django and others.",
    "company_name": "Microsoft",
    "hash_id": "as87df87as6df87as6df",
    "source_url": "https://indeed.com/a_job",
    "searched_skills": ["python", "django"],
    "include_resume_skills_in_match": False,
    "pre_compiled_coverletter": None,
    "chrome_app_version": "0.0.1"
}

if local:
    url = 'http://127.0.0.1:5000/create-job-application'
else:
    url = 'https://YOUR_API_HOST/create-job-application'

if run_create_job_application:
    r = requests.post(url, json=create_job_application_payload)

    if r.status_code == 200:
        print(r.status_code)
        print("success: create-job-application")
        if print_output:
            pprint(r.json(), width=1000)
    else:
        print("create-job-application failed. check API console output")
        print(r.status_code)

# --------------
# get_job_match

job_match_payload = {
    "chrome_app_version": "0.0.1",
    "parsed_resume": None,
    "resume_file_link": None,
    "hiring_manager_name": None,
    "raw_job_title": "business manager",
    "job_ad_description": "There was a python coding job with django and others.",
    "hash_id": "as87df87as6df87as6df",
    "source_url": "https://indeed.com/a_job",
    "searched_skills": ["python", "django"],
    "include_resume_skills_in_match": False,
    "pre_compiled_coverletter": None,
}

if local:
    url = 'http://127.0.0.1:5000/job-match'
else:
    url = 'https://YOUR_API_HOST/job-match'

if run_job_match:
    r = requests.post(url, json=create_job_application_payload)

    if r.status_code == 200:
        print(r.status_code)
        print("success: run_job_match")
        if print_output:
            pprint(r.json(), width=1000)
    else:
        print("run_job_match failed. check API console output")
        print(r.status_code)


# multiple create job application
test_positions = [
    'Software Developer in Melbourne, Australia',
    'Software Developer',
    'software developer',
    'Java Developer',
    'Donkey trainer',
    'Horse trainer',
    'Graduate Software Development and Engineering',
    'Junior Software Engineer',
    'Graduate Front End Developer',
    'Web Developer',
    'Junior Web Developer/Content Publisher',
    'Junior Software Developer',
    'SaaS Software Developer - Graduate',
    'Software Developer',
    'Associate Software Developer',
    'Web Developer (React.js)',
    'Junior Web Developer - Full time - Preston VIC',
]

for i in test_positions:
    create_job_application_payload = {
        "candidate_name": "anne laura",
        "parsed_resume": None,
        "resume_file_link": None,
        "hiring_manager_name": None,
        # "raw_job_title": "waiter",
        "raw_job_title": i,
        "job_ad_description": "Once upon a time there was a job",
        "company_name": "Microsoft",
        "hash_id": "as87df87as6df87as6df",
        "source_url": "https://indeed.com/a_job",
        "searched_skills": ["python", "django"],
        "include_resume_skills_in_match": False,
        "pre_compiled_coverletter": None,
        "chrome_app_version": "0.0.1"
    }

    if local:
        url = 'http://127.0.0.1:5000/create-job-application'
    else:
        url = 'https://YOUR_API_HOST/create-job-application'

    if run_multiple_create_job_application:
        r = requests.post(url, json=create_job_application_payload)

        if r.status_code == 200:
            # print(r.status_code)
            # print("success: create-job-application")
            if print_output:
                pprint(r.json(), width=1000)
        else:
            print(i, " failed.")
            print(r.status_code)

#######

# mass-create-job-application

mass_create_job_application_payload = {
    "job_ads": [
        {
            "candidate_name": "anne laura",
            "parsed_resume": None,
            "resume_file_link": None,
            "hiring_manager_name": None,
            # "raw_job_title": "waiter",
            "raw_job_title": "software developer",
            "job_ad_description": "Once upon a time there was a job",
            "company_name": "Microsoft",
            "hash_id": "as87df87as6df87as6df",
            "source_url": "https://indeed.com/a_job",
            "searched_skills": ["python", "django"],
            "include_resume_skills_in_match": False,
            "pre_compiled_coverletter": None,
            "chrome_app_version": "0.0.1"
        },
        {
            "candidate_name": "anne laura",
            "parsed_resume": None,
            "resume_file_link": None,
            "hiring_manager_name": None,
            # "raw_job_title": "waiter",
            "raw_job_title": "software developer",
            "job_ad_description": "Once upon a time there was a job",
            "company_name": "Microsoft",
            "hash_id": "as87df87as6df87as6df",
            "source_url": "https://indeed.com/a_job",
            "searched_skills": ["python", "django"],
            "include_resume_skills_in_match": False,
            "pre_compiled_coverletter": None,
            "chrome_app_version": "0.0.1"
        }
    ]
}

if local:
    url = 'http://127.0.0.1:5000/mass-create-job-applications'
else:
    url = 'https://YOUR_API_HOST/mass-create-job-applications'

if run_mass_create_job_application:
    r = requests.post(url, json=mass_create_job_application_payload)

    if r.status_code == 200:
        print(r.status_code)
        print("success: mass-create-job-application")
        if print_output:
            pprint(r.json(), width=1000)
    else:
        print("mass-create-job-application failed. check API console output")
        print(r.status_code)

# coverletter html

coverletter_html_payload = {
    "raw_job_title": "Youth Director",
    "company_name": "Microsoft",
    "candidate_name": "Sarah Doe",
    "sign_off": None,
    "contact_number": None,
    "date": None,
    "pre_intro": None,
    "email": None,
    "intro_paragraph": None,
    "body_paragraphs": None,
    "outro_paragraph": None,
    "parsed_resume": None,
    "resume_file_link": None,
    "hiring_manager_name": None,
    "pre_compiled_coverletter_text": "This is a coverletter"
}

if local:
    url = 'http://127.0.0.1:5000/coverletter_as_html'
else:
    url = 'https://YOUR_API_HOST/coverletter_as_html'

if run_coverletter_html:
    r = requests.post(url, json=coverletter_html_payload)

    if r.status_code == 200:
        print(r.status_code)
        print("success: coverletter_html")
        if print_output:
            pprint(r.json(), width=1000)
    else:
        print("coverletter_html failed. check API console output")
        print(r.status_code)

if local:
    url = 'http://127.0.0.1:5000/mass-create-job-applications'
else:
    url = 'https://YOUR_API_HOST/mass-create-job-applications'

if run_mass_create_job_application:
    r = requests.post(url, json=mass_create_job_application_payload)

    if r.status_code == 200:
        print(r.status_code)
        print("success: mass-create-job-application")
        if print_output:
            pprint(r.json(), width=1000)
    else:
        print("mass-create-job-application failed. check API console output")
        print(r.status_code)

# test resume
stylize_resume_payload = {
    "page_numbers": 1,
    "elements_overflowed": [],
    "elements_overflowed_bottom_margins": [],
  "personal": {
    "profile_summary": None,
    "skills": [
      "python",
      "django"
    ],
    "tools": [
      "word",
      "photoshop"
    ],
    "languages": [
      "enlish",
      "french"
    ],
    "first_name": "first_name",
    "middle_name": "middle_name",
    "last_name": "last_name",
    "position_title": "software developer",
    "address": "10 something st",
    "city": "Melbourne",
    "state": "Vic",
    "email": "email@s.com",
    "phone": "12345678",
    "zip_code": "1234"
  },
  "experiences": [
    {
      "experience_position": "test",
      "experience_company": "micro",
      "experience_location": "melbourne",
      "experience_work_start_date": "2021-03-14",
      "experience_work_end_date": "2021-03-14",
      "experience_currently_working_here": None,
      "experience_position_description": "test test test",
      "selected_accomplishments": [
        "I did something great",
        "I did something else great"
      ]
    },
    {
      "experience_position": "test2",
      "experience_company": "micro2",
      "experience_location": "melbourne",
      "experience_work_start_date": "2021-03-14",
      "experience_work_end_date": "2021-03-14",
      "experience_currently_working_here": None,
      "experience_position_description": "test2 test test",
      "selected_accomplishments": [
        "I did something great 2",
        "I did something else great 2"
      ]
    }
  ],
  "education": [
    {
      "institution": "test",
      "degree": "masters something",
      "field": "software",
      "education_start_date": "2021-03-14",
      "education_end_date": "2021-03-14",
      "selected_accomplishments": [
        "I did something great",
        "I did something else great"
      ]
    },
    {
      "institution": "test2",
      "degree": "masters something2",
      "field": "software",
      "education_start_date": "2021-03-14",
      "education_end_date": "2021-03-14",
      "selected_accomplishments": [
        "I did something great2",
        "I did something else great2"
      ]
    }
  ],
  "references": [
    {
      "first_name": "test",
      "last_name": "test",
      "current_position": "software developer",
      "phone": "12345678",
      "email": "test@asdf.com"
    },
    {
      "first_name": "test2",
      "last_name": "test2",
      "current_position": "software developer",
      "phone": "123456782",
      "email": "test2@asdf.com"
    }
  ]
}

if local:
    url = 'http://127.0.0.1:5000/stylize_resume'
else:
    url = 'https://YOUR_API_HOST/stylize_resume'

if run_stylize_resume:
    r = requests.post(url, json=stylize_resume_payload)

    if r.status_code == 200:
        print(r.status_code)
        print("success: stylize_resume")
        if print_output:
            pprint(r.json(), width=1000)
    else:
        print("stylize_resume failed. check API console output")
        print(r.status_code)
