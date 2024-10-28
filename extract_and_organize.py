import os
import zipfile
from shutil import move
import sys


def extract_and_organize_zips_in_each_folder(root_dir, password='infected'):
    # 遍历根目录下的每个文件夹
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)

        # 确保只处理文件夹
        if os.path.isdir(folder_path):
            exe_dir = os.path.join(folder_path, 'exe')
            sample_zip_dir = os.path.join(folder_path, 'sampleZip')

            # 在每个子文件夹中创建 exe 和 sampleZip 文件夹（如果不存在）
            os.makedirs(exe_dir, exist_ok=True)
            os.makedirs(sample_zip_dir, exist_ok=True)

            # 遍历子文件夹内的文件
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.zip'):
                    zip_path = os.path.join(folder_path, file_name)
                    try:
                        # 解压到当前文件夹的 exe 目录
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            zip_ref.extractall(exe_dir, pwd=password.encode())
                        print(f"Extracted {file_name} to {exe_dir} in {folder_name}")
                    except Exception as e:
                        print(f"Failed to extract {file_name} in {folder_name}: {e}")

                    # 移动 zip 文件到当前文件夹的 sampleZip 文件夹
                    move(zip_path, os.path.join(sample_zip_dir, file_name))
                    print(f"Moved {file_name} to {sample_zip_dir} in {folder_name}")


# 从命令行获取路径参数
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_root_directory>")
    else:
        root_directory = sys.argv[1]
        if os.path.isdir(root_directory):
            extract_and_organize_zips_in_each_folder(root_directory)
        else:
            print(f"Error: {root_directory} is not a valid directory.")
