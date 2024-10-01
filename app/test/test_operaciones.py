import pytest

def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a, b):
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b

def test_suma():
    assert suma(2, 2) == 4
    assert suma(-1, 1) == 0
    assert suma(3.5, 2.5) == 6.0
    assert suma(0, 0) == 0

def test_resta():
    assert resta(2, 2) == 0
    assert resta(-1, 1) == -2
    assert resta(-1, -1) == 0

def test_multiplicacion():
    assert multiplicacion(2, 2) == 4
    assert multiplicacion(-1, 1) == -1
    assert multiplicacion(-1, -1) == 1

def test_division():
    assert division(3, 3) == 1
    assert division(10, 5) == 2
    assert division(20, 2) == 10

def test_division_por_cero():
    with pytest.raises(ValueError) as excinfo:
        division(10, 0)
    assert str(excinfo.value) == "No se puede dividir por cero"

    with pytest.raises(ValueError) as excinfo:
        division(-5, 0)
    assert str(excinfo.value) == "No se puede dividir por cero"

    # Probamos que la división de 0 entre un número no cero funciona correctamente
    assert division(0, 5) == 0

    


