import time
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import logging

from weasyprint_custom.weasyprint_extended import CustomHTML
from weasyprint import CSS, default_url_fetcher
from weasyprint.fonts import FontConfiguration

from modules.cover_letter_v2.cover_letter_generator import CoverLetterCreator

# import os
import logging

logger = logging.getLogger(__name__)


def pdf_cover_letter(position, reconciled_position, full_name, company_name, contact, position_ad,
                     resume, cover_letter_components, version):

    date = str(time.strftime("%d/%m/%Y"))

    sender_id = version

    company_file_name = cover_letter_components["company"].replace(" ", "")

    full_filename = company_file_name + "_cover_letter_" + str(sender_id) + ".pdf"

    cv = CoverLetterCreator(reconciled_position=reconciled_position, raw_position=position, user_name=full_name,
                            employer_name=contact, company_name=company_name, ad_text=position_ad, resume=resume,
                            date=date)

    template, html_template, full_html_template_with_inline_css = cv.write_cover_letter()

    font_config = FontConfiguration()

    html = CustomHTML(string=html_template, base_url='weasyprint_css/')

    css = [
        CSS(filename='../weasyprint_css/style.css'),
    ]

    object_url = html.write_pdf_html(
        target=full_filename,
        stylesheets=css,
        font_config=font_config,
        data_type='coverletter'
    )

    logger.debug(object_url)

    return object_url, template, full_html_template_with_inline_css

# code for downloading:

# try:
#     s3.Bucket(bucket_name).download_file(filename, 'file2downloaded.pdf')
# except botocore.exceptions.ClientError as e:
#     if e.response['Error']['Code'] == "404":
#         print("The object does not exist.")
#     else:
#         raise
