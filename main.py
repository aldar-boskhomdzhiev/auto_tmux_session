import argparse
import libtmux
import os

def start(num_envs,base_dir='./'):
    
    server = libtmux.Server()

    session = server.new_session(session_name="jupyter_envs",kill_session=True,attach=False)
    print(f"Создана сессия tmux с именем: {session}")


    for i in range(num_envs):
        env_dir = os.path.join(base_dir,f"dir{i}")

        if not os.path.exists(env_dir):
            os.makedirs(env_dir)

        window = session.new_window(window_name=f"env{i}",attach=False)
        print(f"Создано окно tmux для окружений {i} в директории {env_dir}")


def stop(env_id):

    server = libtmux.server()
    session = libtmux.Server.find_where({"session_name":"jupyter_envs"})

    if session:
        window = session.find_where({"window_name":f"env(env_id)"})
        if window:
            print(f"Останавливем окружение с ID {env_id}")
            window.kill_session()
        else:
            print(f"Окно с ID {env_id} не найдено.")


def stop_all():
    
    server = libtmux.Server()
    session = server.find_where({"session_name":"jupyter_envs"})

    if session:
        print("Останавливаем все окружения")
        session.kill_session()
    else:
        print("Сессия tmux не найдена.")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Manage Jupyter Notebook environments with tmux.")
    subparsers = parser.add_subparsers(dest='command')
    
    start_parser = subparsers.add_parser("start",help="Запустить N окружений")
    start_parser.add_argument("num_envs",type=int,help="Количество окружений для запуска")

    stop_parser = subparsers.add_parser("stop",help="Остановить все окружения")
    stop_parser.add_argument("env_id",type=int,help="ID окружения для остановки")

    subparsers.add_parser("stop_all",help="Остановить все окружения")

    return parser.parse_args()

if __name__== "__main__":
    args = parse_arguments()

    if args.command == "start":
        start(args.num_envs)
    
    elif args.command == "stop":
        stop(args.env_id)

    elif args.command == "stop_all":
        stop_all()

