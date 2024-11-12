from openpyxl import Workbook
import os
import re

# 定义 .opcode 文件所在的文件夹路径
folder_path = '/Users/haihai/Desktop/cybersecurity/MCTI/sub3/APT1'  # 替换为实际的文件夹路径
output_xlsx = os.path.join(os.path.dirname(folder_path), 'opcode_data.xlsx')

# 定义 APT 组织和 MITRE-ID 的映射关系
apt_mitre_map = {
    "APT1": "0006",
    "APT12": "0005",
    "APT16": "0023",
    "APT17": "0025",
    "APT19": "0073",
    "APT3": "0022",
    "APT30": "0013",
    "APT41": "0096",
    "Axiom": "0001",
    "BRONZE BUTLER": "0060",
    "Chimera": "0114",
    "Deep Panda": "0009",
    "Elderwood": "0066",
    "GALLIUM": "0093",
    "HAFNIUM": "0125",
    "Ke3chang": "0004",
    "menuPass": "0045",
    "Moafee": "0002",
    "APT28": "0007",
    "APT29": "0016",
    "Dragonfly 2.0": "0074",
    "FIN5": "0053",
    "Sandworm Team": "0034",
    "TEMP.Veles": "0088",
    "Turla": "0010",
    "Cobalt Group": "0080",
    "Dragonfly": "0035",
    "FIN7": "0046",
    "Gamaredon Group": "0047",
    "Blue Mockingbird": "0108",
    "Bouncing Golf": "0097",
    "DarkVishnya": "0105",
    "Evilnum": "0120",
    "Gallmaker": "0084",
    "Patchwork": "0040",
    "Sidewinder": "0121",
    "Ajax Security Team": "0130",
    "APT33": "0064",
    "APT39": "0087"
}

# 创建 Excel 工作簿
wb = Workbook()
ws = wb.active
ws.append(["Opcodes", "MITRE-ID"])  # 添加表头

# 遍历文件夹中的每个文件
for filename in os.listdir(folder_path):
    if filename.endswith(".opcode"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            # 读取并格式化 opcode 内容：删除换行符、转为大写、用逗号分隔
            opcodes = ', '.join(line.strip().upper() for line in file if line.strip())

            # 获取上级文件夹的名称
            parent_folder_name = os.path.basename(os.path.dirname(file_path))

            # 提取 MITRE-ID 的数字部分
            mitre_id = apt_mitre_map.get(parent_folder_name, None)
            if mitre_id:
                ws.append([opcodes, mitre_id])  # 添加一行数据

# 保存为 Excel 文件
wb.save(output_xlsx)
print(f"Data has been saved to {output_xlsx}")
