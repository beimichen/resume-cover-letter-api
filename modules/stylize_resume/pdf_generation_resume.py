from datetime import datetime
from difflib import SequenceMatcher
import operator
import string
import random


def find_overflow_margins(target_element, elements_overflowed_list, elements_overflowed_margins_list):
    if target_element in elements_overflowed_list:
        element_index = elements_overflowed_list.index(target_element)
        element_margin = elements_overflowed_margins_list[element_index]
        return element_margin
    else:
        return None


def default_template_resume_pdf(resume):
    num_of_pages = resume['page_numbers']
    elements_overflowed = resume['elements_overflowed']
    elements_overflowed_bottom_margins = resume['elements_overflowed_bottom_margins']
    # find_overflow_margins(target_element, elements_overflowed, elements_overflowed_bottom_margins)
    inline_styling = """
            html,body,div,span,object,iframe,h1,h2,h3,h4,h5,h6,p,blockquote,pre,abbr,address,cite,code,del,dfn,em,img,ins,kbd,q,samp,small,strong,sub,sup,var,b,i,dl,dt,dd,ol,ul,li,fieldset,form,label,legend,table,caption,tbody,tfoot,thead,tr,th,td,article,aside,canvas,details,figcaption,figure,footer,header,hgroup,menu,nav,section,summary,time,mark,audio,video {
        border:0;
        font:inherit;
        font-size:100%;
        margin:0;
        padding:0;
        vertical-align:baseline;
        float: none;
        position: static;
        overflow: visible;
        }
        
        article,aside,details,figcaption,figure,footer,header,hgroup,menu,nav,section {
        display:block;
        }
        
        html, body {background: white; font-family: 'Lato', helvetica, arial, sans-serif; font-size: 16px; color: #222;}
        
        .clear {clear: both;}
        
        p {
            font-size: 1em;
            line-height: 1.4em;
            color: #444;
        }
        
        #cv {
            width: 100%;
            max-height: 297mm;
            page-break-after:always;
            background: white;
            margin: 0;
            overflow:visible;
        }
        
        .mainDetails {
            padding: 25px 35px;
            border-bottom: 2px solid #cf8a05;
            background: white;
        }
        
        #name h1 {
            font-size: 2.5em;
            font-weight: 700;
            font-family: 'Rokkitt', Helvetica, Arial, sans-serif;
            margin-bottom: -6px;
        }
        
        #name h2 {
            font-size: 2em;
            margin-left: 2px;
            font-family: 'Rokkitt', Helvetica, Arial, sans-serif;
        }
        
        #mainArea {
            padding: 0 40px;
        }
        
        #headshot {
            width: 12.5%;
            float: left;
            margin-right: 30px;
        }
        
        #headshot img {
            width: 100%;
            height: auto;
            -webkit-border-radius: 50px;
            border-radius: 50px;
        }
        
        #name {
            float: left;
        }
        
        #contactDetails {
            float: right;
        }
        
        #contactDetails ul {
            list-style-type: none;
            font-size: 0.9em;
            margin-top: 2px;
        }
        
        #contactDetails ul li {
            margin-bottom: 3px;
            color: #444;
        }
        
        #contactDetails ul li a, a[href^=tel] {
            color: #444;
            text-decoration: none;
            -webkit-transition: all .3s ease-in;
            -moz-transition: all .3s ease-in;
            -o-transition: all .3s ease-in;
            -ms-transition: all .3s ease-in;
            transition: all .3s ease-in;
        }
        
        #contactDetails ul li a:hover {
            color: #cf8a05;
        }
        
        # .profile-section {
        #     margin-bottom:20px;
        # }
        
        .experience-section article ul {
            margin-bottom:20px;
            padding-left: 40px;
        }
        
        section {
            border-top: 1px solid #dedede;
            padding: 20px 0 0;
        }
        
        section:first-child {
            border-top: 0;
        }
        
        section:last-child {
            padding: 20px 0 10px;
        }
        
        .sectionTitle {
            float: left;
            width: 25%;
        }
        
        .sectionContent {
            float: right;
            width: 72.5%;
        }
        
        .sectionTitle h1 {
            font-family: 'Rokkitt', Helvetica, Arial, sans-serif;
            font-style: italic;
            font-size: 1.5em;
            color: #cf8a05;
        }
        
        .sectionContent h2 {
            font-family: 'Rokkitt', Helvetica, Arial, sans-serif;
            font-size: 1.5em;
            margin-bottom: -2px;
        }
        
        .education-section article ul {
            margin-bottom:20px;
            padding-left: 40px;
        }
        
        # .skills-section {
        #     margin-bottom:20px;    
        # }
        # 
        # .tools-section {
        #     margin-bottom:20px;
        # }
        # 
        # .languages-section {
        #     margin-bottom:20px;
        # }
        # 
        # .references-section {
        #     margin-bottom:20px;
        # }
        
        .subDetails {
            font-size: 0.8em;
            font-style: italic;
            margin-bottom: 3px;
        }
        
        .keySkills {
            list-style-type: none;
            -moz-column-count:3;
            -webkit-column-count:3;
            column-count:3;
            font-size: 1em;
            color: #444;
        }
        
        .keySkills ul li {
            margin-bottom: 3px;
        }
        
        @-webkit-keyframes reset {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 0;
            }
        }
        
        @-webkit-keyframes fade-in {
            0% {
                opacity: 0;
            }
            40% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }
        
        @-moz-keyframes reset {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 0;
            }
        }
        
        @-moz-keyframes fade-in {
            0% {
                opacity: 0;
            }
            40% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }
        
        @keyframes reset {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 0;
            }
        }
        
        @keyframes fade-in {
            0% {
                opacity: 0;
            }
            40% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }
        
        * {
            box-sizing: border-box;
            -moz-box-sizing: border-box;
        }
        
        .page {
            width: 210mm;
            min-height: 297mm;
            padding:0;
            margin: 0;
            border: 0;
            /*border-radius: 5px;*/
            background-color: white;
            display: block
        }
        @page {
            size: A4;
            margin: 0;
            margin-bottom: 30px;
            margin-top: 40px;
        }"""

    if resume["personal"]["first_name"]:
        first_name = resume["personal"]["first_name"].title()
    else:
        first_name = ""

    if resume["personal"]["middle_name"]:
        middle_name = resume["personal"]["middle_name"].title()
    else:
        middle_name = ""

    if resume["personal"]["last_name"]:
        last_name = resume["personal"]["last_name"].title()
    else:
        last_name = ""

    if all(name for name in [first_name, middle_name, last_name]):
        candidate_name = ' '.join([first_name, middle_name, last_name])
    elif all(name for name in [first_name, last_name]):
        candidate_name = ' '.join([first_name, last_name])
    elif first_name:
        candidate_name = first_name
    elif last_name:
        candidate_name = last_name
    else:
        candidate_name = "No name provided - please " \
                         "add a name in the resume tab below"

    # Initiate all elements for header

    if resume["personal"]["address"]:
        address_text = '<p>{}<br>'.format(resume["personal"]["address"].title())

        if resume["personal"]["city"]:
            address_text += '{}<br>'.format(resume["personal"]["city"].title())
        else:
            pass

        if resume["personal"]["state"]:
            address_text += '{}<br>'.format(resume["personal"]["state"])
        else:
            pass

        if resume["personal"]["zip_code"]:
            address_text += '{}<br>'.format(resume["personal"]["zip_code"])
        else:
            pass
    else:
        address_text = ""

    if resume["personal"]["phone"]:
        phone_text = "<li>e: {}</li>".format(resume["personal"]["phone"])
    else:
        phone_text = ''

    if resume["personal"]["email"]:
        email_text = "<li>e: {}</li>".format(resume["personal"]["email"])
    else:
        email_text = ''

    contact_text = f'<ul>{phone_text}{email_text}</ul>'

    position = resume['personal']['position_title']

    header_template = f"""
    <html>
        <head>
        <title>{first_name} {last_name}</title>
        <link href='http://fonts.googleapis.com/css?family=Rokkitt:400,700|Lato:400,300' rel='stylesheet' type='text/css'>

        </head>
        <style>
            {inline_styling}
        </style>
        <body class="page">
        <div id="cv">
            <div class="mainDetails">

                <div id="name">
                    <h1>{first_name} {last_name}</h1>
                    <h2>{position}</h2>
                    {address_text}
                </div>

                <div id="contactDetails">
                    {contact_text}
                </div>
                <div class="clear"></div>
            </div>

            <div id="mainArea">
    """

    # Initiate all elements for body

    body_template_components = []

    # Profile

    profile_summmary_template = ''

    profile_summary_overflow = find_overflow_margins('.profile-section', elements_overflowed,
                                                     elements_overflowed_bottom_margins)

    if profile_summary_overflow:
        overflow_margin = profile_summary_overflow + 20
    else:
        overflow_margin = 20

    if resume['personal']["profile_summary"]:
        profile_summmary_template += f"""
                <section class="profile-section" style="margin-bottom:{overflow_margin}px;">
                    <article>
                        <div class="sectionTitle">
                            <h1>Profile Summary</h1>
                        </div>

                        <div class="sectionContent">
                            <p>{resume['personal']["profile_summary"]}</p>
                        </div>
                    </article>
                    <div class="clear"></div>
                </section>"""

        body_template_components.append(profile_summmary_template)

    # Experience:

    experience_text = ''

    if resume["experiences"]:

        for experience in resume["experiences"]:

            experience_text += '<article>'

            experience_text += f'<h2>{experience["experience_company"]}</h2>'
            experience_text += f'<h4>{experience["experience_location"]}</h4>'

            if experience["experience_work_start_date"]:
                start_dmy = datetime.strptime(experience["experience_work_start_date"], '%Y-%m-%d')
                start_date = str(start_dmy.year)
            else:
                start_date = ""

            if experience["experience_work_end_date"]:
                end_dmy = datetime.strptime(experience["experience_work_end_date"], '%Y-%m-%d')
                end_date = str(end_dmy.year)
            else:
                end_date = "Present"

            if experience["experience_currently_working_here"]:
                end_date = "Present"

            position_line = experience["experience_position"] + ", " + start_date + " - " + end_date

            experience_text += f'<p class="subDetails">{position_line}</p>'

            experience_text += f'<p>{experience["experience_position_description"]}</p>'

            experience_text_bullet_points = '<ul style="margin-left:20px;">'

            if experience["selected_accomplishments"]:
                for selected_accomplishment in experience["selected_accomplishments"]:
                    experience_text_bullet_points += f'<li>{selected_accomplishment}</li>'

            experience_text_bullet_points += '</ul>'

            experience_text += experience_text_bullet_points

            # Create data to post to API create endpoint

            experience_text += '<p></p>'

            experience_text += '</article>'

        experience_overflow = find_overflow_margins('.experience-section', elements_overflowed,
                                                    elements_overflowed_bottom_margins)

        if experience_overflow:
            overflow_margin = experience_overflow + 20
        else:
            overflow_margin = 0

        work_experience_template = f"""
        <section class="experience-section" style="margin-bottom:{overflow_margin}px">
        <div class="sectionTitle">
            <h1>Work Experience</h1>
        </div>
        <div class="sectionContent">
            {experience_text}
        </div>    
        <div class="sectionContent">
        </div>
        <div class="clear"></div>
        </section>
        """

        body_template_components.append(work_experience_template)

    # Education

    education_text = ''

    if resume["education"]:
        for education in resume["education"]:
            education_text += '<article>'
            education_text += f'<h2>{education["institution"].title()}</h2>'

            degree_start_dmy = datetime.strptime(education["education_start_date"], "%Y-%m-%d")
            degree_start = str(degree_start_dmy.year)
            degree_end_dmy = datetime.strptime(education["education_end_date"], "%Y-%m-%d")
            degree_end = str(degree_end_dmy.year)

            degree_line_full = education["degree"] + ", " + degree_start + " - " + degree_end

            education_text += f'<p class="subDetails">{degree_line_full}</p>'

            education_text_bullet_points = ''
            education_key_achievement_text = ''

            if education["selected_accomplishments"]:
                for selected_accomplishment in education["selected_accomplishments"]:
                    education_key_achievement_text += f'<li>{selected_accomplishment}</li>'

                education_text_bullet_points += '<ul style="margin-left:20px;">' + education_key_achievement_text + \
                                                '</ul>'
                education_text += education_text_bullet_points

            education_text += '</article>'

        education_overflow = find_overflow_margins('.education-section', elements_overflowed,
                                                   elements_overflowed_bottom_margins)

        if education_overflow:
            overflow_margin = education_overflow + 20
        else:
            overflow_margin = 0

        education_template = f"""
        <section class="education-section" style="margin-bottom:{overflow_margin}px">
            <div class="sectionTitle">
                <h1>Education</h1>
            </div>

            <div class="sectionContent">
                {education_text}
            </div>
            <div class="clear"></div>
        </section>
        """

        body_template_components.append(education_template)

    # Skills

    skills_text = ''

    skills_overflow = find_overflow_margins('.skills-section', elements_overflowed,
                                            elements_overflowed_bottom_margins)

    if skills_overflow:
        overflow_margin = skills_overflow + 20
    else:
        overflow_margin = 20

    if resume["personal"]["skills"]:
        for skill in resume["personal"]['skills']:
            skills_text += f'<li>{skill}</li>'

        skills_template = f"""
        <section class="skills-section" style="margin-bottom:{overflow_margin}px">
            <div class="sectionTitle">
                <h1>Skills</h1>
            </div>
    
            <div class="sectionContent">
                <ul class="keySkills">
                    {skills_text}
                </ul>
            </div>
            <div class="clear"></div>
        </section>"""

        body_template_components.append(skills_template)

    # Tools

    tools_text = ''

    if resume["personal"]["tools"]:

        for tool in resume["personal"]["tools"]:
            tools_text += f'<li>{tool}</li>'

        tools_overflow = find_overflow_margins('.tools-section', elements_overflowed,
                                               elements_overflowed_bottom_margins)

        if tools_overflow:
            overflow_margin = tools_overflow + 20
        else:
            overflow_margin = 20

        tools_template = f"""
                <section class="tools-section" style="margin-bottom:{overflow_margin}px">
                    <div class="sectionTitle">
                        <h1>Tools</h1>
                    </div>

                    <div class="sectionContent">
                        <ul class="keySkills">
                            {tools_text}
                        </ul>
                    </div>
                    <div class="clear"></div>
                </section>"""

        body_template_components.append(tools_template)

    # Languages

    languages_text = ''
    if resume["personal"]["languages"]:
        resumeLastItem = len(resume["personal"]["languages"]) - 1
        for ind, language in enumerate(resume["personal"]["languages"]):
            _language = language['language']
            _language_level = language['level']
            if ind == resumeLastItem:
                languages_text += f'<p style="margin-bottom:0px;">{_language}</p><p style="font-size:12px;font-style:italic;">{_language_level}</p>'
            else:
                languages_text += f'<p style="margin-bottom:0px;">{_language}</p><p style="font-size:12px;font-style:italic;margin-bottom:10px;">{_language_level}</p>'

        languages_overflow = find_overflow_margins('.languages-section', elements_overflowed,
                                                   elements_overflowed_bottom_margins)

        if languages_overflow:
            overflow_margin = languages_overflow + 20
        else:
            overflow_margin = 20

        languages_template = f"""
        <section class="languages-section" style="margin-bottom:{overflow_margin}px">
            <div class="sectionTitle">
                <h1>Languages</h1>
            </div>

            <div class="sectionContent">
                {languages_text}
            </div>
            <div class="clear"></div>
        </section>"""

        body_template_components.append(languages_template)

    # References
    references_text = ''

    if resume["references"]:

        for referee in resume["references"]:

            references_text += '<article>'

            if referee["first_name"] and referee["last_name"]:
                full_name = referee["first_name"].capitalize() + " " + referee["last_name"].capitalize()
                references_text += f'<h2>{full_name}</h2>'
            elif referee["first_name"]:
                references_text += f'<h2>{referee["first_name"]}</h2>'
            else:
                pass

            if referee["current_position"]:
                references_text += f'<p class="subDetails">{referee["current_position"]}</p>'
            else:
                pass

            if referee["phone"]:
                references_text += f'<p>Phone: {referee["phone"]}</p>'
            else:
                pass

            if referee["email"]:
                references_text += f'<p>Email: {referee["email"]}</p>'
            else:
                pass

            references_text += '</article>'

        references_overflow = find_overflow_margins('.references-section', elements_overflowed,
                                                    elements_overflowed_bottom_margins)

        if references_overflow:
            overflow_margin = references_overflow + 20
        else:
            overflow_margin = 20

        references_template = f"""
        <section class="references-section" style="margin-bottom:{overflow_margin}px">
            <div class="sectionTitle">
                <h1>References</h1>
            </div>

            <div class="sectionContent">
                {references_text}
            </div>
            <div class="clear"></div>
        </section>"""

        body_template_components.append(references_template)

    compiled_body_template = ' '.join(body_template_components)

    body_template = '<div id="mainArea">' + compiled_body_template + '</div>'

    footer_template = f"""
                </div>
            </div>
        </body>
    </html>
    """

    template = header_template + body_template + footer_template

    return template


if __name__ == '__main__':
    resume_test_object = {
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
                "experience_work_start_date": "2021-04-02",
                "experience_work_end_date": "2021-04-02",
                "experience_currently_working_here": True,
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
                "experience_work_start_date": "2021-04-02",
                "experience_work_end_date": "2021-04-02",
                "experience_currently_working_here": True,
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
                "education_start_date": "2021-04-02",
                "education_end_date": "2021-04-02",
                "selected_accomplishments": [
                    "I did something great",
                    "I did something else great"
                ]
            },
            {
                "institution": "test2",
                "degree": "masters something2",
                "field": "software",
                "education_start_date": "2021-04-02",
                "education_end_date": "2021-04-02",
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

    template = default_template_resume_pdf(resume_test_object)
    with open("test.html", "w") as f:
        f.write(template)
