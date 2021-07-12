# Github Unwatch

## Dependencies
- [Python 3.6+](https://www.python.org/downloads/)

## Configuration
### Install

```bash
$ pip install -r requirements.txt
```

### Authentication token
Generate a new token in [personal access tokens](https://github.com/settings/tokens) github page.

## Run

Using option:

```bash
$ python unwatch.py ORG --token <TOKEN>
```

Or using env var:

```bash
export GITHUB_TOKEN=<TOKEN>
$ python unwatch.py ORG
```

## Safelist
If exists some repositories that you don't want unwatch, create a txt or json file named `safelist.(txt|json)` and put in all repositories that should not be touched.

Text file example:

```txt
repo1
repo2
repo3
```

Json file example:

```json
[
    "repo1",
    "repo2",
    "repo3"
]
```

*obs:* All safelists will be read, so if exists a `safelist.txt` and `safelist.json` the script will merge both in one list.
