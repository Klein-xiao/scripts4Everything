import zipfile
import os
import subprocess

# 定义 ZIP 文件所在的目录和 IDA 可执行文件路径
zip_folder = r"C:\path\to\your\zip_folder"  # 将此路径替换为 ZIP 文件所在的文件夹路径
ida_path = r"C:\Users\admin\Downloads\IDA_Pro_7.7\ida64.exe"  # IDA 可执行文件路径
ida_script_path = r"C:\Users\admin\Downloads\extract_opcode.py"  # 提取操作码的脚本路径

# 在指定目录中查找唯一的 ZIP 文件
zip_files = [f for f in os.listdir(zip_folder) if f.endswith('.zip')]
if len(zip_files) != 1:
    raise Exception("指定目录中应该只有一个 ZIP 文件，请检查文件夹内容。")

# 获取 ZIP 文件路径和名称
zip_path = os.path.join(zip_folder, zip_files[0])
zip_name = os.path.splitext(zip_files[0])[0]

# 设置同级目录路径（解压目录和结果文件将保存在这里）
parent_folder = os.path.dirname(zip_folder)  # ZIP 文件所在目录的同级目录
output_base_folder = os.path.join(parent_folder, zip_name)
if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)
    print(f"创建同级输出目录：{output_base_folder}")

# 解压到同级输出目录的 ZIP 文件名对应文件夹
extracted_folder = os.path.join(output_base_folder, "extracted")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)
    print(f"{zip_path} 已解压到 {extracted_folder}")

# 定位到解压后的 'exe' 文件夹
exe_folder = os.path.join(extracted_folder, "exe")
if os.path.exists(exe_folder):
    # 创建 'opcode' 文件夹来存放操作码文件
    opcode_folder = os.path.join(output_base_folder, "opcode")
    if not os.path.exists(opcode_folder):
        os.makedirs(opcode_folder)
        print(f"创建 opcode 文件夹：{opcode_folder}")

    # 遍历 'exe' 文件夹中的每个病毒文件
    for virus_file in os.listdir(exe_folder):
        virus_path = os.path.join(exe_folder, virus_file)
        
        # 调用 IDA 命令行并运行提取脚本
        command = [
            ida_path,
            "-A",  # 自动模式
            f"-S{ida_script_path}",  # 不再传递额外参数，只指定脚本路径
            virus_path  # 目标病毒文件
        ]

        subprocess.run(command)
        print(f"{virus_file} 的操作码已提取")
