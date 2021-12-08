import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--url', '-u', nargs='*')
parser.add_argument('--name', '-n', nargs='*')


def write_response(url, file):
    content = requests.get(url).content
    with open(f'save/{file}.html', 'wb') as f:
        f.write(content)


if __name__ == '__main__':
    args = parser.parse_args()
    for filename, url_name in zip(args.name, args.url):
        write_response(file=filename, url=url_name)
