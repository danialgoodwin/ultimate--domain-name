from pathlib import Path


def write(file: str, text: str):
    path = Path(file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main():
    print('main()')


if __name__ == '__main__':
    main()
