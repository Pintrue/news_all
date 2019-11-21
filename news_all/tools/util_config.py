# coding=utf8


from .others import get_upper_dir


BASE_DIR = get_upper_dir(__file__, 3)

if __name__ == '__main__':
    print(BASE_DIR)
