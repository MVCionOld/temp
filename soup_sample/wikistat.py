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


class HtmlMatcher:

    def __init__(self, body):
        self.body = body

    def count_matched_imgs(self):
        imgs = 0
        for image in self.body.find_all(name='img'):
            if image.has_attr('width'):
                imgs += 1 if int(image['width']) >= 200 else 0
        return imgs

    def count_matched_headers(self):
        headers = 0
        for header in self.body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if re.match(r"^[ETC].*$", header.get_text()):
                headers += 1
        return headers

    def count_max_links_sequence(self):
        return 0

    def count_unwrapped_lists(self):
        lists = 0
        for list_ in self.body.find_all(["ul", "ol"]):
            if len({"ul", "ol"} & set([tag.name for tag in list_.parents])) == 0:
                lists += 1
        return lists


def parse(start, end, path):
    if {start, end} & set(os.listdir(path)) != {start, end}:
        raise ValueError(f"There are no articles: '{start}', '{end}'")

    bridge = build_bridge(start, end, path)
    out = {}

    for file in bridge:
        soup = BeautifulSoup(get_bfile(file, path).decode(), "html.parser")
        body = soup.find(id="bodyContent")
        matcher = HtmlMatcher(body)

        imgs = matcher.count_matched_imgs()
        headers = matcher.count_matched_headers()
        # Длина максимальной последовательности ссылок, между которыми нет других тегов
        linkslen = matcher.count_max_links_sequence()
        # Количество списков, не вложенных в другие списки
        lists = matcher.count_unwrapped_lists()

        out[file] = [imgs, headers, linkslen, lists]

    print(out) # DELETE
    return out
