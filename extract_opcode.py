import os
import idautils
import idaapi
import idc

# 获取从命令行传递的输出文件路径
output_file = idc.ARGV[1]  # IDA 启动时将文件路径作为参数传递

# 打开文件写入操作码
with open(output_file, "w") as f:
    # 遍历程序中的每条指令
    for address in idautils.Heads():
        if idc.isCode(idc.GetFlags(address)):
            mnemonic = idc.GetMnem(address)
            operands = []
            for i in range(3):  # 假设操作数最多为3个
                operand = idc.GetOpnd(address, i)
                if operand:
                    operands.append(operand)
            operands_str = " ".join(operands)
            f.write(f"{mnemonic} {operands_str}\n")

print(f"操作码已提取并保存至 {output_file}")
idaapi.qexit(0)  # 自动退出 IDA
