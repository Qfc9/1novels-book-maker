import urllib.request, shutil, os, time
import re

def get_title(page_source):
    start = page_source.find('<h3 class="title">') + 18
    end = page_source[start:].find('</h3>')
    title_head = page_source[start:start+end]

    start = title_head.find("title") + 7
    end = title_head[start:].find('"')

    title = title_head[start:start+end]

    start =  title_head.find("</a>") + 5
    chapter = title_head[start:]

    print(title)
    print(chapter)

def get_content(page_source):
    start = page_source.find('<div class="chapter-content-p">') + 31
    end = page_source[start:].find('</div>')

    content = remove_tags(page_source[start:start+end])
    content = recover_grammar(content)

    print(content)

def get_next_page(page_source):
    start = page_source.find('<div class="chap-select">') + 25
    start = page_source[start:].find('<a href="') + start + 9
    end = page_source[start:].find('"')

    print(page_source[start:start+end])

def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)

def recover_grammar(text):
    TAG_RE = re.compile(r'&#39;')
    return TAG_RE.sub("'", text)

def main():
    url = "http://1novels.com/"
    url_ext = "241255-demon-thief.html"

    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}

    req = urllib.request.Request(url + url_ext, None, headers)

    with urllib.request.urlopen(req) as response:
        page_source = response.read().decode('utf-8')
        get_title(page_source)
        get_content(page_source)
        get_next_page(page_source)

if __name__ == '__main__':
    main()
