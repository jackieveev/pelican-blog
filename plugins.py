from pelican import signals
from pelican.contents import Article
import uuid, json, pathlib, datetime
from bs4 import BeautifulSoup

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
        article['uuid'] = record['uuid']
        map['articles'][index] = article
    else:
        article['uuid'] = uuid.uuid4().hex
        map['articles'].append(article)
    content.slug = article['uuid']

def finalized(wasted):
    with open('map.json', 'w', encoding='utf8') as file:
        json.dump(map, file, ensure_ascii=False, indent=4)

def add_summary(content):
    if (isinstance(content, Article)):
        content._summary = BeautifulSoup(content.content, 'html.parser').text.replace('\n', ' ') * 2
        content.title = content.title * 2

def add_info_handler(content):
    if (isinstance(content, Article)):
        date = datetime.datetime.strptime(content.locale_date, '%Y-%m-%d')
        now = datetime.datetime.now()
        human_read_date = ''
        if date.year == now.year:
            if date.month == now.month:
                if date.day == now.day:
                    human_read_date = '今天'
                elif now.day - date.day == 1:
                    human_read_date = '昨天'
                else:
                    human_read_date = '{0}天前'.format(now.day - date.day)
            else:
                human_read_date = '{0}个月前'.format(now.month - date.month)
        else:
            human_read_date = '{0}年前'.format(now.year - date.year)
        content.human_read_date = human_read_date
        
def register():
    signals.content_object_init.connect(add_article_uuid)
    signals.content_object_init.connect(add_summary)
    signals.content_object_init.connect(add_info_handler)
    signals.finalized.connect(finalized)