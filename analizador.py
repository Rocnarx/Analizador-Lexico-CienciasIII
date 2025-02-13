import re


PAL_CLAVE = {"if", "else", "while", "for", "function", "return", "int"}
# Operadores
OPERADOR = {"+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", "&&", "||"}
# Simbolos especiales
SIMBOLO = {"(", ")", "{", "}", "[", "]", ";", ","}
# Comentarios // y /* */
COMENTARIO = re.compile(r'//.*')
COMENTARIOS = re.compile(r'/\*.*?/', re.DOTALL)
# Identificadores
IDENTIFICADOR = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
# Numeros validos y flotantes
NUMERO = re.compile(r'^\d+(\.\d+)?(e[+-]?\d+)?$')

def analizador(file_path):

    #REQUERIMIENTO DE .ZLANG

    if not file_path.endswith(".zlang"):
        print("Error 2.3.1: El archivo debe tener la extensión .zlang")
        return None, None, None
    
    #REQUERIMIENTO DE LINEA A LINEA
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()

        # REQUERIMIENTO DE ELIMINACION DE COMENTARIOS
        code = COMENTARIO.sub("", code)
        code = COMENTARIOS.sub("", code)

        tokens = []
        errores = []
        tabla_simbolos = []

        lineas = code.split("\n")

        #REQUERIMIENTO DE ANALISIS LEXICO
        
        for num_linea, linea in enumerate(lineas, start=1):
            palabras = re.split(r'(\s+|[(){}\[\];,])', linea)
            
            for palabra in palabras:
                if palabra.strip() == "":
                    continue
                elif palabra in PAL_CLAVE:
                    tokens.append(("KEYWORD", palabra, num_linea))
                elif palabra in OPERADOR:
                    tokens.append(("OPERADOR", palabra, num_linea))
                elif palabra in SIMBOLO:
                    tokens.append(("SIMBOLO", palabra, num_linea))
                elif IDENTIFICADOR.match(palabra):
                    tokens.append(("IDENTIFICADOR", palabra, num_linea))
                    
                    
                    tabla_simbolos.append({"nombre": palabra, "tipo": "IDENTIFIER", "linea": num_linea})

                elif NUMERO.match(palabra):
                    tokens.append(("NUMBER", palabra, num_linea))
                elif re.match(r'^\d+[a-zA-Z_]+$', palabra):
                    errores.append((num_linea, f"Error 2.3.4.a: Identificador inválido '{palabra}' (comienza con un número)"))
                elif re.search(r'\d+\.\d+\.', palabra):
                    errores.append((num_linea, f"Error 2.3.4.b: Número mal formado '{palabra}'"))
                elif re.match(r'^[^a-zA-Z0-9\s]+$', palabra) and palabra not in OPERADOR and palabra not in SIMBOLO:
                    errores.append((num_linea, f"Error 2.3.4.c: Operador desconocido '{palabra}'"))
                else:
                    errores.append((num_linea, f"Error: Token no reconocido '{palabra}'"))

        return tokens, tabla_simbolos, errores

    except FileNotFoundError:
        print("No se encontró el archivo.")
    except Exception as e:
        print(f"Error inesperado: {e}")

tokens, simbolos, errores = analizador("ejemplo.zlang")


print("\nTabla de Tokens:")
for token in tokens:
    print(token)

#REQUERIMIENTO DE TABLA DE SIMBOLOS
print("\nTabla de Simbolos:")
for datos in simbolos:
    print(f"Nombre: {datos['nombre']}, Tipo: {datos['tipo']}, Linea: {datos['linea']}")

print("\nErrores detectados:")
for error in errores:
    print(f"Linea {error[0]}: {error[1]}")

    
