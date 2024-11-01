import zipfile
import os
import subprocess
import tempfile

# 全局路径配置
ZIP_FOLDER = r"C:\path\to\your\zip_folder"  # ZIP 文件所在文件夹路径
GHIDRA_PATH = r"C:\path\to\ghidra_10.1.5_PUBLIC\ghidraRun.bat"  # Ghidra 可执行文件路径
GHIDRA_PROJECT_PATH = r"C:\path\to\your\ghidra_project"  # Ghidra 项目存储位置

# 提取操作码的 Ghidra 脚本模板
GHIDRA_SCRIPT_TEMPLATE = """
from ghidra.program.model.listing import Instruction
from ghidra.app.script import GhidraScript
import os

class ExtractOpcodes(GhidraScript):
    def run(self):
        program = self.getCurrentProgram()
        program_name = program.getName()
        output_folder = "{output_folder}"
        output_file_path = os.path.join(output_folder, "{}.opcode".format(program_name))

        with open(output_file_path, "w") as f:
            listing = program.getListing()
            instructions = listing.getInstructions(True)
            for instr in instructions:
                mnemonic = instr.getMnemonicString()
                operands = [instr.getDefaultOperandRepresentation(i) for i in range(instr.getNumOperands())]
                f.write("{} {}\n".format(mnemonic, " ".join(operands)))
        print("操作码已提取并保存至: {}".format(output_file_path))
"""

def extract_zip(zip_path, output_base_folder):
    """解压 ZIP 文件到指定文件夹"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        extracted_folder = os.path.join(output_base_folder, "extracted")
        zip_ref.extractall(extracted_folder)
        print(f"{zip_path} 已解压到 {extracted_folder}")
    return extracted_folder

def create_opcode_folder(base_folder):
    """创建 opcode 文件夹以存放提取的操作码文件"""
    opcode_folder = os.path.join(base_folder, "opcode")
    if not os.path.exists(opcode_folder):
        os.makedirs(opcode_folder)
        print(f"创建 opcode 文件夹：{opcode_folder}")
    return opcode_folder

def create_ghidra_script(output_folder):
    """创建临时 Ghidra 脚本文件用于提取操作码"""
    ghidra_script_content = GHIDRA_SCRIPT_TEMPLATE.format(output_folder=output_folder)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as script_file:
        script_file.write(ghidra_script_content.encode())
        print(f"Ghidra 脚本文件已创建：{script_file.name}")
        return script_file.name

def run_ghidra(ghidra_script_path, virus_path):
    """调用 Ghidra 命令行运行提取操作码的脚本"""
    command = [
        GHIDRA_PATH,
        GHIDRA_PROJECT_PATH,
        "-import", virus_path,
        "-scriptPath", os.path.dirname(ghidra_script_path),
        "-postScript", os.path.basename(ghidra_script_path)
    ]
    subprocess.run(command, shell=True)
    print(f"{virus_path} 的操作码已提取")

def main():
    # 查找唯一的 ZIP 文件
    zip_files = [f for f in os.listdir(ZIP_FOLDER) if f.endswith('.zip')]
    if len(zip_files) != 1:
        raise Exception("指定目录中应该只有一个 ZIP 文件，请检查文件夹内容。")
    
    zip_path = os.path.join(ZIP_FOLDER, zip_files[0])
    zip_name = os.path.splitext(zip_files[0])[0]
    parent_folder = os.path.dirname(ZIP_FOLDER)
    output_base_folder = os.path.join(parent_folder, zip_name)
    
    if not os.path.exists(output_base_folder):
        os.makedirs(output_base_folder)
        print(f"创建同级输出目录：{output_base_folder}")

    # 解压 ZIP 文件并创建提取操作码的目标文件夹
    extracted_folder = extract_zip(zip_path, output_base_folder)
    exe_folder = os.path.join(extracted_folder, "exe")
    opcode_folder = create_opcode_folder(output_base_folder)

    # 创建临时 Ghidra 脚本文件
    ghidra_script_path = create_ghidra_script(opcode_folder)

    # 遍历 exe 文件夹并对每个文件运行 Ghidra 提取操作码
    if os.path.exists(exe_folder):
        for virus_file in os.listdir(exe_folder):
            virus_path = os.path.join(exe_folder, virus_file)
            run_ghidra(ghidra_script_path, virus_path)

    # 删除临时 Ghidra 脚本文件
    os.remove(ghidra_script_path)
    print("临时 Ghidra 脚本文件已删除")

# 执行主函数
if __name__ == "__main__":
    main()
