import json
import regex


def dict2JSON(dict_list_in):
    dict_list = [{key: convert_value(key, value)
                  for key, value in dic.items()}
                 for dic in dict_list_in]
    dict_list_mod = process_comments(dict_list)
    return [json.dumps(dic, ensure_ascii=False) for dic in dict_list_mod]


def convert_value(key, value):
    if key == 'authors':
        author_list = semicolon_list_converter(value)
        if author_list:
            return author_list
        return ['unknown']

    if key == 'publication_date':
        return date_converter(value)

    if key == 'genre':
        return semicolon_list_converter(value)

    if key == 'read':
        return read_converter(value)

    return value


def date_converter(date_string):
    date_pattern1 = r'^(\d{4})-(\d{2})-(\d{2})'
    matched = regex.search(date_pattern1, date_string)
    if matched:
        return {'year': int(matched.group(1)),
                'month': int(matched.group(2)),
                'day': int(matched.group(3)), }

    date_pattern2 = r'^(\d{4})/(\d+)'
    matched = regex.search(date_pattern2, date_string)
    if matched:
        return {'year': int(matched.group(1)),
                'month': int(matched.group(2)),
                'day': 'unknown'}

    date_pattern3 = r'^(\d{4})'
    matched = regex.search(date_pattern3, date_string)
    if matched:
        return {'year': matched.group(1),
                'month': 'unknown',
                'day': 'unknown'}

    return {'year': 'unknown',
            'month': 'unknown',
            'day': 'unknown'}


def semicolon_list_converter(string_in):
    if not string_in:
        return []
    return [name.strip() for name in string_in.strip().split(";")
            if name.strip()]


def read_converter(value):
    if value == '○':
        return '既読'
    if value == '×':
        return '未読'
    return '対象外'


def process_comments(dict_list):
    for dic in dict_list:
        dic['book_info'] = {}
        value = dic['comment']
        if value:
            dic['book_info'], dic['comment'] = read_book_info(value)
    return dict_list


def read_book_info(comment_string):
    book_info = {}
    comment_list = semicolon_list_converter(comment_string)
    for comment in comment_list:
        extract_book_info_comment(('邦題：', 'japanese_title'),
                                  (book_info, comment_list), comment)
        extract_book_info_comment(('ASIN:', 'ASIN'),
                                  (book_info, comment_list), comment)
        extract_book_info_comment(('韓国語題：', 'korean_title'),
                                  (book_info, comment_list), comment)
    return book_info, comment_list


def extract_book_info_comment(pattern_key_tuple, comment_info_tuple, comment):
    book_info, comment_list = comment_info_tuple
    info_pattern, book_info_key = pattern_key_tuple
    if comment[0:len(info_pattern)] == info_pattern:
        book_info[book_info_key] = comment[len(info_pattern):].strip()
        comment_list.remove(comment)
    return book_info, comment_list
