from analizador import analizador
from analizador_semantico import SemanticAnalyzer
from generador_cod_intermedio import IntermediateCodeGenerator
from generador_codigo import CodeGenerator

tokens, simbolos, errores_lexicos = analizador("ejemplo.zlang")

semantic_analyzer = SemanticAnalyzer()
semantic_analyzer.analyze(tokens)

intermediate_generator = IntermediateCodeGenerator()
intermediate_generator.generate(tokens)

code_generator = CodeGenerator()
code_generator.generate(intermediate_generator.code)
