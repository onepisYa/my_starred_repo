import requests
from datetime import datetime
from datetime import timedelta

now = datetime.strftime(datetime.now(), "%x %X")
fields = [
    'name', 'language', 'full_name', 'stargazers_count', 'description',
    'updated_at', 'homepage', 'clone_url', 'html_url'
]
template = '''
<table>
            <dl>
              <dt><a href="{html_url}"> {name} </a></dt>
              <dd>
              {description}
              </dd>
            </dl>
            <tbody>
                <tr>
                    <td><b>language</b></td>
                    <td>{language}</td>
                </tr>
                <tr>
                    <td><b>full_name</b></td>
                    <td>{full_name}</td>
                </tr>
                <tr>
                    <td><b>stargazers_count</b></td>
                    <td>{stargazers_count}</td>
                </tr>
                <tr>
                    <td><b>homepage</b></td>
                    <td>{homepage}</td>
                </tr>
                <tr>
                    <td><b>clone_url</b></td>
                    <td>{clone_url}</td>
                </tr>
                <tr>
                    <td><b>updated_at(china_local_time)</b></td>
                    <td>{china_lt}</td>
                </tr>
                <tr>
                    <td><b>updated_at(utc)</b></td>
                    <td>{updated_at}</td>
                </tr>
                <tr>
                    <td><b>page</b></td>
                    <td>{page}</td>
                </tr>
            </tbody>
</table>
<hr>

'''


def get_pages(pages=1):
    """
    :pages: total_page
    """
    url = """
    https://api.github.com/users/onepisya/starred?page={}&sort=starred&per_page=100
    """.strip()

    payload = {}
    headers = {"accept": "application/vnd.github.v3+json"}
    star_pages = (requests.request("GET",
                                   url.format(i),
                                   headers=headers,
                                   data=payload).json()
                  for i in range(1, pages + 1))
    return star_pages


def process_pages(star_pages):
    for idx, page in enumerate(star_pages):
        for repo in page:
            project = {
                field: str(repo.get(field, '无')).replace('|', "∧")
                for field in fields
            }
            project.update({'page': idx + 1})
            timestamp = datetime.strptime(project["updated_at"],
                                          "%Y-%m-%dT%H:%M:%SZ")
            cn_lt = timestamp + timedelta(hours=8)
            # 计算出中国的本地时间
            project['china_lt'] = datetime.strftime(cn_lt, "%x %X")

            yield project


def save_pages(projects):
    with open("./README.md", "w+", encoding="utf-8") as fp:
        fp.write("""# my_starred_repo
show me my starred repo
update at {}
---

""".format(now))
        for project in projects:
            fp.write(template.format(**project))


def main():
    pages = get_pages(24)
    project_gen = process_pages(pages)
    projects = sorted(project_gen, key=lambda x: x['language'], reverse=False)
    save_pages(projects)


if __name__ == "__main__":
    main()
