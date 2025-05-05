# APIs is a tool to recive extructured data.
# As the HTTP it's a text transfer protocol,
# the solicited data using an Web API 
# must be serialized in a String format. (Normally using Json)
import requests, json
from collections import Counter
import dateutil

class GitApi:

    def __init__(self):
        ...

    def run(self):
        github_user = 'joelgrus'
        endpoint = f'https://api.github.com/users/{github_user}/repos'

        repos = json.loads(requests.get(endpoint).text) # list of dicts.
        # print(repos)

        parse = dateutil.parser.parse
        print(parse('2025-04-01'))
        dates = [parse(repo['created_at']) for repo in repos]
        month_counts = Counter(date.month for date in dates)
        
        print(dates)
        print(month_counts)

        last_5_repositories = sorted(repos, key=lambda r: r['pushed_at'], reverse=True)[:5]
        last_5_languages = [repo['language'] for repo in last_5_repositories]

        print(last_5_repositories)
        print(last_5_languages)

def main():
    ga = GitApi()
    ga.run()

if __name__ == '__main__':
    main()
