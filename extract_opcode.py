import idautils
import idaapi
import idc
import sys

# 从命令行获取输出文件路径
output_file = sys.argv[1]  # 使用从命令行传入的参数

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

# 完成提取后退出 IDA
idaapi.qexit(0)
