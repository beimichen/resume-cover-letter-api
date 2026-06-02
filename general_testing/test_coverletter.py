from pprint import pprint

from modules.coverletter_v1.cover_letter import write_cover_letter

print("Built successfully")

l, c, diagnostic_report = write_cover_letter(
    "anne laura", # name
    "Lithium Industries12",  # company
    "software developer",  # position
    "java software developer", # raw_position
    "This is a job ad",  # position_ad (not used at the moment in coverletter.py)
    "Laura Jones",  # contact coverletter is addressed to
    "information and communication technology",  # Industry
    "Software Engineering",  # Sub Industry
    "d7df8sdf7sf87sh8df",  # user id
    {
        "first_name": "Camille",
        "middle_name": "Reubens",
        "last_name": "Moore",
        "address": "115 Bulleen Rd",
        "city": "Balwyn North",
        "state": "Victoria",
        "country": "Australia",
        "zip_code": 1234,
        "phone": "98899889",
        "email": "careub@tests.com",
        "profile_summary": "Highly creative and multitalented Graphic Designer with extensive experience in multimedia, marketing and print design. Exceptional collaborative and interpersonal skills; dynamic team player with well-developed written and verbal communication abilities. Highly skilled in client and vendor relations and negotiations; talented at building and maintaining “win-win” partnerships. Passionate and inventive creator of innovative marketing strategies and campaigns; accustomed to performing in deadline-driven environments with an emphasis on working within budget requirements.",
        "skills_tags": [
            "Website Design",
            "Video Editing",
            "Video Photomontages",
            "Photograph Restoration",
            "Retouching",
            "Lithography",
            "3D Animation"
        ],
        "tools_tags": [
            "Adobe Creative Suite",
            "Photoshop",
            "InDesign",
            "Illustrator",
            "AutoCAD"
        ],
        "languages": [
            {
                'language': 'ENGLISH',
                'level': 'NATIVE OR BILINGUAL PROFICIENCY'
            },
            {
                'language': 'FRENCH',
                'level': 'NATIVE OR BILINGUAL PROFICIENCY'
            },

        ],
        "experience": [
            {
                "company_name": "Market Studios Ltd.",
                "company_location": "Norwalk, California",
                "position_name": "software developer",
                "currently_working_here": False,
                "work_start_date": "2016-04-02",
                "work_end_date": "2018-04-03",
                "id": 1,
                "industry_name": "information and communication technology",
                "subindustry_name": "Software Engineering",
                "position_description": "Successfully translated subject matter into concrete design for newsletters, promotional materials and sales collateral. Created design theme and graphics for marketing and sales presentations, training videos and corporate websites. Participated in team effort to produce streamlined production of policy manuals and educational materials for newly hired employees and freelance designers.",
                "selected_accomplishment_1": "Earned several awards for providing graphic design support to both headquarter employees and hundreds of field offices.",
                "selected_accomplishment_2": "Coordinated staff participation in community-sponsored charitable events.",
                "selected_accomplishment_3": "Managed accounting and back office management"
            },
            {
                "company_name": "Cygnet Media Productions",
                "company_location": "Surrey Hills, Melbourne",
                "position_name": "3D illustrator",
                "currently_working_here": False,
                "work_start_date": "2012-04-02",
                "work_end_date": "2014-04-02",
                "id": 2,
                "industry_name": "information and communication technology",
                "subindustry_name": "Software Engineering",
                "position_description": "Successfully manage and coordinate graphic design projects from concept through completion. Work closely with clients to create vision, conceive designs, and consistently meet deadlines and requirements. Effectively build, motivate, and direct design and production teams. Coordinate freelance designers, consultants and vendors to meet all project requirements. Create and conduct highly persuasive sales and marketing presentations. Expertly convert features to benefits to achieve client objectives. Manage all operational, strategic, financial, quote/bid, staffing, and administrative functions.",
                "selected_accomplishment_1": "Successfully completed client projects worth up to $470,000",
                "selected_accomplishment_2": "Provided proposal layout and design for million-dollar corporate contracts under extremely tight deadlines",
                "selected_accomplishment_3": "Established trusting relationships with designers, vendors, and key clients"
            }
        ],
        "education": [
            {
                "degree": "Bachelor of Arts in Marketing, Minor in Graphic Arts",
                "institution_name": "University of Melbourne",
                "education_start_date": "2012-06-14",
                "education_end_date": "2013-06-14",
                "id": 1
            },
            {
                "degree": "3D Animation",
                "institution_name": "Swinbourne University",
                "education_start_date": "2015-06-14",
                "education_end_date": "2016-06-14",
                "id": 2
            }
        ],
        "referees": [
            {
                "first_name": "Laura",
                "last_name": "Paroux",
                "id": 1,
                "current_position_name": "Professor of Arts - Melbourne University",
                "phone": "0423 432 895",
                "email": "laura@testmail.com"
            },
            {
                "first_name": "Anne",
                "last_name": "Jones",
                "id": 1,
                "current_position_name": "Professor of Arts - Melbourne University",
                "phone": "0423 432 895",
                "email": "laura@testmail.com"
            }
        ]
    }, # resume
    {
        'q1': {
            'answer': "General question answer 1.",
            'lead_in': "lead in 1 - we're not using leadins yet"
        },
        'q2': {
            'answer': "General question answer 2.",
            'lead_in': "lead in 1 - we're not using leadins yet"
        }
    }, # general questions
    {'response_1': {'id': 1, 'user_response': 'laravel,interesting,django'},
     'response_2': {'id': 2, 'user_response': 'python,flask'},
     'response_3': {'id': 3, 'user_response': 'I can rebase Git repos without breaking production.'}}, # specific questions
    False,
    None,
)

pprint(l, width=1000)
print("===============")
pprint(c, width=1000)
print("===============")
pprint(diagnostic_report, width=1000)

l_empty, c_empty, diagnostic_report_empty = write_cover_letter(
    "", # name
    "",  # company
    "",  # position
    "", # raw_position
    "",  # position_ad (not used at the moment in coverletter.py)
    "",  # contact coverletter is addressed to
    "",  # Industry
    "",  # Sub Industry
    "",  # user id
    {}, # resume
    {}, # general questions
    {}, # specific questions
    False,
    None,
)
print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
pprint(l_empty, width=1000)
print("===============")
pprint(c_empty, width=1000)
print("===============")
pprint(diagnostic_report_empty, width=1000)
