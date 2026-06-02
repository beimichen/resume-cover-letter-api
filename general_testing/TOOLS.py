import os
import boto3
import requests
import json
import io
from datetime import datetime
from ast import literal_eval

now = datetime.now()


def check_environment(bucket_request):
    try:
        environment = os.environ['ENV_NAME']  # "https://YOUR_APP_HOST"
        admin = os.environ['superuser']
        password = os.environ['superuserpass']
        if environment == 'Local':
            try:
                env_url = 'http://127.0.0.1:8000'
                local_aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
                local_aws_secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
                session = boto3.Session(
                    aws_access_key_id=local_aws_access_key_id,
                    aws_secret_access_key=local_aws_secret_key,
                )
                s3 = session.resource('s3', region_name='us-west-2')
                if bucket_request == 'chat':
                    bucket = s3.Bucket('docgen-chat-staging')
                elif bucket_request == 'template':
                    bucket = s3.Bucket('docgen-action-templates-staging')
                return env_url, admin, password, bucket
            except Exception as e:
                print(e)
                print(e.args)
                print(
                    'please set up local environments: "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY". These are used to '
                    'access s3 buckets from your local environment.')
                pass
        elif environment == 'Staging':
            env_url = 'https://YOUR_APP_HOST'
            s3 = boto3.resource('s3', region_name='us-west-2')
            if bucket_request == 'chat':
                bucket = s3.Bucket('docgen-chat-staging')
            elif bucket_request == 'template':
                bucket = s3.Bucket('docgen-action-templates-staging')
            return env_url, admin, password, bucket
        elif environment == 'Production':
            env_url = 'https://YOUR_APP_HOST'
            s3 = boto3.resource('s3', region_name='us-west-2')
            if bucket_request == 'chat':
                bucket = s3.Bucket('docgen-chat')
            elif bucket_request == 'template':
                bucket = s3.Bucket('docgen-action-templates')
            return env_url, admin, password, bucket
    except Exception as e:
        print(e)
        print(e.args)
        print('Please set up environment variables: "ENV_NAME","superuser" and "superuserpass"')
        pass


def get_token(admin, password, environment):
    payload = {'username': admin, 'password': password}
    print("pass: ", password)
    print("admin: ", admin)
    token_url = environment + "/resume/api-token-auth/"
    print("TEST_TOKEN")
    print(token_url)
    r = requests.post(token_url, data=payload)
    print("r: ",r)
    token = r.text
    print("r text: ", token)
    token = literal_eval(token)
    print("literal eval: ", token)

    print("TEST1")
    token = token["token"]

    headers = {'Authorization': 'Token ' + token}

    return headers


def store_data_s3(data, data_type, sender_id, environment, non_entity_file_name=None):
    s3 = boto3.resource('s3', region_name='us-west-2')

    def putObject(s3Object, obj):
        s3object.put(
            Body=(bytes(json.dumps(object).encode('UTF-8')))
        )

    if data_type == 'company':
        file_name = data + '_' + sender_id + '.json'
        object = {
            'company': data,
            'timestamp': now.strftime("%d/%m/%Y %H:%M:%S"),
            'sender_id': sender_id
        }
        if environment == 'https;//YOUR_APP_HOST':
            s3object = s3.Object('docgen-entity-companies', file_name)
        else:
            s3object = s3.Object('docgen-entity-companies-staging', file_name)
        putObject(s3object, object)
    elif data_type == 'job':
        file_name = data + '_' + sender_id + '.json'
        object = {
            'job_title': data,
            'timestamp': now.strftime("%d/%m/%Y %H:%M:%S"),
            'sender_id': sender_id
        }
        if environment == 'https;//YOUR_APP_HOST':
            s3object = s3.Object('docgen-entity-jobs', file_name)
        else:
            s3object = s3.Object('docgen-entity-jobs-staging', file_name)
        putObject(s3object, object)
    elif data_type == 'cover-letter':
        file_name = non_entity_file_name + '.pdf'
        object = data
        if environment == 'https;//YOUR_APP_HOST':
            s3object = s3.Object('coverletters-docgen', file_name)
            bucket_name = 'coverletters-docgen'
        else:
            s3object = s3.Object('coverletters-docgen-staging', file_name)
            bucket_name = 'coverletters-docgen-staging'
        putObject(s3object, object)
        return bucket_name
    elif data_type == 'resume':
        file_name = non_entity_file_name + '.pdf'
        object = data
        if environment == 'https;//YOUR_APP_HOST':
            s3object = s3.Object('resume-docgen', file_name)
            bucket_name = 'resume-docgen-staging'
        else:
            s3object = s3.Object('resume-docgen-staging', file_name)
            bucket_name = 'resume-docgen-staging'
        putObject(s3object, object)
        return bucket_name


def fetch_data_from_s3_file(s3_file):
    try:
        data = s3_file.get()['Body'].read().decode('utf-8')
        return data
    except Exception as e:
        print(e)
        print(e.args)
        print('Please check S3 settings')
        pass


def fetch_data_from_s3_file_txt(s3_file):
    try:
        data = io.BytesIO(s3_file.get()['Body'].read())
        return data
    except Exception as e:
        print(e)
        print(e.args)
        print('Please check S3 settings')
        pass



def get_resume_api_endpoints(environment, django_user_id):
    resume_personal_url = environment + "/resume/personal-api/" + django_user_id + "/"
    resume_experience_url = environment + "/resume/experience-api/" + django_user_id + "/"
    resume_education_url = environment + "/resume/education-api/" + django_user_id + "/"
    resume_reference_url = environment + "/resume/reference-api/" + django_user_id + "/"
    urls = {
        'resume_personal_url': resume_personal_url,
        'resume_experience_url': resume_experience_url ,
        'resume_education_url': resume_education_url,
        'resume_reference_url': resume_reference_url
    }
    return urls

