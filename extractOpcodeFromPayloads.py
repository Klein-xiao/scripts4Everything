import zipfile
import os
import subprocess

# 定义文件路径
input_folder = os.path.expanduser("~/Downloads/payloads")  # 病毒文件夹路径
output_folder = os.path.expanduser("~/Downloads/opcode_output")  # 操作码文件保存路径
ida_path = os.path.expanduser("~/Downloads/idat64")  # IDA 可执行文件路径（64位或32位）

# 创建输出文件夹（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历每个病毒文件夹
for folder_name in os.listdir(input_folder):
    folder_path = os.path.join(input_folder, folder_name)
    if os.path.isdir(folder_path):
        # 查找ZIP文件
        zip_files = [f for f in os.listdir(folder_path) if f.endswith('.zip')]
        for zip_file in zip_files:
            zip_path = os.path.join(folder_path, zip_file)
            malware_name = os.path.splitext(zip_file)[0]
            extracted_folder = os.path.join(folder_path, malware_name)
            
            # 解压ZIP文件
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_folder)
                print(f"{zip_file} 已解压到 {extracted_folder}")

            # 进入解压后的 'exe' 子文件夹
            exe_folder = os.path.join(extracted_folder, "exe")
            if os.path.exists(exe_folder):
                # 遍历 exe 文件夹中的每个 .exe 文件
                exe_files = [f for f in os.listdir(exe_folder) if f.endswith('.exe')]
                for exe_file in exe_files:
                    exe_path = os.path.join(exe_folder, exe_file)
                    
                    # 设置输出的操作码文件路径
                    opcode_file = os.path.join(output_folder, f"{malware_name}_{exe_file}.opcode")
                    
                    # 调用IDA命令行并运行提取脚本
                    ida_script_path = os.path.expanduser("~/Downloads/extract_opcode.py")  # 提取脚本路径
                    command = [
                        ida_path,
                        "-A",  # 自动模式
                        "-S" + ida_script_path + " " + opcode_file,  # 指定脚本并传递输出文件路径
                        exe_path  # 目标EXE文件
                    ]

                    subprocess.run(command)
                    print(f"{exe_file} 的操作码已提取至 {opcode_file}")
