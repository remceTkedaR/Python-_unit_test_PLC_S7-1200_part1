# This is a sample Python script.

# Program test for PLC S7 1200 my home.


import pytest
from plc import PLC
import time
import snap7
import snap7.util
from snap7.types import *

# Adres IP sterownika PLC
plc_ip = "192.168.1.121"


# Połącz się ze sterownikiem PLC przed wykonaniem testów
@pytest.fixture(scope="module")
def plc_connection():
    plc = snap7.client.Client()
    plc.connect(plc_ip, 0, 1)

    # Sprawdź, czy połączenie zostało nawiązane poprawnie
    if plc.get_connected():
        yield plc
    else:
        raise ConnectionError("Nie można nawiązać połączenia z PLC.")

    # Zamknij połączenie z PLC
    plc.disconnect()


# Funkcja do odczytu wartości z pamięci PLC
def read_memory(client, byte, bit, data_type):
    result = client.read_area(snap7.types.Areas.MK, 0, byte, data_type)
    if data_type == S7WLBit:
        return snap7.util.get_bool(result, 0, bit)
    elif data_type == S7WLByte or data_type == S7WLWord:
        return snap7.util.get_int(result, 0)
    elif data_type == S7WLReal:
        return snap7.util.get_real(result, 0)
    elif data_type == S7WLDWord:
        return snap7.util.get_dword(result, 0)
    else:
        return None


# Funkcja do zapisu wartości do pamięci PLC
def write_memory(client, byte, bit, data_type, value):
    result = client.read_area(snap7.types.Areas.MK, 0, byte, data_type)
    if data_type == S7WLBit:
        snap7.util.set_bool(result, 0, bit, value)
    elif data_type == S7WLByte or data_type == S7WLWord:
        snap7.util.set_int(result, 0, value)
    elif data_type == S7WLReal:
        snap7.util.set_real(result, 0, value)
    elif data_type == S7WLDWord:
        snap7.util.set_dword(result, 0, value)
    client.write_area(snap7.types.Areas.MK, 0, byte, result)


# Test sterowania wyjściem za pomocą flagi wejściowej
def test_output_control(plc_connection):
    input_byte = 53
    input_bit = 5
    output_byte = 3
    output_bit = 7

    # Ustawienie flagi wejściowej na wartość True
    write_memory(plc_connection, input_byte, input_bit, S7WLBit, True)
    time.sleep(2)
    write_memory(plc_connection, input_byte, input_bit, S7WLBit, False)

    # Pobranie wartości flagi wyjściowej
    output_value = read_memory(plc_connection, output_byte, output_bit, S7WLBit)
    assert output_value == True

    # Ustawienie flagi wejściowej na wartość False
    write_memory(plc_connection, input_byte, input_bit, S7WLBit, True)
    time.sleep(2)
    write_memory(plc_connection, input_byte, input_bit, S7WLBit, False)

    # Pobranie wartości flagi wyjściowej
    output_value = read_memory(plc_connection, output_byte, output_bit, S7WLBit)
    assert output_value == False


# Wykonaj testy
pytest.main(["-v"])
