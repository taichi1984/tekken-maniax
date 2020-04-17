import markdown
import re
import os


def convert_to_html(article):
    md = markdown.Markdown(extensions=['tables'])
    print(article)

    if os.name == 'nt':
        article = re.sub('\r\n', '  \r\n', article)
    else:
        article = re.sub('\n', '  \n', article)

    html = md.convert(article)
    print(html)
    html = re.sub('\[youtube=\((.*)\)\]',
                  '<iframe width="560" height="315" src="https://www.youtube.com/embed/\\1" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
                  html)

    return html;
