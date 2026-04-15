#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L2RoseGuard - Encriptador de l2.ini
Encripta el archivo de configuración del cliente Lineage 2
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import os
import sys

class L2Encrypter:
    def __init__(self, key):
        """Inicializa el encriptador con una clave"""
        # Generar clave AES de 256 bits a partir de la clave proporcionada
        self.key = hashlib.sha256(key.encode()).digest()
        self.block_size = AES.block_size
    
    def encrypt_file(self, input_file, output_file):
        """Encripta un archivo"""
        try:
            # Leer archivo
            with open(input_file, 'rb') as f:
                data = f.read()
            
            # Generar IV aleatorio
            iv = os.urandom(self.block_size)
            
            # Crear cipher y encriptar
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            encrypted_data = cipher.encrypt(pad(data, self.block_size))
            
            # Guardar: IV + datos encriptados
            with open(output_file, 'wb') as f:
                f.write(iv + encrypted_data)
            
            print(f"✓ Archivo encriptado: {input_file} -> {output_file}")
            return True
            
        except Exception as e:
            print(f"✗ Error al encriptar: {e}")
            return False
    
    def decrypt_file(self, input_file, output_file):
        """Desencripta un archivo"""
        try:
            # Leer archivo encriptado
            with open(input_file, 'rb') as f:
                data = f.read()
            
            # Extraer IV y datos encriptados
            iv = data[:self.block_size]
            encrypted_data = data[self.block_size:]
            
            # Crear cipher y desencriptar
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(encrypted_data), self.block_size)
            
            # Guardar archivo desencriptado
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
            
            print(f"✓ Archivo desencriptado: {input_file} -> {output_file}")
            return True
            
        except Exception as e:
            print(f"✗ Error al desencriptar: {e}")
            return False

def main():
    if len(sys.argv) < 4:
        print("Uso: python l2encrypter.py <encrypt|decrypt> <archivo_entrada> <archivo_salida> <clave>")
        print("Ejemplo: python l2encrypter.py encrypt l2.ini l2.ini.enc mi_clave_secreta")
        sys.exit(1)
    
    action = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    key = sys.argv[4] if len(sys.argv) > 4 else "L2RoseGuard_Default_Key_2024!"
    
    encrypter = L2Encrypter(key)
    
    if action == "encrypt":
        encrypter.encrypt_file(input_file, output_file)
    elif action == "decrypt":
        encrypter.decrypt_file(input_file, output_file)
    else:
        print("Acción no válida. Use 'encrypt' o 'decrypt'")

if __name__ == "__main__":
    main()
