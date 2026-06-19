import buildpy.markdown as md
import buildpy.htmlmaker as htmlmk
import buildpy.headtail as ht
import buildpy.metadata as meta
import buildpy.xmlbuild as xmlb
import buildpy.config as conf
from pathlib import Path
from datetime import datetime
import json

def build_about(pages):
    content = ''
    about_path = Path("posts-md/about.md")
    if not about_path.exists():
        content = "# 關於我\n這裡目前沒有內容，請建立 `posts-md/about.md`！"
    else:
        with open(about_path, 'r', encoding="utf-8") as f:
            content = f.read()
        
    html = htmlmk.html_template.format(
        f'關於我 | {conf.site_title}',
        f'''
        {meta.desc.format(f'關於 {conf.author} 和 {conf.site_title}')} 
        {meta.og_title.format(f'關於我 | {conf.site_title}')}
        {meta.og_desc.format(f'關於 {conf.author} 和 {conf.site_title}')}
        {meta.author}
        <link rel="canonical" href="{conf.url}/about.html">
        {meta.pub_date.format('2026-05-24')}
        ''',
        f'''
        {ht.get_header(pages)}
        <div id="blog">
            <div id="content">
                {md.markdown_to_html(content)}
            </div>
        </div>
        {ht.get_footer()}
        '''
    )
    return html


def build(post, pages):
    content = ''
    with open(f"posts-md/{post['slug']}.md", 'r', encoding="utf-8") as f:
        content = f.read()
        
    giscus_tips_html = conf.giscus_tips.replace("\n", "<br>")
        
    html = htmlmk.html_template.format(
        f'{post["title"]} | {conf.site_title}',
        f'''
        {meta.desc.format(post["description"])} 
        {meta.og_title.format(post["title"])}
        {meta.og_desc.format(post["description"])}
        {meta.author}
        {meta.canonical.format(post['slug'])}
        {meta.pub_date.format(post["time"])}
        ''',
        f'''
        {ht.get_header(pages)}
        <div id="blog">
            <div id="title-chunk">
                <h1 id="title" class="title">{post["title"]}</h1>
                <span id="time" class="title">{post["time"]}</span>
            </div>
            <div id="content">
                {md.markdown_to_html(content)}
                <br>
            </div>
        </div>
        <div id="comment">
            <h4>Giscus留言區</h4>
            <span>{giscus_tips_html}</span>
            <script src="https://giscus.app/client.js"
                    data-repo="{conf.giscus['repo']}"
                    data-repo-id="{conf.giscus['repo_id']}"
                    data-category="{conf.giscus['category']}"
                    data-category-id="{conf.giscus['category_id']}"
                    data-mapping="pathname"
                    data-strict="0"
                    data-reactions-enabled="1"
                    data-emit-metadata="0"
                    data-input-position="bottom"
                    data-theme="{conf.giscus['theme']}"
                    data-lang="zh-TW"
                    crossorigin="anonymous"
                    async>
            </script>
            <br>
        </div>
        {ht.get_footer()}
        '''
    )
    return html

def get_articles(posts, all_posts):
    articles = ''
    count = len(posts) if all_posts else min(len(posts), 6)

    for i in range(count):
        tags = ""
        for j in posts[i]["tags"]:
            tags += f'<span class="tag">{j}</span> '
        article = f'''
        <article class="post-card"><a href="posts/{posts[i]['slug']}.html">
            <h3>{posts[i]["title"]}</h3>
            <p class="post-time">{posts[i]["time"]}</p>
            <p class="des">{posts[i]["description"]}</p>
            <div class="tags">{tags}</div>
        </a></article>
        '''
        articles += article
    return articles

def build_home(posts, pages):
    desc_html = "<br>".join(conf.site_desc)
    
    html = htmlmk.html_template.format(
        f"首頁 | {conf.site_title}",
        f'''
        {meta.desc.format(f"{conf.site_title}的首頁")} 
        {meta.og_title.format(conf.site_title)}
        {meta.og_desc.format(f"{conf.site_title}的首頁")}
        {meta.author}
        {meta.pub_date.format("2026-05-12")}
        <meta name="google-site-verification" content="-BsyQE4UmvmmmNQqDf_hvjxk3V9AFHN1nPSElMM7Vs0" />
        <link rel="alternate" type="application/rss+xml" title="RSS" href="/rss.xml">
        ''',
        f'''
        {ht.get_header(pages)}
        <section class="hero">
            <h1>{conf.site_title}</h1>
            <p>{desc_html}</p>
        </section>

        <section id="posts-list">
            <h2>最新文章</h2>
            <div id="posts-container">
                {get_articles(posts, False)}
            </div>
        </section>
        {ht.get_footer()}
        '''
    )
    return html

def build_all(posts, pages):
    html = htmlmk.html_template.format(
        f"所有文章 | {conf.site_title}",
        f'''
        {meta.desc.format(f"{conf.site_title}的所有文章畫面")} 
        {meta.og_title.format(conf.site_title)}
        {meta.og_desc.format(f"{conf.site_title}的所有文章畫面")}
        {meta.author}
        {meta.pub_date.format("2026-05-12")}
        ''',
        f'''
        {ht.get_header(pages)}
        <section class="hero">
            <h1>所有文章</h1>
        </section>

        <section id="posts-list">
            <div id="posts-container">
                {get_articles(posts, True)}
            </div>
        </section>
        {ht.get_footer()}
        '''
    )
    return html

def buildspec(pages):
    """實作自訂獨立頁面的建置，並動態套用導覽列"""
    for page in pages:
        slug = page["slug"]
        title = page["title"]
        desc = page.get("desc") or page.get("description") or ""
        
        # 處理動態時間 TODAY
        time_str = page.get("time", "2026-01-01")
        if time_str.upper() == "TODAY":
            time_str = datetime.now().strftime("%Y-%m-%d")

        content = ''
        page_path = Path(f"posts-md/spec/{slug}.md")
        if not page_path.exists():
            content = f"# {title}\n這裡目前沒有內容，請建立 `posts-md/spec//{slug}.md`！"
        else:
            with open(page_path, 'r', encoding="utf-8") as f:
                content = f.read()

        html = htmlmk.html_template.format(
            f'{title} | {conf.site_title}',
            f'''
            {meta.desc.format(desc)} 
            {meta.og_title.format(f'{title} | {conf.site_title}')}
            {meta.og_desc.format(desc)}
            {meta.author}
            <link rel="canonical" href="{conf.url}/{slug}.html">
            {meta.pub_date.format(time_str)}
            ''',
            f'''
            {ht.get_header(pages)}
            <div id="blog">
                <div id="content">
                    {md.markdown_to_html(content)}
                </div>
            </div>
            {ht.get_footer()}
            '''
        )

        # 獨立頁面直接產生在 docs/spec 目錄下（例如 docs/spec/blogroll.html）
        with open(f'docs/spec/{slug}.html', 'w', encoding="utf-8") as f:
            f.write(html)
        print(f"  └─ 自訂頁面 {slug}.html 建置成功！ >v<")


def run_build():
    """執行完整建置的進入點"""
    Path("docs/posts").mkdir(parents=True, exist_ok=True)

    if not Path("posts.json").exists():
        print("❌ 錯誤：找不到 posts.json，無法讀取文章列表！")
        return

    with open("posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)

    posts = sorted(posts, key=lambda x: x["time"], reverse=True)

    if not Path("pages.json").exists():
        print("❌ 錯誤：找不到 pages.json，無法讀取頁面列表！")
        return

    with open("pages.json", "r", encoding="utf-8") as f:
        pages = json.load(f)

    # 1. 關於我
    try:
        with open('docs/about.html', 'w', encoding="utf-8") as f:
            f.write(build_about(pages))
    except Exception as e:
        print(f"建置 about 失敗... >皿< ({e})")
    else:
        print("建置 about 成功！ >v<")

    # 2. 各篇文章
    for post in posts:
        try:
            with open(f'docs/posts/{post["slug"]}.html', 'w', encoding="utf-8") as f:
                f.write(build(post, pages))
        except Exception as e:
            print(f"建置 {post['slug']} 失敗... >皿< ({e})")
        else:
            print(f"建置 {post['slug']} 成功！ >v<")

    # 3. 首頁
    try:
        with open("docs/index.html", "w", encoding="utf-8") as f:
            f.write(build_home(posts, pages))
    except Exception as e:
        print(f"建置 index 失敗... >皿< ({e})")
    else:
        print("建置 index 成功！ >v<")

    # 4. 所有文章
    try:
        with open("docs/all.html", "w", encoding="utf-8") as f:
            f.write(build_all(posts, pages))
    except Exception as e:
        print(f"建置 all 失敗... >皿< ({e})")
    else:
        print("建置 all 成功！ >v<")
        
    # 5. Sitemap
    try:
        with open("docs/sitemap.xml", "w", encoding="utf-8") as f:
            f.write(xmlb.buildsm(posts))
    except Exception as e:
        print(f"建置 sitemap 失敗... >皿< ({e})")
    else:
        print("建置 sitemap 成功！ >v<")

    # 6. RSS
    try:
        with open("docs/rss.xml", "w", encoding="utf-8") as f:
            f.write(xmlb.buildrss(posts))
    except Exception as e:
        print(f"建置 rss 失敗... >皿< ({e})")
    else:
        print("建置 rss 成功！ >v<")

    # 7. 自訂獨立頁面
    try:
        print("開始建置自訂獨立頁面...")
        buildspec(pages)
    except Exception as e:
        print(f"建置 spec 失敗... >皿< ({e})")
    else:
        print("建置 spec 成功！ >v<")

if __name__ == "__main__":
    run_build()

