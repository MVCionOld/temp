import os
import re

import collections
from bs4 import BeautifulSoup


def get_redirect_links(filename, path):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")
    with open(os.path.join(path, filename), "rb") as html_file:
        html = html_file.read().decode()
        data = re.findall(link_re, html)
        return list(set(data) & set(os.listdir(path)))


"""
def build_tree(start, end, path):
    files = dict(itertools.zip_longest(os.listdir(path), [], fillvalue=set()))
    files_entries = set()
    for filename in files.keys():
        for redirect_filename in get_redirect_links(filename, path):
            if redirect_filename in files_entries:
                files[filename].add(redirect_filename)
                files[redirect_filename].add(filename)
    for filename in files.keys():
        files[filename] = list(files[filename])
    return files
"""


def build_tree(path, start, end):
    visited = {start}
    queue = collections.deque([start])
    parents = {start: None}
    while queue:
        current = queue.popleft()
        if current == end:
            break
        for next_article in get_redirect_links(current, path):
            if next_article not in visited:
                queue.append(next_article)
                parents[next_article] = current
                visited.add(next_article)
                if next_article == end:
                    return parents, True
    return parents, False


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):
    bridge, current = [], end
    parents, correct = build_tree(path, start, end)

    if not correct:
        return []

    while current is not None:
        bridge.append(current)
        current = parents[current]
    return bridge


def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно добраться от start до end, то,
    по крайней мере, известны сами start и end, и можно распарсить хотя бы их: bridge = [end, start]. Оценка за тест,
    в этом случае, будет сильно снижена, но на минимальный проходной балл наберется, и тест будет пройден.
    Чтобы получить максимальный балл, придется искать все страницы. Удачи!
    """

    if {start, end} & set(os.listdir(path)) != {start, end}:
        raise ValueError(f"There are no articles '{start}', '{end}'")

    bridge = build_bridge(start, end, path)  # Искать список страниц можно как угодно, даже так: bridge = [end, start]

    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open("{}{}".format(path, file)) as data:
            soup = BeautifulSoup(data, "html.parser")

        body = soup.find(id="bodyContent")

        # TODO посчитать реальные значения
        imgs = 5  # Количество картинок (img) с шириной (width) не меньше 200
        headers = 10  # Количество заголовков, первая буква текста внутри которого: E, T или C
        linkslen = 15  # Длина максимальной последовательности ссылок, между которыми нет других тегов
        lists = 20  # Количество списков, не вложенных в другие списки

        out[file] = [imgs, headers, linkslen, lists]

    return out
