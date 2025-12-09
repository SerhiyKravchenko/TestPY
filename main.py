'''
Organise and orchestrate the program
'''
import subprocess
import os
import shutil

from pathlib import Path

def main():
    '''
    Docstring for main
    '''
    input_dir = Path("/data")

    file = [f for f in input_dir.iterdir() if f.is_file()]
    path_to_script = "implementation/visual.py"

    # Передаємо шлях до visual.py як аргумент
    command = ["python", path_to_script, file]

    try:
        subprocess.run(command, check=True)
        print("Візуалізація успішно завершена.")
    except subprocess.CalledProcessError as e:
        print(f"Помилка при запуску візуалізації: {e}")

if __name__ == "__main__":
    main()