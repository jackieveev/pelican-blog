from pelican import signals
from pelican.contents import Article
import uuid, pathlib, datetime, os, glob, sys
from bs4 import BeautifulSoup
from css_html_js_minify import (
    process_single_css_file,
    process_single_html_file,
    process_single_js_file,
)

def compress(pelican):
    for f in glob.iglob(pelican.output_path + '/**/*.htm*', recursive=True):
        process_single_html_file(f, overwrite=True)
    for f in glob.iglob(pelican.output_path + '/**/*.css', recursive=True):
        process_single_css_file(f, overwrite=True)
    for f in glob.iglob(pelican.output_path + '/**/*.js', recursive=True):
        process_single_js_file(f, overwrite=True)

def iter3(seq):
    """Generate one triplet per element in 'seq' following PEP-479."""
    nxt, cur = None, None
    for prv in seq:
        if cur:
            yield nxt, cur, prv
        nxt, cur = cur, prv
    # Don't yield anything if empty seq
    if cur:
        # Yield last element in seq (also if len(seq) == 1)
        yield nxt, cur, None


def get_translation(article, prefered_language):
    if not article:
        return None
    for translation in article.translations:
        if translation.lang == prefered_language:
            return translation
    return article


def set_neighbors(articles, next_name, prev_name):
    for nxt, cur, prv in iter3(articles):
        setattr(cur, next_name, nxt)
        setattr(cur, prev_name, prv)

        for translation in cur.translations:
            setattr(translation, next_name,
                    get_translation(nxt, translation.lang))
            setattr(translation, prev_name,
                    get_translation(prv, translation.lang))

def neighbors(generator):
    set_neighbors(generator.articles, 'next_article', 'prev_article')

    for category, articles in generator.categories:
        articles.sort(key=lambda x: x.date, reverse=True)
        set_neighbors(
            articles, 'next_article_in_category', 'prev_article_in_category')

    if hasattr(generator, 'subcategories'):
        for subcategory, articles in generator.subcategories:
            articles.sort(key=lambda x: x.date, reverse=True)
            index = subcategory.name.count('/')
            next_name = 'next_article_in_subcategory{}'.format(index)
            prev_name = 'prev_article_in_subcategory{}'.format(index)
            set_neighbors(articles, next_name, prev_name)

def add_summary(content):
    if (isinstance(content, Article)):
        html = BeautifulSoup(content._content, 'html.parser')
        # 锚点
        titles = html.find_all(['h1', 'h2', 'h3', 'h4'])
        headings = []
        for index, title in enumerate(titles):
            level = int(title.name.replace('h', ''))
            link = 'article-anchor-{}'.format(index)
            title_anchor = BeautifulSoup('<a class="article-anchor"></a>', 'html.parser')
            click_tag = BeautifulSoup('<a></a>', 'html.parser')
            title_anchor.a['id'] = link
            title['class'] = 'article-headings'
            click_tag.a['href'] = '#{}'.format(link)
            click_tag.a.append(title.text)
            title.append(title_anchor)
            headings.append((level, click_tag))
        content.headings = headings if len(headings) else None
        # 代码块包裹div，让其可以滚动
        highlight_tables = html.find_all('table', { 'class': 'highlighttable' })
        for item in highlight_tables:
            tag = BeautifulSoup('<div></div>', 'html.parser')
            tag.div['class'] = 'highlighttable-wrapper'
            item.wrap(tag.div)
        content.content_with_anchors = str(html)
        # 概述
        content._summary = html.text.replace('\n', ' ')

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
    signals.content_object_init.connect(add_summary)
    signals.content_object_init.connect(add_info_handler)
    signals.article_generator_finalized.connect(neighbors)
    signals.finalized.connect(compress)
