import zipfile
import os
import subprocess

# 定义 ZIP 文件路径和 IDA 可执行文件路径
zip_path = r"C:\path\to\your\zipfile.zip"  # 将此路径替换为您的 ZIP 文件路径
ida_path = r"C:\path\to\idat64.exe"  # 将此路径替换为您的 IDA 可执行文件路径

# 获取 ZIP 文件名称并定义解压文件夹路径
malware_name = os.path.splitext(os.path.basename(zip_path))[0]
extracted_folder = os.path.join(os.path.dirname(zip_path), malware_name)

# 解压 ZIP 文件
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)
    print(f"{zip_path} 已解压到 {extracted_folder}")

# 定位到解压后的 'exe' 文件夹
exe_folder = os.path.join(extracted_folder, "exe")
if os.path.exists(exe_folder):
    # 创建同级的 'opcode' 文件夹（如果不存在）
    opcode_folder = os.path.join(extracted_folder, "opcode")
    if not os.path.exists(opcode_folder):
        os.makedirs(opcode_folder)
        print(f"创建 opcode 文件夹：{opcode_folder}")

    # 遍历 'exe' 文件夹中的每个病毒文件
    for virus_file in os.listdir(exe_folder):
        virus_path = os.path.join(exe_folder, virus_file)
        
        # 设置输出的操作码文件路径，文件名与病毒文件名相同
        opcode_file = os.path.join(opcode_folder, f"{virus_file}.opcode")
        
        # 调用 IDA 命令行并运行提取脚本
        ida_script_path = r"C:\path\to\extract_opcode.py"  # 将此路径替换为您的提取脚本路径
        command = [
            ida_path,
            "-A",  # 自动模式
            "-S" + ida_script_path + " " + opcode_file,  # 指定脚本并传递输出文件路径
            virus_path  # 目标病毒文件
        ]

        subprocess.run(command)
        print(f"{virus_file} 的操作码已提取并保存至 {opcode_file}")
