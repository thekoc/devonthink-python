import jieba
from wordcloud import WordCloud
import random
import matplotlib.pyplot as plt

from pydt3 import DEVONthink3

ignore_words = """function return var value if else for while break continue switch case default element object key array https component"""\
    .split()

def generate_wordcloud(text, output_file='wordcloud.png'):
    # 对文本进行分词
    word_list = list(jieba.cut(text))
    text = ''
    for word in word_list:
        if len(word) <= 2 or word in ignore_words:
            continue
        text += word + ' '

    # 创建词云对象
    wc = WordCloud(
        background_color='white',
        width=800,
        height=600,
        max_words=200,
        max_font_size=100,
        random_state=42
    )

    wc.generate(text)

    wc.to_file(output_file)

    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    texts = []
    dtp3 = DEVONthink3()
    db = dtp3.ext.db_by_name('blue-book')
    contents = db.contents
    print(len(contents))
    sampled_records = random.sample(db.contents, min(40, len(db.contents)))
    names = []
    texts = []
    for record in sampled_records:
        if record.type == 'picture':
            continue
        if 'newsletter' in record.location:
            continue
        name = record.name
        names.append(name)
        texts.append(name)
        texts.append(record.rich_text.splitlines()[0])

    samples = texts
    generate_wordcloud(' '.join(samples), 'wordcloud.png')