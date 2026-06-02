import html2text
from bs4 import BeautifulSoup


def convert_job_ad_description(job_ad_description):
    if type(job_ad_description) == list:
        output = ' '.join(job_ad_description)
    else:
        output = job_ad_description

    is_html = bool(BeautifulSoup(output, "html.parser").find())
    if is_html:
        output = html2text.html2text(job_ad_description)
    else:
        pass

    return output


print("input: single line string")
job = "this is a job"
print("-------------")
print("output: ",convert_job_ad_description(job))

print("-------------")
print("input: multi line string")
job = """
this is a 

multiline job
"""
print("-------------")
print("output: ",convert_job_ad_description(job))
print("-------------")
print("input: single line HTML")
job = "<p><strong>this</strong> is a html job</p>"
print("-------------")
print("output: ",convert_job_ad_description(job))
print("-------------")

print("input: multi line HTML")

job = """
<p><strong>this</strong> is a html job</p>

<p><strong>this</strong> is a html job</p>
"""
print("-------------")
print("output: ",convert_job_ad_description(job))

print("-------------")
print("input: list of sentences")
job = ["this","is", "a", "job","as a list (javascript array)"]
print("-------------")
print("output: ",convert_job_ad_description(job))
print("-------------")