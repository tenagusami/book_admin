# import odfpy
import json


def main():
    file = open('testbooks.json', 'r')
    book_data = json.load(file)
    print(book_data)
    return


if __name__ == '__main__':
    main()
