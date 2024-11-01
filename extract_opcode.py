import idautils
import idaapi
import idc
import os

# 获取当前打开的 IDA 数据库文件路径和名称
input_filepath = idaapi.get_input_file_path()
input_filename = idaapi.get_root_filename()
output_folder = os.path.dirname(input_filepath)
output_file = os.path.join(output_folder, f"{input_filename}.opcode")

# 打开文件写入操作码
with open(output_file, "w") as f:
    # 遍历程序中的每条指令
    for address in idautils.Heads():
        if idc.isCode(idc.GetFlags(address)):
            mnemonic = idc.print_insn_mnem(address)
            operands = []
            for i in range(3):  # 假设操作数最多为3个
                operand = idc.print_operand(address, i)
                if operand:
                    operands.append(operand)
            operands_str = " ".join(operands)
            f.write("{} {}\n".format(mnemonic, operands_str))  # 使用 format() 方法替代 f""

print(f"操作码已提取并保存至 {output_file}")
idaapi.qexit(0)  # 自动退出 IDA
