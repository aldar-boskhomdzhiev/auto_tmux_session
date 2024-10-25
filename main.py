import argparse
import libtmux
import os
import random
import string

def start(num_envs, base_dir='./'):
    
    server = libtmux.Server()

    # Создание сессии tmux
    session = server.new_session(session_name="jupyter_envs", kill_session=True, attach=False)
    print(f"Создана сессия tmux с именем: {session}")

    base_port = 8888 
    for i in range(num_envs):
        env_dir = os.path.join(base_dir, f"dir{i}")
        venv_dir = os.path.join(env_dir,"venv")

        # Создание директории для окружения
        if not os.path.exists(env_dir):
            os.makedirs(env_dir)

        if not os.path.exists(venv_dir):
            os.system(f'python3 -m venv {venv_dir}')
            print(f"Создано виртуальное окружение в {venv_dir}")

        # Генерация случайного токена для Jupyter
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        port = base_port + i  # Определение порта

        # Создание окна в tmux
        window = session.new_window(window_name=f"env{i}", attach=False)

        # Команда для запуска Jupyter
        cmd = (f"source {venv_dir}/bin/activate && "
               f"jupyter notebook --ip 0.0.0.0 --port {port} --no-browser "
               f"--NotebookApp.token='{token}' --NotebookApp.notebook_dir='{env_dir}'")
               
        # Отправка команды в tmux окно
        window.attached_pane.send_keys(cmd)
        
        print(f"Создано окружение {i} на порту {port} с токеном {token} в директории {env_dir}")

    # Подключение к сессии
    session.attach_session()

def stop(env_id):
    server = libtmux.Server()
    session = server.find_where({"session_name": "jupyter_envs"})

    if session:
        window = session.find_where({"window_name": f"env{env_id}"})
        if window:
            print(f"Останавливаем окружение с ID {env_id}")
            window.kill_window()
        else:
            print(f"Окно с ID {env_id} не найдено.")
    else:
        print("Сессия tmux не найдена.")

def stop_all():
    server = libtmux.Server()
    session = server.find_where({"session_name": "jupyter_envs"})

    if session:
        print("Останавливаем все окружения")
        session.kill_session()
    else:
        print("Сессия tmux не найдена.")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Manage Jupyter Notebook environments with tmux.")
    subparsers = parser.add_subparsers(dest='command')

    start_parser = subparsers.add_parser("start", help="Запустить N окружений")
    start_parser.add_argument("num_envs", type=int, help="Количество окружений для запуска")

    stop_parser = subparsers.add_parser("stop", help="Остановить окружение по ID")
    stop_parser.add_argument("env_id", type=int, help="ID окружения для остановки")

    subparsers.add_parser("stop_all", help="Остановить все окружения")

    return parser.parse_args()

if __name__ == "__main__":
    
    args = parse_arguments()

    if args.command == "start":
        start(args.num_envs)

    elif args.command == "stop":
        stop(args.env_id)

    elif args.command == "stop_all":
        stop_all()
