# Ghidra Script: extract_opcode.py
from ghidra.program.model.listing import Instruction
from ghidra.app.script import GhidraScript
import os

class ExtractOpcodes(GhidraScript):
    def run(self):
        program = self.getCurrentProgram()
        program_name = program.getName()
        
        # 输出文件夹，您可以将其设置为所需的路径
        output_folder = self.askDirectory("选择输出文件夹", "选择保存操作码的目录").getAbsolutePath()
        output_file_path = os.path.join(output_folder, "{}.opcode".format(program_name))

        with open(output_file_path, "w") as f:
            listing = program.getListing()
            instructions = listing.getInstructions(True)
            for instr in instructions:
                mnemonic = instr.getMnemonicString()
                operands = [instr.getDefaultOperandRepresentation(i) for i in range(instr.getNumOperands())]
                f.write("{} {}\n".format(mnemonic, " ".join(operands)))
        
        print("操作码已提取并保存至: {}".format(output_file_path))
