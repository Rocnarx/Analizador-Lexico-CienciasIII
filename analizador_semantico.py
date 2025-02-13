class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.errors = []
        self.in_function = False

    def analyze(self, tokens):
        print("\n=== Iniciando Análisis Semántico ===")
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token[0] == "KEYWORD" and token[1] == "function":
                self.handle_function_declaration(tokens, i)
                i += 1 
            elif token[0] == "KEYWORD" and token[1] == "int":
                self.handle_variable_declaration(tokens, i)
                i += 2 
            elif token[0] == "IDENTIFICADOR":
                self.check_variable_usage(token)
                if i + 1 < len(tokens) and tokens[i + 1][0] == "OPERADOR":
                    self.check_operation(token, tokens)
            elif token[0] == "KEYWORD" and token[1] == "return":
                pass  # Eliminamos la validación de ';'
            i += 1

        if self.errors:
            print("\n=== Errores Encontrados en el Análisis Semántico ===")
            for error in self.errors:
                print(f"[Error] {error}")
        else:
            print("\n=== Análisis Semántico Completado con Éxito ===")

    def handle_function_declaration(self, tokens, index):
        func_name = tokens[index + 1][1]
        self.symbol_table[func_name] = "function"
        print(f"[Proceso] Función '{func_name}' declarada")

        i = index + 3 
        while tokens[i][0] != "SIMBOLO" or tokens[i][1] != ")":
            if tokens[i][0] == "IDENTIFICADOR":
                param_name = tokens[i][1]
                self.symbol_table[param_name] = "parameter"
                print(f"[Proceso] Parámetro '{param_name}' registrado")
            i += 1

    def handle_variable_declaration(self, tokens, index):
        if index + 1 < len(tokens) and tokens[index + 1][0] == "IDENTIFICADOR":
            var_name = tokens[index + 1][1]
            self.symbol_table[var_name] = "int"
            print(f"[Proceso] Variable '{var_name}' declarada con tipo 'int'")
        else:
            self.errors.append(f"Declaración inválida en la línea {tokens[index][2]}")

    def check_variable_usage(self, token):
        identifier = token[1]
        if identifier in self.symbol_table and self.symbol_table[identifier] == "function":
            return 

        if identifier not in self.symbol_table:
            self.errors.append(f"Uso de variable no declarada: '{identifier}' en la línea {token[2]}")

    def check_operation(self, token, tokens):
        idx = tokens.index(token)
        if idx > 0 and idx + 1 < len(tokens):
            left = tokens[idx - 1]
            right = tokens[idx + 1]

            if right[0] == "IDENTIFICADOR" and self.symbol_table.get(right[1]) == "function":
                return
                   
            if left[0] == "IDENTIFICADOR" and right[0] == "IDENTIFICADOR":
                if self.symbol_table.get(left[1]) != self.symbol_table.get(right[1]):
                    self.errors.append(f"Operación incompatible entre tipos en la línea {token[2]}")
