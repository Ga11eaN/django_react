import paramiko
import stat


def connect(host_name, port, username, password, dir=''):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name,
                   username=username,
                   port=port,
                   password=password,
                   look_for_keys=False
                   )
    sftp = client.open_sftp()
    if dir == '..':
        sftp.chdir('..')
    else:
        sftp.chdir(dir)
    list_of_objects = []
    for obj in sftp.listdir_iter():
        if stat.S_ISDIR(obj.st_mode):
            list_of_objects.append({'name': obj.filename, 'obj_type': 'dir'})
        else:
            list_of_objects.append({'name': obj.filename, 'obj_type': 'file'})
    sftp.close()
    return list_of_objects


def download_file(host_name, port, username, password, path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name,
                   username=username,
                   port=port,
                   password=password,
                   look_for_keys=False
                   )
    sftp = client.open_sftp()
    file = sftp.open(path, 'rb').read()
    sftp.close()
    return file


# result = download_file(host_name='198.19.243.251',
#                  port=2222,
#                  username='tester',
#                  password='password',
#                  path="inbox\ELIG_FRAMPTONCONSTRUCTION_20210611_Sample.CSV.gpg")
#
# print(result.read())