from hashlib import md5
import datetime, random


class Common(object):
    # Mã hóa md5 chuỗi string
    @staticmethod
    def md5(string):
        return md5(string.encode()).hexdigest()

    # Tạo tên file mới từ file ban đầu
    @staticmethod
    def gen_rnd_filename():
        filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))

    # Thêm thời gian vào tên file ban đầu
    @staticmethod
    def gen_filename(filename):
        filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return '%s-%s' % (filename_prefix, Common.rename_file(filename))

    # Thay thế các ký tự thừa trong chuỗi bằng ký tự -
    @staticmethod
    def rename_file(filename):
        while filename.find('  ') >= 0:
            filename = filename.replace('  ', ' ')

        if filename.find(' - ') >= 0:
            filename = filename.replace(' - ', '-')

        if filename.find(' + ') >= 0:
            filename = filename.replace(' + ', '-')

        if filename.find(' _ ') >= 0:
            filename = filename.replace(' _ ', '-')

        if filename.find(' ') >= 0:
            filename = filename.replace(' ', '-')

        return filename