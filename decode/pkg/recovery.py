#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
手动还原js代码
"""

import re
import execjs

# 获取执行js的函数
def get_js():
    f = open("./decode.js", 'r', encoding='utf-8')  # 打开JS文件
    line = f.readline()
    html_str = ''
    while line:
        html_str = html_str + line
        line = f.readline()
    return html_str

# 获取被解密js的函数
def get_code():
    f = open("./code.js", 'r', encoding='utf-8')  # 打开JS文件
    line = f.readline()
    html_str = ''
    while line:
        html_str = html_str + line
        line = f.readline()
    return html_str

source_js_code = get_code()
enfunc="_0x15f5"

# 执行js 获取返回值
def encrypt(n1, n2):
    """

    :param n1:
    :param n2:
    :return:
    """
    js_str = get_js()
    ctx = execjs.compile(js_str)  # 加载JS文件
    # _0x3574 是上面js的函数名字 后面是两个参数
    return ctx.call(enfunc, n1, n2)


# 正则匹配出整体这样的格式 [('_0x3574("0x0", "7ND[")', '0x0', '7ND[')， ("函数整体", "参数1", "参数2")]
res = re.findall(r"\[?(" + enfunc + "\(\"(.*?)\", \"(.*?)\"\))\]?", source_js_code)

for i in res:
    # 获取执行后的结果
    new_i = encrypt(i[1], i[2])

    # 替换结果
    source_js_code = source_js_code.replace(i[0], f"\"{new_i}\"")

# 还原后的函数
print(source_js_code)


