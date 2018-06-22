import ezodf as odf
from functools import reduce


def read(file_path):
    sheets = odf.opendoc(file_path).sheets
    return reduce(lambda table, name: table+read_sheet(sheets[name]),
                  sheets.names(), [])


def read_sheet(sheet):
    table = [ods_row2_dict(row, effective_columns(sheet.row(0)), sheet.name)
             for row in sheet.rows() if not is_empty_row(row)]
    return table[1:]


def n_effective_columns(title_row):
    return len(effective_columns(title_row))


def effective_columns(title_row):
    return [cell for cell in title_row if cell.value is not None]


def is_empty_row(row):
    return not any([cell.value for cell in row])


def ods_row2_dict(row, title_row_ods, sheet_name):
    column_zip = ods_row2_zip(row, title_row_ods, sheet_name)
    columns = {column_title2key(key): value for key, value in column_zip}
    return columns


def ods_row2_zip(row, title_row, sheet_name):
    columns = [(title_row[column_id].value, str(cell.value))
               for column_id, cell in enumerate(row)
               if column_id < len(title_row)]
    columns.append(('分類', sheet_name))
    return columns


def column_title2key(title):
    if title == '題名':
        return 'original_title'
    if title == '号':
        return 'volume'
    if title == '著者（編者・監修者）':
        return 'authors'
    if title == '保管場所':
        return 'storage'
    if title == '発行年月日' or title == '発売日':
        return 'publication_date'
    if title == '発行所':
        return 'publisher'
    if title == 'ジャンル':
        return 'genre'
    if title == 'ISBN-13':
        return title
    if title == '既読（○）/未読（×）/対象外（△）':
        return 'read'
    if title == 'メディア':
        return 'medium'
    if title == '分類':
        return 'category'
    if title == '貸出':
        return 'rental'
    return 'comment'


def make_out_data_matrix(title_row, in_data_matrix):
    out_matrix = [[row[item] for item in title_row] for row in in_data_matrix]
    out_matrix.insert(0, title_row)
    return out_matrix


if __name__ == '__main__':
    pass
