from bs4 import BeautifulSoup

def generate_table_of_contents(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')
        
    for index,h1_tag in enumerate(soup.find_all('h1'),start=1):
        h1_tag['id'] = f'h1_{index}'
        
    for index,h2_tag in enumerate(soup.find_all('h2'),start=1):
        h2_tag['id'] = f'h2_{index}'

    for index,h3_tag in enumerate(soup.find_all('h3'),start=1):
        h3_tag['id'] = f'h3_{index}'

    headings = soup.find_all(['h1', 'h2', 'h3'])  # 必要な見出し要素を指定 

         # 目次用のリストを作成
    table_of_contents = []

    for heading in headings:
        table_of_contents.append({
            'id': heading.get('id'),
            'text': heading.text,
            'level': int(heading.name[1])  # 見出しのレベルを取得
        })

    return table_of_contents , soup
