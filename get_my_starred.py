import requests

fields = [
    'name', 'language','full_name', 'stargazers_count', 'description',  'updated_at', 'homepage','clone_url',
]

table_header = """| {name} | {language}| {full_name} | {stargazers_count}  | {description}  |\
{updated_at} | {homepage} | {clone_url} |{page}|
|------|-----------|----------|-------------|-----------|------------------|----------|------------|-------------------------|
""".format(**{field:field for field in fields}, page='page')

template ="| {name} | {language} | {full_name} | {stargazers_count}  | {description} |\
{updated_at} | {homepage} | {clone_url} |{page}|\n"



def get_pages(pages=1):
    """
    :pages: total_page
    """
    url = "https://api.github.com/users/onepisya/starred?page={}&sort=starred&per_page=100"
    payload = {}
    headers = {}
    star_pages = (requests.request("GET", url, headers=headers,
                                   data=payload).json() for i in range(1, pages+1))
    return star_pages


def process_pages(star_pages):
    for idx, page in enumerate(star_pages):
        for repo in page:
            project = {field: str(repo.get(field, '无')).replace('|', "∧") for field in fields}
            project.update({'page': idx+1})
            project['name'] = make_img(repo.get('name'), repo.get('html_url'))
            yield project


def make_img(name, url):
    return f"""[{name}]({url})"""


def save_pages(projects):
    with open("./README.md", "w+", encoding="utf-8") as fp:
        fp.write("# my_starred_repo\
show me my starred repo\
\
---\
\
\
")
        fp.write(table_header)
        for project in projects:
            fp.write(template.format(**project))

def main():
    pages = get_pages(15)
    project_gen = process_pages(pages)
    projects = sorted(project_gen,key=lambda x: x['language'],reverse=False)
    save_pages(projects)


if __name__ == "__main__":
    main()
