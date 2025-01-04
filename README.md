![PyPI - Version](https://img.shields.io/pypi/v/requests-verbose)

# requests-verbose

Convert [requests.Response](https://requests.readthedocs.io/en/latest/api/#requests.Response) object into a string 
mimicking `curl --verbose` output. Useful for debugging of an HTTP request and its response.

## Install

```shell
pip install requests-verbose
```

## Usage

```python
import requests
from requests_verbose import http_str
resp = requests.get("https://raw.githubusercontent.com/python/peps/refs/heads/main/peps/pep-0020.rst")
print(http_str(resp))
```

Results in:
```
HTTP Request
GET https://raw.githubusercontent.com/python/peps/refs/heads/main/peps/pep-0020.rst HTTP/11
> User-Agent: python-requests/2.32.3
> Accept-Encoding: gzip, deflate
> Accept: */*
> Connection: keep-alive

<NO BODY>

HTTP Response
https://raw.githubusercontent.com/python/peps/refs/heads/main/peps/pep-0020.rst HTTP/11
< Connection: keep-alive
< Content-Length: 891
< Cache-Control: max-age=300
< Content-Security-Policy: default-src 'none'; style-src 'unsafe-inline'; sandbox
< Content-Type: text/plain; charset=utf-8
< ETag: W/"7488b1a4236ea135e37614a1865fe92f1ad29f6f2bfde5aa9fbee59f18a58a61"
< Strict-Transport-Security: max-age=31536000
< X-Content-Type-Options: nosniff
< X-Frame-Options: deny
< X-XSS-Protection: 1; mode=block
< X-GitHub-Request-Id: F68F:4E53C:8963C11:8F181B5:67784A69
< Content-Encoding: gzip
< Accept-Ranges: bytes
< Date: Fri, 03 Jan 2025 20:38:52 GMT
< Via: 1.1 varnish
< X-Served-By: cache-vie6340-VIE
< X-Cache: HIT
< X-Cache-Hits: 0
< X-Timer: S1735936733.781834,VS0,VE7
< Vary: Authorization,Accept-Encoding,Origin
< Access-Control-Allow-Origin: *
< Cross-Origin-Resource-Policy: cross-origin
< X-Fastly-Request-ID: 326d7cae8caa6dd4663daa6dda7c037e51f36453
< Expires: Fri, 03 Jan 2025 20:43:52 GMT
< Source-Age: 115

PEP: 20
Title: The Zen of Python
<...>
```

## Help

```python
from requests_verbose import http_str
help(http_str)
```

## Development

- Open a GitHub Issue, ask a question first
- Build and install locally:

```shell
make dev
```

- Make changes
- Before commiting

```shell
make format
```

- Commit and open a Pull Request

## License

See [LICENSE](https://github.com/pilosus/requests-verbose/tree/main/LICENSE)
