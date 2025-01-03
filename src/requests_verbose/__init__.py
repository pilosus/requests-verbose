# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Sequence

import requests
from requests.structures import CaseInsensitiveDict

DEFAULT_BODY_SIZE = 10 * 1024  # 10 Kb

DEFAULT_SENSITIVE_HEADERS = (
    "authorisation",
    "token_secret",
    "api-key",
    # The following list of header names is taken from the `sentry-python` project:
    # https://github.com/getsentry/sentry-python/blob/bb85c26a2b877965c5e0a0cd841b7f676ec2533e/sentry_sdk/scrubber.py
    # distributed under MIT License: Copyright (c) 2018-2024 Functional Software, Inc. dba Sentry
    # stolen from relay
    "password",
    "passwd",
    "secret",
    "api_key",
    "apikey",
    "auth",
    "credentials",
    "mysql_pwd",
    "privatekey",
    "private_key",
    "token",
    "session",
    # django
    "csrftoken",
    "sessionid",
    # wsgi
    "x_csrftoken",
    "x_forwarded_for",
    "set_cookie",
    "cookie",
    "authorization",
    "x_api_key",
    # other common names used in the wild
    "aiohttp_session",  # aiohttp
    "connect.sid",  # Express
    "csrf_token",  # Pyramid
    "csrf",  # (this is a cookie name used in accepted answers on stack overflow)
    "_csrf",  # Express
    "_csrf_token",  # Bottle
    "PHPSESSID",  # PHP
    "_session",  # Sanic
    "symfony",  # Symfony
    "user_session",  # Vue
    "_xsrf",  # Tornado
    "XSRF-TOKEN",  # Angular, Laravel
)


def _filter_sensitive_headers(
    headers: CaseInsensitiveDict[str] | dict[str, str],
    sensitive_headers: Sequence[str] | None,
) -> CaseInsensitiveDict[str] | dict[str, str]:
    """
    Redact values of potentially sensitive HTTP headers for safe logging
    """
    if sensitive_headers is None:
        return headers

    result = {}
    for header_name, header_value in headers.items():
        if header_name.lower() in sensitive_headers:
            result[header_name] = "[Filtered]"
        else:
            result[header_name] = header_value
    return result


def _headers_to_str(
    headers: CaseInsensitiveDict[str] | dict[str, str], prefix: str
) -> str:
    result = []
    for name, value in headers.items():
        result.append(f"{prefix} {name}: {value}")
    return "\n".join(result)


def _get_body_size(s: str | bytes | None) -> int:
    if isinstance(s, bytes):
        return len(s)
    # TODO shall we handle different encodings here?
    if isinstance(s, str):
        return len(s)
    if s is None:
        return 0


def _prep_header_for_logging(
    headers: CaseInsensitiveDict[str] | dict[str, str],
    prefix: str,
    sensitive_headers: Sequence[str] | None,
) -> str:
    redacted = _filter_sensitive_headers(
        headers=headers, sensitive_headers=sensitive_headers
    )
    message = _headers_to_str(headers=redacted, prefix=prefix)
    return message


def _prep_body(
    body: str | bytes | None, body_size_limit_bytes: int | None = None
) -> str | bytes:
    body_size = _get_body_size(body)
    if body is None:
        return "<NO BODY>"
    if body_size_limit_bytes is None:
        return body
    if body_size >= body_size_limit_bytes:
        return f"<BODY EXCEEDS LIMIT> (size {body_size} bytes, limit {body_size_limit_bytes} bytes)"
    return body


def http_str(
    response: requests.Response,
    body_size_limit_bytes: int | None = DEFAULT_BODY_SIZE,
    sensitive_headers: Sequence[str] | None = DEFAULT_SENSITIVE_HEADERS,
) -> str:
    """
    Return a string representing a prepared HTTP request and corresponding HTTP response.

    :param response: requests.Response object
    :param body_size_limit_bytes: show body if its size does not exceeds given limit in bytes, None - no limits
    :param sensitive_headers: list or tuple of headers to be redacted for security reasons, None - no redaction
    :return: string representing an HTTP-request and a corresponding HTTP-response
    """
    request = response.request
    request_template = "{method} {url} HTTP/{version}\n{headers}\n\n{body}"
    request_headers = _prep_header_for_logging(
        headers=request.headers, prefix=">", sensitive_headers=sensitive_headers
    )
    version = response.raw.version
    request_body = _prep_body(request.body, body_size_limit_bytes)
    request_str = request_template.format(
        method=request.method,
        url=request.url,
        version=version,
        headers=request_headers,
        body=request_body,
    )

    response_template = "{url} HTTP/{version}\n{headers}\n\n{body}"
    response_headers = _prep_header_for_logging(
        headers=response.headers, prefix="<", sensitive_headers=sensitive_headers
    )
    response_body = _prep_body(response.text, body_size_limit_bytes)
    response_str = response_template.format(
        url=response.url,
        version=version,
        headers=response_headers,
        body=response_body,
    )
    message = (
        f"HTTP Request\n" f"{request_str}\n\n" f"HTTP Response\n" f"{response_str}"
    )
    return message
