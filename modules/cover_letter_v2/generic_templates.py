recruitment_titles = [
    'recruitment manager',
    'head of recruitment',
    'employment manager'
]

intro_sentences = [
    "It is a pleasure to be applying for this position at your company."
]

body_sentences = [
    "As someone with an extensive background in the field, I am well-equipped to provide the necessary expertise to compliment your team. My passion for the field makes me confident in my ability to fulfill this role."
    "During my previous employment tenure, I worked in numerous areas of relevance."
    "I make it a priority to put the needs of others first and to always meet deadlines."
    "I am well-aware of the careful planning and dedication this position requires."
    "My abilities stem from my University education which taught me the knowledge needed to apply my skills."
]


outro_sentences = [
    "The opportunity to discuss the position in further detail would be most welcome.",
    "I look forward to discussing the position with you further. Thank you for your consideration.",
    "I would appreciate the opportunity to discuss this position and my qualifications with you further.",
    "I look forward to the opportunity to discuss this position and my qualifications with you further.",
    "I would like to thank you for reviewing my application.",
    "I look forward to learning more about your company and the responsibilities this position entails"
]

conclusion_sentences = [
    "Thank you for your consideration.",
    "I appreciate your consideration.",
    "Thank you for your kind consideration.",
    "Thank you for your time and consideration.",
    "Thank you for reviewing my application."
]

sign_offs = [
    "Sincerely,",
    "Yours Sincerely,",
    "Kind Regards,",
    "Kindest Regards,",
    "Warm Regards,",
    "Warmest Regards,"
]



# intro_plug_sentences = [
#     [
#         "I saw that {} was hiring a {}, and I felt compelled to send you my resume.",
#         "company",
#         "position"
#     ],
#     [
#         "I am thrilled to submit this application for the role of {} at {}.",
#         "position",
#         "company"
#     ],
#     [
#         "It is my privilege to apply for the position of {} at {}.",
#         "position",
#         "company"
#     ]
# ]




# each must have exactly two {}.
# Format [sentence,first filler("company" or "position"), second filler("company" or "position")]
# fillers can only be "position" or "company" - must be exact match.
# position and company can be in ANY order¡™¡


education_sentences_one_degree = [
    [
        "Along with my experience in the field of {}, I also possess a {} from {}.",

        "industry",
        "degree",
        "institution"],
    [
        "Complimentary to my experience in the field, I also possess a {} from {}.",

        "degree",
        "institution"
    ],
    [
        "With regards to my education, I possess a {} from {}.",

        "degree",
        "institution"
    ]
]

education_sentences_two_degrees = [
    [
        "Along with my experience in the field of {}, I also possess both a {} from {}, and a {} from {}.",

        "industry",
        "degree_1",
        "institution_1",
        "degree_2",
        "institution_2"
    ],
    [
        "Complimentary to my experience in the field, I also possess a {} from {} and a {} from {}.",

        "degree_1",
        "institution_1",
        "degree_2",
        "institution_2"
    ],
    [
        "With regards to my education, I possess a {} from {} and a {} from {}.",

        "degree_1",
        "institution_1",
        "degree_2",
        "institution_2"
    ]
]

# do not at total_years variable more than once per collection.
experience_sentences = [
    [
        "As a highly skilled professional with a considerable track record spanning {} years in {}, I am both qualified for the position and passionate about the field.",
        "total_years",
        "position_sub_industry"
    ],
    [
        "As a successful {} and spanning {} years of experience, I can bring substantial knowledge and experience to this role.",
        "position",
        "total_years"
    ],
    [
        "As a highly skilled professional with a considerable track record in {}, I am both qualified for the position and passionate about the field.",
        "position_sub_industry"
    ],
    [
        "Due to my significant experience and expertise in {}, I can bring substantial knowledge and experience in this role as a {}.",
        "position_sub_industry",
        "position"
    ]

]

# Can contain a single {}
# must be "previous_company"
selected_accomplishments_dot_points_sentences = [
    [
        "Highlights of my experience during my employment at {} include:",
        "previous_company"
    ],
    [
        "Some highlights of my experience at {} include:",
        "previous_company"
    ],
    [
        "A selection of highlights regarding my experience at {} include:",
        "previous_company"
    ]
]
