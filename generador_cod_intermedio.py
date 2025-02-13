class IntermediateCodeGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.code = []

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def generate(self, tokens):
        print("\n=== Generando Código Intermedio ===")
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token[0] == "OPERADOR" and token[1] in {"+", "-", "*", "/"}:
                temp_var = self.new_temp()
                left = tokens[i - 1][1]
                right = tokens[i + 1][1]
                self.code.append(f"{temp_var} = {left} {token[1]} {right}")
                i += 2

            elif token[0] == "KEYWORD" and token[1] == "if":
                condition = f"{tokens[i + 2][1]} {tokens[i + 3][1]} {tokens[i + 4][1]}"
                self.code.append(f"IF {condition} THEN")
                i += 5

            elif token[0] == "KEYWORD" and token[1] == "else":
                self.code.append("ELSE")
                i += 1

            elif token[0] == "KEYWORD" and token[1] == "while":
                condition = f"{tokens[i + 2][1]} {tokens[i + 3][1]} {tokens[i + 4][1]}"
                self.code.append(f"WHILE {condition}")
                i += 5

            elif token[0] == "KEYWORD" and token[1] == "return":
                self.code.append(f"RETURN {tokens[i + 1][1]}")
                i += 2

            elif token[0] == "OPERADOR" and token[1] == "=":
                left = tokens[i - 1][1]
                
                if tokens[i + 1][0] == "IDENTIFICADOR" and tokens[i + 2][1] == "(":
                    func_name = tokens[i + 1][1]
                    params = []
                    j = i + 3
                    while tokens[j][1] != ")":
                        if tokens[j][0] in {"IDENTIFICADOR", "NUMBER"}:
                            params.append(tokens[j][1])
                        j += 1
                    param_str = ", ".join(params)
                    self.code.append(f"{left} = CALL {func_name}({param_str})")
                    i = j + 1 
                
                elif tokens[i + 1][0] == "IDENTIFICADOR" and tokens[i + 2][0] == "OPERADOR" and tokens[i + 2][1] in {"+", "-", "*", "/"}:
                    temp_var = self.new_temp()
                    right_operand = tokens[i + 3][1]
                    self.code.append(f"{temp_var} = {tokens[i + 1][1]} {tokens[i + 2][1]} {right_operand}")
                    self.code.append(f"{left} = {temp_var}")
                    i += 3
                else:
                    
                    right = tokens[i + 1][1]
                    self.code.append(f"{left} = {right}")
                    i += 2
            else:
                i += 1

        self.print_code()

    def print_code(self):
        for line in self.code:
            print(line)
