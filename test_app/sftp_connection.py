"""SFTP SSH connection

These scripts upload file to the sftp server

There are two different sftp servers connections: one through OpenSSH Key and another through file encryption and
login/password connection


"""
from io import StringIO
import os.path
import paramiko
import threading


def mkdir_p(sftp, remote_directory):
    """Change to this directory, recursively making new folders if needed.
    Returns True if any folders were created."""
    if remote_directory == '/':
        # absolute path so change directory to root
        sftp.chdir('/')
        return
    if remote_directory == '':
        # top-level relative directory must exist
        return
    try:
        sftp.chdir(remote_directory)  # subdirectory exists
    except IOError:
        dirname, basename = os.path.split(remote_directory.rstrip('/'))
        mkdir_p(sftp, dirname)  # make parent directories
        sftp.mkdir(basename)  # subdirectory is missing, so creating it
        sftp.chdir(basename)
        return True


def sftp_simple_upload(host_name, port, username, password, upload_path, filename):
    """
    This function uploads file to SFTP server using the login/password
    :param filename: name of the uploaded file
    :param host_name: str, hostname
    :param port: int, port
    :param username: str
    :param password: str, key password, not user password
    :param upload_path: str, path where upload to at the sftp server
    :return: nothing to return, just upload the file to sftp server
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name,
                   username=username,
                   port=port,
                   password=password,
                   look_for_keys=False
                   )
    sftp = client.open_sftp()
    mkdir_p(sftp, upload_path)
    sftp.put(f'./uploads/test.txt', f'{filename[:-5]}.txt')
    sftp.close()


def sftp_key_upload(host_name, port, username, password, key, upload_path, filename, key_passphrase):
    """
    This function uploads file to SFTP server using the public/private key pair and login/password
    :param key_passphrase:
    :param filename: name of the uploaded file
    :param host_name: str, hostname
    :param port: int, port
    :param username: str
    :param password: str, key password, not user password
    :param key: str, value from your private key
    :param upload_path: str, path where upload to at the sftp server
    :return: nothing to return, just upload the file to sftp server
    """
    # Creating paramiko RSA key instance for connection
    keyfile = StringIO(key.decode('utf-8'))
    dec_key = paramiko.RSAKey.from_private_key(keyfile, key_passphrase)
    # Uploading the file to sftp server and closing the connection
    sftp = multifactor_auth_sftp_client(host=host_name,
                                        port=port,
                                        username=username,
                                        key=dec_key,
                                        password=password)

    mkdir_p(sftp, upload_path)
    sftp.put(f'./uploads/test.txt', f'{filename[:-5]}.txt')
    sftp.close()


def multifactor_auth_sftp_client(host, port, username, key, password):
    # Create an SSH transport configured to the host
    transport = paramiko.Transport((host, port))
    # Negotiate an SSH2 session
    transport.connect()
    # Attempt authenticating using a private key
    transport.auth_publickey(username, key)
    # Create an event for password auth
    password_auth_event = threading.Event()
    # Create password auth handler from transport
    password_auth_handler = paramiko.auth_handler.AuthHandler(transport)
    # Set transport auth_handler to password handler
    transport.auth_handler = password_auth_handler
    # Acquire lock on transport
    transport.lock.acquire()
    # Register the password auth event with handler
    password_auth_handler.auth_event = password_auth_event
    # Set the auth handler method to 'password'
    password_auth_handler.auth_method = 'password'
    # Set auth handler username
    password_auth_handler.username = username
    # Set auth handler password
    password_auth_handler.password = password
    # Create an SSH user auth message
    userauth_message = paramiko.message.Message()
    userauth_message.add_string('ssh-userauth')
    userauth_message.rewind()
    # Make the password auth attempt
    password_auth_handler._parse_service_accept(userauth_message)
    # Release lock on transport
    transport.lock.release()
    # Wait for password auth response
    password_auth_handler.wait_for_response(password_auth_event)
    # Create an open SFTP client channel
    return transport.open_sftp_client()
