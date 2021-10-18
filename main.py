from pathlib import Path
import stat

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
#!/bin/sh
cd {backuper_directory}
MOMENT="$(date +%H%M%S)"
YEAR="$(date +%Y)"
MONTH="$(date +%m)"
DAY="$(date +%d)"
FILENAME={project_name}-$MOMENT.sql
PGPASSWORD={postgres_password} pg_dump -h {postgres_host} -p {postgres_port} -U {postgres_user} {postgres_db} > {backuper_directory}/{project_name}/$FILENAME
AWS_ACCESS_KEY_ID={access_key_id} AWS_SECRET_ACCESS_KEY={secret_access_key} AWS_DEFAULT_REGION={region} aws s3 cp {backuper_directory}/{project_name}/$FILENAME s3://{bucket_name}/$YEAR/$MONTH/$DAY/
rm *.sql
"""

def prepare_dirs(project_path: str):
    if project_path.exists():
        print(f'{project_path} already exists')
    else:
        project_path.mkdir(exist_ok=False)
        return project_path

def do():
    current_path = Path().absolute()
    if current_path.parts[-1] != 'Backuper':
        print("Must be launched from within 'Backuper' directory")
        return
    project_name = input('Enter project name: ')
    if (project_path := prepare_dirs(current_path / project_name)) is not None:
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

        script = POSTGRES_BACKUP_SCRIPT_TEMPLATE.format(
            backuper_directory=current_path,
            project_name=project_name, 
            postgres_password=postgres_password, 
            postgres_host=postgres_host, 
            postgres_port=postgres_port, 
            postgres_user=postgres_user,
            postgres_db=postgres_db, 
            access_key_id=access_key_id, 
            secret_access_key=secret_access_key, 
            region=region, 
            bucket_name=bucket_name)
        script_path = project_path / 'do_db_backup.sh'
        script_path.write_text(script)
        script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)
        print(f'{script_path} successfully created. Now you can add it to your cron.')


if __name__ == '__main__':
    do()
