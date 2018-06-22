import unittest
import json
import access_ods as a
import book_data as d

mock_json = '''{
    "original_title": "title", "volume": 1,
    "volumes_total": 1,
    "authors": {
        "author1": "Y. Kan-ya"
    },
    "publication_date": {
        "year": 2018,
        "month": 1,
        "date": 1
    },
    "publisher": "Leonid",
    "genre": {
        "genre1": "ero"
    },
    "ISBN-13": "978-4416203118",
    "read": true,
    "storage": "娯楽1",
    "book_info": {
        "japanese_book": false,
        "japanese_title": "やらしい"
    },
    "comment": ""
}'''


class TestJSON(unittest.TestCase):
    def test_read_json(self):
        j = json.loads(mock_json)
        self.assertEqual(j['genre']['genre1'], 'ero')


class TestBook(unittest.TestCase):
    def test_book(self):
        class MockCell:
            value = None

            def __init__(self, value):
                self.value = value

        class MockRow:
            row = [MockCell(None) for i in range(5)]

            def __init__(self, *args):
                self.row[0].value = True
                self.row[1].value = True

        class MockBookRow(object):
            """Documentation for ClassName

            """
            row = [MockCell('ちょっとしたストレスを自分ではね返せる子の育て方'),
                   MockCell('土井高徳'),
                   MockCell('教育1'),
                   MockCell('2016-06-25'),
                   MockCell('青春出版社'),
                   MockCell('教育; 育児'),
                   MockCell('978-4413230056'),
                   MockCell('○'),
                   MockCell(None), MockCell(None), ]
            title_row = [MockCell('題名'),
                         MockCell('著者（編者・監修者）'),
                         MockCell('保管場所'),
                         MockCell('発行年月日'),
                         MockCell('発行所'),
                         MockCell('ジャンル'),
                         MockCell('ISBN-13'),
                         MockCell('既読（○）/未読（×）/対象外（△）'),
                         MockCell('備考'), MockCell('貸出'), MockCell(None)]
            title_JSON = ['original_title',
                          'authors',
                          'storage',
                          'publication_date',
                          'publisher',
                          'genre',
                          'ISBN-13',
                          'read',
                          'comment',
                          'rental',
                          'category']
            empty_row = [MockCell(None) for i in range(10)]

        self.assertEqual(a.n_effective_columns(MockRow().row), 2)
        self.assertEqual(a.n_effective_columns(MockBookRow().title_row), 10)
        self.assertEqual(a.effective_columns(MockBookRow().title_row),
                         MockBookRow().title_row[:10])
        self.assertEqual(a.is_empty_row(MockBookRow().row), False)
        self.assertEqual(a.is_empty_row(MockBookRow().empty_row), True)
        self.assertCountEqual(
            a.ods_row2_dict(
                MockBookRow().row, MockBookRow().title_row, '書籍').keys(),
            MockBookRow().title_JSON)

    def test_book_info(self):
        self.assertEqual(
            d.semicolon_list_converter('邦題：維摩経・首楞厳三昧経; ASIN: abcde'),
            ['邦題：維摩経・首楞厳三昧経', 'ASIN: abcde'])
        self.assertEqual(
            d.extract_book_info_comment(
                ('邦題：', 'japanese_title'),
                ({}, ['ASIN: abcde']), '邦題：維摩経・首楞厳三昧経'),
            ({'japanese_title': '維摩経・首楞厳三昧経'},
             ['ASIN: abcde', '邦題：維摩経・首楞厳三昧経']))
        self.assertEqual(
            d.read_book_info('邦題：維摩経・首楞厳三昧経; ASIN: abcde'),
            ({'ASIN': 'abcde',
              'japanese_title': '維摩経・首楞厳三昧経'}, []))


if __name__ == "__main__":
    unittest.main()
