from pathlib import Path


def load_env(file) -> dict:
    print(f'load_env({file})')
    env = {}
    with Path(file).open() as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('#'): continue
            tokens = line.split('=')
            env[tokens[0]] = tokens[1].rstrip('\n')
    print(f'    env={env}')
    return env


def main():
    print('main()')
    load_env('.env.local')


if __name__ == '__main__':
    main()
