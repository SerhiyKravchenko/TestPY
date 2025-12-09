import os
import subprocess
import shlex

def main():
    print("Введи повний шлях до файлу:")
    input_datafile = input("Шлях до файлу: ").strip()

    if not os.path.isfile(input_datafile):
        print("Файлу не існує! Перевір шлях і спробуй ще раз.")
        return

    input_datafile_dir = os.path.dirname(input_datafile)
    input_datafile = os.path.abspath(input_datafile)


# Create Local Output Directory for generated images
    local_output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(local_output_dir, exist_ok=True)
    print(f"Результати будуть збережені у локальній теці: {local_output_dir}")
    
    # Define internal container paths based on your main.py requirements
    container_data_dir = "/app/data"   # Where the input file will be mounted
    container_frames_dir = "/app/frames" # Where the app writes images (mounted)

# The file path inside the container
    container_input_path = container_data_dir #os.path.join(container_data_dir, os.path.basename(input_datafile)).replace('\\', '/')

    print(f"\nСтворюю Docker image... з файлом {input_datafile}")
    # NOTE: The build command MUST NOT contain --build-arg LOCALFILE now
    build_cmd = 'docker build -t standings .'
    
    try:
        subprocess.run(shlex.split(build_cmd), check=True)
    except subprocess.CalledProcessError as e:
        print("Помилка створення Docker образу.")
        return

    run_cmd = (
        f'docker run --rm ' # --rm removes the container after it exits   --rm
        '--name standings_proc '
        # 1. Mount the local input file directly to the internal container file path.
        # We mount it to the expected /app/data/file.name path.
        f'-v "{input_datafile_dir}":"{container_input_path}":ro '
        
        # 2. Mount the local output directory to the app's hardcoded output directory.
        f'-v "{local_output_dir}":"{container_frames_dir}" '
        
        f'standings'
    )
    
    print("\nЗапускаю Docker контейнер...")
    print(f"Команда: {run_cmd}")

    try:
        # Use shell=True for complex commands with multiple quotes, or ensure proper shlex splitting
        subprocess.run(run_cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Помилка запуску Docker контейнера:")
        print(e)
    
    print(f"\n✅ Завершено. Результати (frames) у теці: {local_output_dir}")

if __name__ == "__main__":
    main()
