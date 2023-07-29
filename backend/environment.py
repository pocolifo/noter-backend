import os

repo_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_file(file: str):
    if not os.path.exists(file):
        return {}

    env = {}

    with open(file, 'rt') as fp:
        while (line := fp.readline()):
            line = line[line.find('#')+1:]  # get rid of the comments

            if '=' in line:
                key, val = line.split('=', 1)

                if not key:
                    continue

                val = val.rstrip().lstrip().removeprefix('"').removeprefix('\'').removesuffix('"').removesuffix('\'')
                env[key] = val

    return env

def load_all(env_file: str = os.path.join(repo_root, '.env'), default_env_file: str = os.path.join(repo_root, '.env.default')):
    env = load_file(default_env_file)

    if os.path.exists(env_file):
        for key, val in load_file(env_file).items():
            env[key] = val
    
    print(env)
    
    return env

def append_to_environ(env: dict[str, str]):
    for key, val in env.items():
        os.environ[key] = val
