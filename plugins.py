from pelican import signals
from pelican.contents import Article
import uuid, json, pathlib, datetime
from bs4 import BeautifulSoup
import os, sys, random

map = {'articles': []}

try:
    with open('map.json', 'r', encoding='utf8') as file:
        map = json.load(file)
except IOError:
    pass

def add_article_uuid(content):
    if not isinstance(content, Article):
        return
    article = {
        'title': content.title,
        'category': content.category.name,
        'slug': content.slug,
        'filename':pathlib.Path(content.source_path).name
    }
    record = next((x for x in map['articles'] if x['slug'] == content.slug), None)
    if (record is not None):
        index = map['articles'].index(record)
        map['articles'][index] = article
    else:
        map['articles'].append(article)

def finalized(_):
    with open('map.json', 'w', encoding='utf8') as file:
        json.dump(map, file, ensure_ascii=False, indent=4)

def add_summary(content):
    if (isinstance(content, Article)):
        html = BeautifulSoup(content._content, 'html.parser')
        # 锚点
        new_content = BeautifulSoup(content._content, 'html.parser')
        anchors = html.find_all(['h1', 'h2'])
        h2_titles = new_content.find_all(['h1', 'h2'])
        for index, item in enumerate(anchors):
            item.name = 'a'
            link = 'article-anchor-{}'.format(index)
            item['href'] = '#{}'.format(link)
            tag = BeautifulSoup('<a class="article-anchor"></a>', 'html.parser')
            tag.a['id'] = link
            h2_titles[index].append(tag)
        content.anchors = anchors
        highlight_tables = new_content.find_all('table', { 'class': 'highlighttable' })
        for item in highlight_tables:
            tag = BeautifulSoup('<div></div>', 'html.parser')
            tag.div['class'] = 'highlighttable-wrapper'
            item.wrap(tag.div)
        content.content_with_anchors = str(new_content)
        # 概述
        content._summary = html.text.replace('\n', ' ')
        # 首图
        img = html.find('img')
        if img:
            img['class'] = 'article-thumb-image mr25'
        content.thumb_image = img
        content.title = content.title

def add_info_handler(content):
    if (isinstance(content, Article)):
        date = datetime.datetime.strptime(content.locale_date, '%Y-%m-%d')
        content.human_read_date = date.strftime('%Y年%m月%d日 %a')

def add_uuid_slug(pelican):
    for root, dirs, files in os.walk(pelican.path):
        index = len(files)
        for file in files:
            if (file.endswith('.md')):
                with open(os.path.join(root, file), 'r+', encoding='utf8') as f:
                    data = f.readlines()
                    for line in data:
                        if line == '\n':
                            data.insert(0, 'Slug: {}\n'.format(uuid.uuid4().hex))
                            f.seek(0)
                            f.writelines(data)
                            break
                        if line.startswith('Slug:'):
                            break

def register():
    signals.initialized.connect(add_uuid_slug)
    signals.content_object_init.connect(add_article_uuid)
    signals.content_object_init.connect(add_summary)
    signals.content_object_init.connect(add_info_handler)
    signals.finalized.connect(finalized)