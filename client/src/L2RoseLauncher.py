#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L2RoseGuard - Launcher del Cliente
Inicia el juego con protección integrada
"""

import os
import sys
import subprocess
import ctypes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

class L2RoseLauncher:
    def __init__(self):
        self.key = hashlib.sha256(b"MiClaveSecreta2024").digest()
        self.game_exe = "l2.exe"
        self.ini_enc = "l2.ini.enc"
        self.ini_dec = "l2.ini"
        
    def decrypt_ini(self):
        """Desencripta l2.ini.enc a l2.ini temporal"""
        try:
            if not os.path.exists(self.ini_enc):
                print("[L2RoseGuard] ERROR: No se encontró l2.ini.enc")
                return False
                
            with open(self.ini_enc, 'rb') as f:
                data = f.read()
            
            iv = data[:16]
            encrypted = data[16:]
            
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(encrypted), 16)
            
            with open(self.ini_dec, 'wb') as f:
                f.write(decrypted)
                
            print("[L2RoseGuard] l2.ini desencriptado correctamente")
            return True
            
        except Exception as e:
            print(f"[L2RoseGuard] ERROR al desencriptar: {e}")
            return False
    
    def launch_game(self):
        """Inicia el juego"""
        try:
            print("[L2RoseGuard] Iniciando Lineage 2...")
            
            # Iniciar el juego
            process = subprocess.Popen([self.game_exe], 
                                     cwd=os.getcwd(),
                                     creationflags=subprocess.CREATE_NEW_CONSOLE)
            
            print(f"[L2RoseGuard] Juego iniciado (PID: {process.pid})")
            
            # Esperar a que termine
            process.wait()
            
            # Limpiar archivo desencriptado
            if os.path.exists(self.ini_dec):
                os.remove(self.ini_dec)
                print("[L2RoseGuard] Archivo temporal eliminado")
                
        except Exception as e:
            print(f"[L2RoseGuard] ERROR al iniciar: {e}")
    
    def run(self):
        """Ejecutar launcher"""
        print("=" * 50)
        print("L2RoseGuard - Sistema de Protección")
        print("=" * 50)
        
        if self.decrypt_ini():
            self.launch_game()
        else:
            input("Presiona Enter para salir...")

if __name__ == "__main__":
    launcher = L2RoseLauncher()
    launcher.run()
