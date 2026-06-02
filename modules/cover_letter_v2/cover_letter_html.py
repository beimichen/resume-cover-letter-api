import time


def create_cv_html(insertable_position, company, user_name, sign_off, contact_number, date, pre_intro, email, intro_paragraph,
                   body_paragraphs, outro_paragraph, user_name_present, pre_compiled_coverletter_text):

    position = insertable_position.title()

    if user_name:
        full_name = user_name
    else:
        full_name = '[user_name]'

    full_cover_letter_html = []


    if contact_number:
        contact_ptext = '<h3 style="font-weight:700;margin-bottom:0px!important;">{}</h3>'.format(contact_number)
        full_cover_letter_html.append(contact_ptext)

    if email:
        email_ptext = '<h3 style="font-weight:700;margin-bottom:0px!important;">{}</h3>'.format(email)
        full_cover_letter_html.append(email_ptext)

    if company:
        company_ptext = '<h3 style="font-weight:700;margin-bottom:20px!important;">{}</h3>'.format(company)
        full_cover_letter_html.append(company_ptext)

    if not pre_compiled_coverletter_text:

        addressee_ptext = '<div>{}</div>'.format(pre_intro.strip('\n'))

        full_cover_letter_html.append(addressee_ptext)

        intro_ptext = '<div>{}</div>'.format(intro_paragraph.strip('\n'))

        full_cover_letter_html.append(intro_ptext)

        list_sentences_indices_in_body_paragraphs = []
        list_sentences_indices_in_full_cover_letter_html = []

        for ind, par in enumerate(body_paragraphs):
            if '*' in par or '•' in par:
                li_text = '<li>{}</li>'.format(par)
                full_cover_letter_html.append(li_text.strip('\n'))
                global_index = len(full_cover_letter_html) - 1
                list_sentences_indices_in_body_paragraphs.append(ind)
                list_sentences_indices_in_full_cover_letter_html.append(global_index)
            else:
                body_ptext = '<div>{}</div>'.format(par)
                full_cover_letter_html.append(body_ptext.strip('\n'))

        if list_sentences_indices_in_body_paragraphs:
            pre_bullet_point_sentence_index_in_body = list_sentences_indices_in_body_paragraphs[0] - 1
            last_bullet_point_sentence_index_in_body = list_sentences_indices_in_body_paragraphs[-1]
            bullet_point_par = ''.join(
                body_paragraphs[pre_bullet_point_sentence_index_in_body:last_bullet_point_sentence_index_in_body])
            bullet_point_par = '<ul>' + bullet_point_par + '</ul>'
            global_pre_bullet_point_sentence_index = list_sentences_indices_in_full_cover_letter_html[0] - 1
            global_last_bullet_point_index = list_sentences_indices_in_full_cover_letter_html[-1]
            full_cover_letter_html = full_cover_letter_html[
                                     0:global_pre_bullet_point_sentence_index] + [
                                         bullet_point_par] + full_cover_letter_html[
                                                             global_last_bullet_point_index:]

        outro_ptext = '<div>{}</div>'.format(outro_paragraph.strip('\n'))

        full_cover_letter_html.append(outro_ptext)

        sign_off_ptext = '<div>{}</div>'.format(sign_off.strip('\n'))

        full_cover_letter_html.append(sign_off_ptext)

    else:
        # print(pre_compiled_coverletter_text)
        cover_letter_text_split = pre_compiled_coverletter_text.splitlines()
        sign_off_text = cover_letter_text_split[-2]
        for paragraph in cover_letter_text_split:
            if paragraph == sign_off_text:
                print(paragraph)
                coverletter_ptext = '<div style="font-weight:500;margin-bottom:0px!important;">{}</div>'.format(paragraph.strip('\n'))
            elif '•' in paragraph:
                coverletter_ptext = '<div style="font-weight:500;margin-bottom:0px!important;">{}</div>'.format(paragraph.strip('\n'))
            else:
                coverletter_ptext = '<div style="font-weight:500;margin-bottom:10px;">{}</p>'.format(paragraph.strip('\n'))

            full_cover_letter_html.append(coverletter_ptext)

    # if user_name_present is False:
    #     full_name_ptext = '<p>{}</p>'.format(full_name.strip('\n'))
    #     full_cover_letter_html.append(full_name_ptext)

    if not date:
        date = ""

    if not position:
        position = ""

    formatted_cover_letter_html = []

    for text in full_cover_letter_html:
        formatted_cover_letter_html.append(text)

    cover_letter_compiled = ''.join(formatted_cover_letter_html)

    inline_styling = """
    
    article,aside,details,figcaption,figure,footer,header,hgroup,menu,nav,section {
        display:block;
    }
    
    html, body {
        background: white; 
        font-size: 13.5px; 
        color: #222;
    }
    
    .clear {
        clear: both;
    }
    
    p, div {
        font-size: 13.5px;
        line-height: 1.4em;
        margin-bottom: 10px;
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
        font-size: 18px;
        font-weight: 700;
        margin-bottom: -6px;
    }
    
    #name h2 {
        font-size: 2em;
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
        font-style: italic;
        font-size: 1.5em;
        color: #cf8a05;
    }
    
    .sectionContent h2 {
        font-size: 1.5em;
        margin-bottom: -2px;
    }
    
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
        margin-bottom: 20px;
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
    }
    """

    full_html_template = f"""
                <html>
                    <head>
                    <title>{full_name} - Curriculum Vitae</title>

                    <link type="text/css" rel="stylesheet" href="style.css">
                    <link href='http://fonts.googleapis.com/css?family=Rokkitt:400,700|Lato:400,300' rel='stylesheet' type='text/css'>

                    </head>
                    <body class="page">
                    <div id="cv">
                        <div class="mainDetails">

                            <div id="name">
                                <h1>{full_name}</h1>
                                <h2>{position}</h2>
                            </div>

                            <div id="contactDetails">
                                <ul>
                                    <li>{date}</li>
                                </ul>
                            </div>
                            <div class="clear"></div>
                        </div>

                        <div id="mainArea">
                            <section>
                                <article>

                                    <div class="sectionCoverLetter">
                                        {cover_letter_compiled}
                                    </div>
                                </article>
                                <div class="clear"></div>
                            </section>

                        </div>
                    </div>
                    </body>
                    </html>
                """

    full_html_template_with_inline_css = f"""
                    <html>
                        <head>
                        <title>{full_name} - Curriculum Vitae</title>

                        <style>
                            {inline_styling}
                        </style>
                        <link href='http://fonts.googleapis.com/css?family=Rokkitt:400,700|Lato:400,300' rel='stylesheet' type='text/css'>
                        
                        </head>
                        <body class="page">
                        <div id="cv">
                            <div class="mainDetails">

                                <div id="name">
                                    <h1 style="margin-bottom:10px!important;">{full_name}</h1>
                                    <h2>{position}</h2>
                                </div>

                                <div id="contactDetails">
                                    <ul>
                                        <li>{date}</li>
                                    </ul>
                                </div>
                                <div class="clear"></div>
                            </div>

                            <div id="mainArea">
                                <section>
                                    <article>

                                        <div class="sectionCoverLetter">
                                            {cover_letter_compiled}
                                        </div>
                                    </article>
                                    <div class="clear"></div>
                                </section>

                            </div>
                        </div>
                        </body>
                        </html>
                    """


    return full_html_template, full_html_template_with_inline_css

if __name__ == '__main__':
    full_html_template, full_html_template_with_inline_css = create_cv_html(
        position="dev",
        company="micro",
        user_name="John",
        sign_off=None,
        contact_number="9234 2347",
        date="21/03/2021",
        pre_intro=None,
        email="goat@goat.com",
        intro_paragraph=None,
        body_paragraphs=None,
        outro_paragraph=None,
        pre_compiled_coverletter_text="Yep this is it.")

    with open("test_coverletter_output.html", "w") as f:
        f.write(full_html_template_with_inline_css)