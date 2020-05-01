
def check_file_extension(file_with_path):
    """
    :param file_with_path: File Name With Path
    :return: Extension of the file
    """
    import os
    return os.path.splitext(file_with_path)[1][1:].strip()


def delimiter_detect(file_with_path):
    """
    :param file_with_path: File Name With Path
    :return: Delimiter
    """
    import csv
    file = open(file_with_path, 'r')
    dialect = csv.Sniffer().sniff(file.readline(), ['|', '\t', '~', '^', ';', ','])
    delimiter = dialect.delimiter
    file.close()
    return delimiter


def detect_file_encoding(file_with_path):
    """
    :param file_with_path: File Name With Path
    :return: file's encoding
    """
    import chardet
    with open(file_with_path, 'rb') as rawdata:
        result = chardet.detect(rawdata.read(10000))
    rawdata.close()
    return result['encoding']


def file_reader(file_with_path):
    """
    :param file_with_path: File Name With Path
    :return: Pandas Dataframe
    """
    import pandas as pd
    import xlrd
    file_extension = check_file_extension(file_with_path)

    if file_extension in ['csv', 'txt']:
        try:
            df = pd.read_csv(file_with_path, delimiter=delimiter_detect(file_with_path), engine='python',
                             dtype=str, encoding=detect_file_encoding(file_with_path))
            print(df.head())
            return df
            # df.to_pickle(file_with_path + '.pkl')
        except Exception as e:
            print(e)
            pass

    if file_extension in ['xlsx', 'xls']:
        try:
            wb = xlrd.open_workbook(file_with_path)
            sheet = wb.sheet_by_name('Sheet1')
            headers = [str(cell.value) for cell in sheet.row(0)]
            converters = {}
            for columns in headers:
                converters.update({"'" + columns + "'": str})
            df = pd.read_excel(file_with_path, converters=converters, sheet_name='Sheet1')
            # print(df.head())
            return df
        except Exception as e:
            print(e)
            pass

