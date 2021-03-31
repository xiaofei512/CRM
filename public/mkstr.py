import string
import random

def letters(strlen=6):
    """指定长度的字母字符串"""
    random_str = ''
    base_str = string.ascii_letters#所有字母
    length = len(base_str)-1
    for i in range(strlen):
        random_str += base_str[random.randint(0,length)]
    return random_str

def digits(strlen=6):
    """指定长度的数字字符串"""
    random_str = ''
    base_str = string.digits#所有数字
    length = len(base_str)-1
    for i in range(strlen):
        random_str += base_str[random.randint(0,length)]
    return random_str

def spechara(strlen=6):
    """指定长度的特殊字符字符串"""
    random_str = ''
    base_str = string.punctuation + string.whitespace #所有字符串加空格
    length = len(base_str)-1
    for i in range(strlen):
        random_str += base_str[random.randint(0,length)]
    return random_str

def allof(strlen=6):
    """指定长度的所有可打印的字符串"""
    random_str = ''
    base_str = string.printable #所有字符串加空格
    length = len(base_str)-1
    for i in range(strlen):
        random_str += base_str[random.randint(0,length)]
    return random_str
