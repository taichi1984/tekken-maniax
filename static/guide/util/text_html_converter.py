import markdown as md
import re

def convert_to_html(article):
    article = article.replace("\n","<br>")
    html = md.markdown(article)
    html = re.sub('\[youtube=\((.*)\)\]',
                  '<iframe width="560" height="315" src="https://www.youtube.com/embed/\\1" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
                  article)

    return html;