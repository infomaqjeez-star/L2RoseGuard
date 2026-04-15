#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L2RoseGuard Launcher Profesional
Version ejecutable sin ventana de consola
"""

import os
import sys
import subprocess
import tempfile
import shutil
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
import ctypes

# Ocultar consola
if sys.platform == 'win32':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

class L2LauncherPro:
    def __init__(self):
        self.key = hashlib.sha256(b"MiClaveSecreta2024").digest()
        self.game_exe = "l2.exe"
        self.ini_enc = "l2.ini.enc"
        self.temp_dir = None
        
    def decrypt_to_memory(self):
        """Desencripta l2.ini.enc y guarda en archivo temporal oculto"""
        try:
            if not os.path.exists(self.ini_enc):
                self.show_error("No se encontró l2.ini.enc")
                return None
                
            with open(self.ini_enc, 'rb') as f:
                data = f.read()
            
            iv = data[:16]
            encrypted = data[16:]
            
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(encrypted), 16)
            
            # Crear archivo temporal en carpeta oculta
            self.temp_dir = tempfile.mkdtemp(prefix='.')
            temp_path = os.path.join(self.temp_dir, 'l2.ini')
            
            with open(temp_path, 'wb') as f:
                f.write(decrypted)
                
            # Ocultar archivo
            ctypes.windll.kernel32.SetFileAttributesW(temp_path, 0x02)
            
            return temp_path
            
        except Exception as e:
            self.show_error(f"Error de desencriptación: {e}")
            return None
    
    def show_error(self, message):
        """Mostrar error en ventana"""
        ctypes.windll.user32.MessageBoxW(0, message, "L2RoseGuard Error", 0x10)
    
    def launch_game(self, ini_path):
        """Inicia el juego con el l2.ini temporal"""
        try:
            # Copiar l2.ini temporal a la carpeta del juego
            shutil.copy(ini_path, 'l2.ini')
            
            # Iniciar juego
            process = subprocess.Popen(
                [self.game_exe],
                cwd=os.getcwd(),
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
            # Esperar un momento y eliminar l2.ini desencriptado
            import time
            time.sleep(2)
            
            if os.path.exists('l2.ini'):
                os.remove('l2.ini')
            
            # Esperar a que termine el juego
            process.wait()
            
        except Exception as e:
            self.show_error(f"Error al iniciar: {e}")
        finally:
            # Limpiar archivos temporales
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def run(self):
        """Ejecutar launcher"""
        ini_path = self.decrypt_to_memory()
        if ini_path:
            self.launch_game(ini_path)

if __name__ == "__main__":
    launcher = L2LauncherPro()
    launcher.run()
