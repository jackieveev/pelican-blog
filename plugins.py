from pelican import signals
from pelican.contents import Article
import uuid, json, pathlib

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

def register():
    signals.content_object_init.connect(add_article_uuid)
    signals.finalized.connect(finalized)