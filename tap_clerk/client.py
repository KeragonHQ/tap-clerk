from __future__ import annotations

import sys
from typing import Any, Callable, Iterable

import requests
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.pagination import BaseOffsetPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream
from singer_sdk.helpers.jsonpath import extract_jsonpath

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]

class ClerkStream(RESTStream):
    """Clerk stream class."""

    API_LIMIT_PAGE_SIZE = 100
    RECORDS_JSONPATH = "$[*]"

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.clerk.com/v1"

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config.get("auth_token", ""),
        )

    @property
    def http_headers(self) -> dict:
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
        return headers

    def get_new_paginator(self) -> BaseOffsetPaginator:
        return BaseOffsetPaginator(start_value=0, page_size=self.API_LIMIT_PAGE_SIZE)

    def get_url_params(self, context: dict | None, next_page_token: Any | None) -> dict[str, Any]:
        params: dict = {"limit": self.API_LIMIT_PAGE_SIZE}
        if next_page_token:
            params["offset"] = next_page_token
        if self.replication_key:
            params["order_by"] = f'-{self.replication_key}'
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        yield from extract_jsonpath(self.RECORDS_JSONPATH, input=response.json())
