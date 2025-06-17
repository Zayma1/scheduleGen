import subprocess
import json
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Gerar horário (Enviar JSON)")
        print("2. Sair")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            carregar_json()
        elif choice == "2":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def carregar_json():
    root.withdraw() 

    print("Selecione o arquivo JSON...")
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])

    if not file_path:
        print("Nenhum arquivo selecionado.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        data_str = json.dumps(data)
        subprocess.run(["python", "src/main/initGen.py", data_str])
    except Exception as e:
        print(f"Erro ao carregar o JSON: {e}")

if __name__ == "__main__":
    menu()
