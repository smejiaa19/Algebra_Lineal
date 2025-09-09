import re
import unicodedata
from fractions import Fraction


def normalizar_ecuacion(equation: str) -> str:
    # Normaliza los caracteres de acuerdo a la normalizacion NFKC de unicode
    equation = unicodedata.normalize('NFKC', equation)

    # Caracteres especiales a normalizar
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
        # se reemplazan caracteres especiales (si los hay) por caracteres normalizados
        equation = equation.replace(old, new)

    return equation.strip()


def convertir_ecuacion(ecuacion, variables):
    ecuacion = ecuacion.replace(" ", "")  #
    ecuacion = normalizar_ecuacion(ecuacion)
    ecuacion_separada = ecuacion.split("=")  # Para asi separar del termino independiente y las variables

    if len(ecuacion_separada) != 2:
        raise ValueError("La ecuacion debe contener un único signo '='.")

    term_independiente = Fraction(ecuacion_separada[1])
    coeficientes = [Fraction(0)] * len(variables)

    patron = re.compile(r"([+-]?[\d]*)([a-zA-Z]+)")

    # se itera por cada termino que corresponda con el patron el cual es: coeficiente + variable
    for num in patron.finditer(ecuacion_separada[0]):
        coeficiente, variable = num.groups()
        if coeficiente == "" or coeficiente == "+":
            coeficiente = Fraction(1)
        elif coeficiente == "-":
            coeficiente = Fraction(-1)
        else:
            coeficiente = Fraction(coeficiente)

        if variable not in variables:
            raise ValueError(f"La variable '{variable}' no fue declarada en la lista de variables.")

        index_var = variables.index(variable)
        coeficientes[index_var] = coeficiente

    return coeficientes + [term_independiente]  # se devuelve la fila de coeficientes con el termino independiente


def crear_matriz():
    while True:
        try:
            n_incog = int(input("Ingrese el numero de incognitas: "))
            if n_incog <= 0:
                print("El numero de incógnitas debe ser mayor a cero.")
                continue
            break
        except ValueError:
            print("Debe ingresar un número entero.")

    while True:
        variables = input("Ingrese las incognitas (separadas por espacios, ej: x y z): ").split()
        if len(variables) != n_incog:
            print(f"Debe ingresar exactamente {n_incog} variables")
            continue
        if len(set(variables)) != n_incog:
            print("Las variables no deben repetirse.")
            continue
        break

    matriz = []
    print("Ingrese cada ecuacion")
    for i in range(n_incog):
        while True:
            ecuacion = input(f"Ecuacion {i+1}: ")
            if not ecuacion.strip():
                print("La ecuacion no puede estar vacia.")
                continue
            try:
                fila = convertir_ecuacion(ecuacion, variables)
                matriz.append(fila)
                break
            except Exception as e:
                print(f"Error en la ecuacion: {e}")
    return matriz, variables


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
                raise ValueError("Sistema sin solucion unica")

        for j in range(i, n + 1):
            matriz[i][j] /= pivote

        print(f"\nOperacion: F{i+1} -> 1/{pivote} * F{i+1}")
        for fila in matriz:
            print(" | ".join(f"{f.numerator}/{f.denominator}" if f.denominator != 1 else f"{f.numerator}" for f in fila))

        for k in range(i + 1, n):
            factor = matriz[k][i]
            for j in range(i, n + 1):
                matriz[k][j] -= factor * matriz[i][j]

            if abs(factor) > tolerancia:
                print(f"\nOperacion: F{k+1} -> F{k+1} - ({factor}) * F{i+1}")
                for fila in matriz:
                    print(" | ".join(f"{f.numerator}/{f.denominator}" if f.denominator != 1 else f"{f.numerator}" for f in fila))

    # Sustitución hacia atras
    soluciones = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        soluciones[i] = matriz[i][n]  # termino independiente
        operaciones = []
        for j in range(i + 1, n):
            operaciones.append(f"{matriz[i][j]}*{soluciones[j]}")
            soluciones[i] -= matriz[i][j] * soluciones[j]

        # impresion de los pasos de sustitucion al tener la matriz triangular
        if operaciones:
            print(f"\nSustitucion para variable {i+1}: {matriz[i][n]} - ({' + '.join(operaciones)}) = {soluciones[i]}")
        else:
            print(f"\nSustitucion para variable {i+1}: {soluciones[i]} (sin otras variables)")

    return soluciones


def imprimir_soluciones(soluciones, variables):
    print("\nSolucion del sistema:")
    for i, j in zip(variables, soluciones):
        print(f"{i} = {j}")


if __name__ == "__main__":
    matriz, variables = crear_matriz()
    soluciones = eliminacion_filas(matriz)
    imprimir_soluciones(soluciones, variables)
