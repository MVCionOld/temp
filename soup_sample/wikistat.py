import collections
import itertools
import os
import re

from bs4 import BeautifulSoup


def get_redirect_links(filename, path):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")
    with open(os.path.join(path, filename), "rb") as html_file:
        html = html_file.read().decode()
        data = re.findall(link_re, html)
        return list(set(data))


def build_tree(start, end, path):
    files = dict(itertools.zip_longest(os.listdir(path), [], fillvalue=set()))
    files_entries = set(os.listdir(path))
    for filename in files.keys():
        for redirect_filename in get_redirect_links(filename, path):
            if redirect_filename in files_entries:
                files[filename].add(redirect_filename)
                files[redirect_filename].add(filename)
    for filename in files.keys():
        files[filename] = list(files[filename])
    return files


def bfs(files, start, end):
    visited = {start}
    queue = collections.deque([start])
    parents = dict(start=None)
    while queue:
        current = queue.popleft()
        if current == end:
            break
        for next in files[current]:
            if next not in visited:
                queue.append(next)
                parents[next] = current
                visited.add(next)
                if next == end:
                    return parents, True
    return parents, False


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):
    files = build_tree(start, end, path)
    bridge, current = [], end
    parents, correct = bfs(files, start, end)

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

    bridge = build_bridge(start, end, path)  # Искать список страниц можно как угодно, даже так: bridge = [end, start]

    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open("{}{}".format(path, file)) as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        # TODO посчитать реальные значения
        imgs = 5  # Количество картинок (img) с шириной (width) не меньше 200
        headers = 10  # Количество заголовков, первая буква текста внутри которого: E, T или C
        linkslen = 15  # Длина максимальной последовательности ссылок, между которыми нет других тегов
        lists = 20  # Количество списков, не вложенных в другие списки

        out[file] = [imgs, headers, linkslen, lists]

    return out
