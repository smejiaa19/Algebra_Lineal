import re  # Importamos modulo de expresiones regulares


def convertir_ecuacion(ecuacion, variables):
    """Aqui se realiza el proceso de convertir la ecuacion de tipo:
    2x + y - z = 8 en: 2 + 1 -1 = 8
    """

    ecuacion = ecuacion.replace(
        " ", ""
    )  # Buscamos espacios dentro de toda la ecuacion y los sustituimos
    ecuacion_separada = ecuacion.split(
        "="
    )  # Para asi separar del termino independiente y las variables

    term_independiente = int(
        ecuacion_separada[1]
    )  # Aqui basicamente tomamos la ecuacion (que es un string) y decimos que la variable
    coeficientes_var = [0] * len(
        variables
    )  # Una lista de caracteres | para los coeficientes de cada variable

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
            coeficiente = 1
        elif coeficiente == "-":
            coeficiente = -1
