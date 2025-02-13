
class CodeGenerator:
    def __init__(self):
        self.code = []

    def generate(self, intermediate_code):
        print("\n=== Generando Código de Objeto ===")
        for line in intermediate_code:
            if "=" in line:
                parts = line.split(" = ")
                self.code.append(f"MOV {parts[0]}, {parts[1]}")
        self.print_code()

    def print_code(self):
        for line in self.code:
            print(line)

