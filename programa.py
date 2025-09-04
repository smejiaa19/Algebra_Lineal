import re  # Importamos modulo de expresiones regulares
import unicodedata

from fractions import Fraction  # Para mantener exactitud con enteros y fracciones


def normalizar_ecuacion(equation: str) -> str:
    """
    Convierte simbolos unicode a ASCII para operacion con Fraction
    ejemplos
    − → -
    × → *
    ÷ → /
    ０１２３ → 0123
    Fullwidth parentheses → ()
    """
    equation = unicodedata.normalize('NFKC', equation)

    replacements = {
        '−': '-',
        '×': '*',
        '÷': '/',  
        '⁺': '+',
        '⁻': '-',
        '∙': '*',
        '⋅': '*',
    }
    equation = re.sub(r'[\u200B\u200C\u200D\u2060]', '', equation)

    for old, new in replacements.items():
        equation = equation.replace(old, new)

    return equation.strip()

def convertir_ecuacion(ecuacion, variables):
    """Aqui se realiza el proceso de convertir la ecuacion de tipo:
    2x + y - z = 8 en: 2 + 1 -1 = 8
    """

    ecuacion = ecuacion.replace(" ", "")  # Buscamos espacios dentro de toda la ecuacion y los sustituimos
    ecuacion = normalizar_ecuacion(ecuacion)
    ecuacion_separada = ecuacion.split("=")  # Para asi separar del termino independiente y las variables
    
    term_independiente = Fraction(ecuacion_separada[1])  # Aqui basicamente tomamos la ecuacion (que es un string) y decimos que la variable
    coeficientes = [Fraction(0)] * len(variables)  # Una lista de caracteres | para los coeficientes de cada variable

    patron = re.compile(r"([+-]?[\d]*)([a-zA-Z]+)")
    """ Compilamos una expresion regular para que sea mas eficiente, en vez de escribir re.findall()etc, 
        Ahora patron se convierte en un objeto que nos permite recorrer coincidencias dentro del texto 
        r'' Significa raw string o basicamente la cadena de caracteres cruda, como nos beneficia esto?
        Simple al usar un raw string nos ahorramos el tener que escribir \\d que significa digito.
        Porque python cuando tenemos un string y escribimos string = \n lo interpreta como un salto de linea 
        Pero cuando escribimos string = r'\n' literalmente va a escribir \n.
    """

    """
        Siguiendo un poco la explicacion dentro de los parentesis lo que hacemos es decir: 
        esta expresion se va a tomar como un raw string lo que nos permite usar \d y no \\d para la libreria re 
            asimismo el primer grupo de captura ([+-]?[\d]*) Indica que vamos primero a buscar signos + o - que solo pueden aparecer 1 vez, nunca juntos
        ahora para \d* decimos que puede ser cualquiero digito entre 0 y 9 y que puede aparecer mas de 1 vez. 
    """

    for num in patron.finditer(ecuacion_separada[0]):
        coeficiente, variable = num.groups()
        if coeficiente == "" or coeficiente == "+":
            coeficiente = Fraction(1)
        elif coeficiente == "-":
            coeficiente = Fraction(-1)
        else:
            coeficiente = Fraction(coeficiente)

        index_var = variables.index(variable)
        coeficientes[index_var] = coeficiente

    return coeficientes + [term_independiente]  # Aqui retornamos la matriz aumentada


def crear_matriz():
    n_incog = int(input("Ingrese el numero de incognitas: "))
    print("Ingrese las incognitas (uso: separar con espacios eg: a b c)")

    variables = input().split()

    matriz = []
    print("Ingrese cada ecuacion")
    for i in range(n_incog):
        print("ecuacion: ",i+1)
        ecuacion = input()
        fila = convertir_ecuacion(ecuacion, variables)
        matriz.append(fila)

    return matriz, variables


def imprimir_matriz_identidad(n_incog):
    for i in range(n_incog):
        fila = []
        for j in range(n_incog):
            if i == j:
                fila.append(1)
            else:
                fila.append(0)
        print(" ".join(map(str, fila)))


def eliminacion_filas(matriz, tolerancia=1e-12):
    n = len(matriz)

    # Eliminacion hacia adelante
    for i in range(n):
        pivote = matriz[i][i]
        if abs(pivote) <= tolerancia:
            for k in range(i + 1, n):
                if abs(matriz[k][i]) > tolerancia:
                    matriz[i], matriz[k] = matriz[k], matriz[i]
                    pivote = matriz[i][i]
                    break
            else:
                raise ValueError("Sistema sin solución única")

        for j in range(i, n + 1):
            matriz[i][j] /= pivote
        
        for k in range(i + 1, n):
            factor = matriz[k][i]
            for j in range(i, n + 1):
                matriz[k][j] -= factor * matriz[i][j]

        print(f"Matriz después del paso {i + 1}:")
        for fila in matriz:
            #print(fila)
            print([f"{f.numerator}/{f.denominator}" if f.denominator != 1 else f"{f.numerator}" for f in fila])

    # Sustitución hacia atrás
    soluciones = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        soluciones[i] = matriz[i][n]
        for j in range(i + 1, n):
            soluciones[i] -= matriz[i][j] * soluciones[j]

    return soluciones


def imprimir_soluciones(soluciones, variables):
    print("Solucion del sistema: ")
    for i, j in zip(variables, soluciones):
        print(f"{i} = {j}")


matriz, variables = crear_matriz()
imprimir_matriz_identidad(len(variables))
soluciones = eliminacion_filas(matriz)
imprimir_soluciones(soluciones, variables)
