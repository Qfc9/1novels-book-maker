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

    return (title, chapter + "\n")

def get_content(page_source):
    start = page_source.find('<div class="chapter-content-p">') + 31
    end = page_source[start:].find('</div>')

    content = remove_tags(page_source[start:start+end])
    content = recover_grammar(content)

    return content

def get_next_page(page_source):
    start = page_source.find('<select name="chapterz" class="chapterz">') + 41
    start = page_source[start:].find('<a href="') + start + 9
    end = page_source[start:].find('"')

    return page_source[start:start+end]

def remove_tags(text):
    tag_re = re.compile(r'<[^>]+>')
    break_re = re.compile(r'(<br/>|<br />)')
    newline_re = re.compile(r'\n')
    text = newline_re.sub("", text)
    text = break_re.sub("\n", text)
    return tag_re.sub('', text)

def recover_grammar(text):
    squote_re = re.compile(r'(&#39;|&#039;)')
    dquote_re = re.compile(r'&quot;')
    space_re = re.compile(r'&nbsp;')
    text = squote_re.sub("'", text)
    text = dquote_re.sub('"', text)
    return space_re.sub(" ", text)

def main():
    url = "http://1novels.com/"
    url_ext = "241255-demon-thief.html"

    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}

    book = open("test.txt", "w")

    while(url_ext != url[:-1]):
        req = urllib.request.Request(url + url_ext, None, headers)
        with urllib.request.urlopen(req) as response:
            page_source = response.read().decode('utf-8', "ignore")
            title = get_title(page_source)
            book.write(title[0] + "\n\n")
            book.write(title[1])

            content = get_content(page_source)
            book.write(content)

            url_ext = get_next_page(page_source)
            print(url_ext)

    book.close()

if __name__ == '__main__':
    main()
