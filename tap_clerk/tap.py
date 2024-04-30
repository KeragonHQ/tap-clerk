from __future__ import annotations

from singer_sdk import Tap
from tap_clerk import streams
from singer_sdk import typing as th

class TapClerk(Tap):
    """Clerk tap class."""
    name = "tap-clerk"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,
            description="The token to authenticate against the Clerk API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.ClerkStream]:
        return [
            streams.OrganizationsStream(self),
            streams.OrganizationMembershipStream(self),
            streams.UsersStream(self),
        ]

if __name__ == "__main__":
    TapClerk.cli()
