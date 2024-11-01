#include <idc.idc>

static main() {
    auto output_file;
    auto address;
    auto mnemonic;
    auto operand;
    auto operand_str;
    auto i;

    // 获取当前打开的文件路径并设置输出文件路径
    output_file = get_idb_path();
    output_file = Strleft(output_file, strlen(output_file) - 4) + ".opcode";  // 替换扩展名为 .opcode

    // 打开文件写入操作码
    auto file = fopen(output_file, "w");
    if (file == 0) {
        Message("无法打开文件: %s\n", output_file);
        return;
    }
    
    // 遍历程序中的每条指令
    address = FirstSeg();
    while (address != BADADDR) {
        if (isCode(GetFlags(address))) {
            mnemonic = GetMnem(address);
            operand_str = "";

            // 获取每个操作数
            for (i = 0; i < 3; i++) {  // 假设操作数最多为3个
                operand = GetOpnd(address, i);
                if (operand != "") {
                    operand_str = operand_str + operand + " ";
                }
            }
            
            // 写入文件
            fprintf(file, "%s %s\n", mnemonic, operand_str);
        }
        address = NextHead(address, BADADDR);
    }

    // 关闭文件
    fclose(file);
    Message("操作码已提取并保存至 %s\n", output_file);
    
    // 退出 IDA
    Exit(0);
}
