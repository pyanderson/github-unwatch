import argparse
import json
import os

# third imports
import requests


def read_safelist():
    safelist = []
    if os.path.exists('safelist.txt'):
        with open('safelist.txt') as txt_file:
            safelist.extend(repo.strip() for repo in txt_file.readlines())
    if os.path.exists('safelist.json'):
        with open('safelist.json') as json_file:
            safelist.extend(repo.strip() for repo in json.load(json_file))
    return set([repo for repo in safelist if repo])


def repositories(org, token):
    url = 'https://api.github.com/user/subscriptions'
    params = {'page': 1, 'per_page': 100}
    headers = {'Authorization': f'token {token}'}
    repos = []
    while True:
        res = requests.get(url, params=params, headers=headers)
        page = res.json()
        repos.extend(page)
        if len(page) < 100:
            break
        params['page'] += 1
    return [repo for repo in repos if repo['owner']['login'] == org]


def unwatch_org(org, token):
    repos = repositories(org, token)
    safelist = read_safelist()
    headers = {'Authorization': f'token {token}'}
    print(f'found {len(repos)} repositories')
    total = 0
    for repo in repos:
        if repo['name'] not in safelist:
            res = requests.delete(repo['subscription_url'], headers=headers)
            if res.status_code > 399:
                print(f'failed to unwatch {repo["name"]}')
                continue
            total += 1
            print(f'successfully unwatch {repo["name"]}')
    print(f'successfully unwatch {total} repositories')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Unwatch/unsubscribe in all repositories of one '
                    'organization ignoring the repositories in the safelist'
    )
    parser.add_argument('org', help='Organization')
    parser.add_argument(
        '--token',
        default=os.environ.get('GITHUB_TOKEN'),
        help='Authentication token'
    )
    args = parser.parse_args()
    if args.token is None:
        raise SystemExit('necessary the authentication token')
    unwatch_org(args.org, args.token)
