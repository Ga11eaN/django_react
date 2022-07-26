import pgpy
import pandas as pd
import io
import os


def decrypt_file(path_to_key, path_to_file, passphrase, file_name):
    key, _ = pgpy.PGPKey.from_blob(path_to_key)
    encrypted_message = pgpy.PGPMessage.from_blob(path_to_file)

    with key.unlock(passphrase):
        decrypted_message = key.decrypt(encrypted_message)
        str_decrypted_message = decrypted_message.message.decode('utf-8')

    upload_path = '.\\uploads\\'
    for file_name in os.listdir(upload_path):
        file_in_folder = upload_path + file_name
        os.remove(file_in_folder)

    read_str = pd.read_csv(io.StringIO(str_decrypted_message), sep=",")
    read_str.to_csv(f".\\uploads\\{file_name}", index=None)
    file = open(f".\\uploads\\{file_name}", 'rb')
    return file


# decrypt_file(path_to_key=r"D:\Users\yaroslav.maniukh\Desktop\0xA0CADA93-sec.asc",
#              path_to_file=r"D:\Users\yaroslav.maniukh\Desktop\ELIG_FRAMPTONCONSTRUCTION_20210611_Sample.CSV.gpg",
#              passphrase='Tardis594!')
