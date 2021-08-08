AWS_REGIONS = [
    'us-east-2',
    'us-east-1',
    'us-west-1',
    'us-west-2',
    'af-south-1',
    'ap-east-1',
    'ap-south-1',
    'ap-northeast-3',
    'ap-northeast-2',
    'ap-southeast-1',
    'ap-southeast-2',
    'ap-northeast-1',
    'ca-central-1',
    'eu-central-1',
    'eu-west-1',
    'eu-west-2',
    'eu-south-1',
    'eu-west-3',
    'eu-north-1',
    'me-south-1',
    'sa-east-1',
    'us-gov-east-1',
    'us-gov-west-1',
]

POSTGRES_BACKUP_SCRIPT_TEMPLATE = """
cd /root/backup
MOMENT="$(date +%H%M%S)"
YEAR="$(date +%Y)"
MONTH="$(date +%m)"
DAY="$(date +%d)"
PGPASSWORD={} pg_dump -h {} -p {} -U {} {} > /root/backup/{}-$MOMENT.sql

AWS_ACCESS_KEY_ID={} AWS_SECRET_ACCESS_KEY={} AWS_DEFAULT_REGION={} aws s3 cp /root/backup/{}-$MOMENT.sql s3://{}/$YEAR/$MONTH/$DAY/
rm *.sql
"""


def do():
    project_name = input('Enter project name: ')
    while (region := input('Enter AWS region: ')) not in AWS_REGIONS:
        print('Invalid region')
    bucket_name = input('Enter S3 bucket name: ')
    access_key_id = input('Enter access key ID: ')
    secret_access_key = input('Enter secret access key ID: ')
    postgres_host = input('Enter db host: ')
    postgres_port = input('Enter db port: ')
    postgres_user = input('Enter db user: ')
    postgres_password = input('Enter db password: ')
    postgres_db = input('Enter db name: ')

    preview = POSTGRES_BACKUP_SCRIPT_TEMPLATE.format(postgres_password, postgres_host, postgres_port, postgres_user,
                                                     postgres_db, project_name, access_key_id, secret_access_key,
                                                     region, project_name, bucket_name)
    print(preview)


if __name__ == '__main__':
    do()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
