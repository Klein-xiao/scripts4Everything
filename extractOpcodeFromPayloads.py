import zipfile
import os
import subprocess

# 定义病毒文件夹的路径
input_folder = r"C:\Users\YourUsername\Downloads\payloads"  # 使用原始字符串 r""，避免转义问题
ida_path = r"C:\Users\YourUsername\Downloads\idat64.exe"  # IDA 可执行文件路径（64位或32位）

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

            # 定位到解压后的 'exe' 文件夹
            exe_folder = os.path.join(extracted_folder, "exe")
            if os.path.exists(exe_folder):
                # 创建同级的 'opcode' 文件夹（如果不存在）
                opcode_folder = os.path.join(extracted_folder, "opcode")
                if not os.path.exists(opcode_folder):
                    os.makedirs(opcode_folder)
                    print(f"创建 opcode 文件夹：{opcode_folder}")

                # 遍历 'exe' 文件夹中的每个文件
                for virus_file in os.listdir(exe_folder):
                    virus_path = os.path.join(exe_folder, virus_file)
                    
                    # 设置输出的操作码文件路径，文件名与病毒文件名相同
                    opcode_file = os.path.join(opcode_folder, f"{virus_file}.opcode")
                    
                    # 调用IDA命令行并运行提取脚本
                    ida_script_path = r"C:\Users\YourUsername\Downloads\extract_opcode.py"  # 提取脚本路径
                    command = [
                        ida_path,
                        "-A",  # 自动模式
                        "-S" + ida_script_path + " " + opcode_file,  # 指定脚本并传递输出文件路径
                        virus_path  # 目标病毒文件
                    ]

                    subprocess.run(command)
                    print(f"{virus_file} 的操作码已提取并保存至 {opcode_file}")
