import collections
import os
import re

from bs4 import BeautifulSoup


def get_bfile(filename, path):
    with open(os.path.join(path, filename), "rb") as html_file:
        return html_file.read()


def get_redirect_links(filename, path):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")
    html = get_bfile(filename, path).decode()
    data = re.findall(link_re, html)
    return list(set(data) & set(os.listdir(path)))


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
    if {start, end} & set(os.listdir(path)) != {start, end}:
        raise ValueError(f"There are no articles '{start}', '{end}'")

    bridge = build_bridge(start, end, path)

    out = {}
    for file in bridge:
        soup = BeautifulSoup(get_bfile(file, path).decode(), "html.parser")

        body = soup.find(id="bodyContent")

        imgs = 0  # Количество картинок (img) с шириной (width) не меньше 200
        headers = 0  # Количество заголовков, первая буква текста внутри которого: E, T или C
        linkslen = 0  # Длина максимальной последовательности ссылок, между которыми нет других тегов
        lists = 0  # Количество списков, не вложенных в другие списки

        for image in body.find_all(name='img'):
            if image.has_attr('width'):
                imgs += 1 if int(image['width']) >= 200 else 0

        for header in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if re.match(r"[ETC].*", header.get_text()):
                headers += 1

        out[file] = [imgs, headers, linkslen, lists]

    return out
