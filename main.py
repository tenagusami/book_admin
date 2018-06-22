import json
import access_ods as a
import book_data as d


def lookup_json():
    file = open('testbooks.json', 'r')
    book_data = json.load(file)
    print(book_data)
    return


def main():
    dict_table = a.read('/home/ykanya/lib/books/books.ods')
    table = d.dict2JSON(dict_table)
    print(table)

    # lookup_json()


if __name__ == '__main__':
    main()
