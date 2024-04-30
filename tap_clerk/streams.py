from __future__ import annotations

import sys
import typing as t

import requests
from singer_sdk import typing as th
from singer_sdk.helpers.jsonpath import extract_jsonpath

from tap_clerk.client import ClerkStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources


class OrganizationsStream(ClerkStream):
    """Organizations stream class."""
    name = "organizations"
    path = "/organizations"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("object", th.StringType),
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("slug", th.StringType),
        th.Property("members_count", th.IntegerType),
        th.Property("max_allowed_memberships", th.IntegerType),
        th.Property("admin_delete_enabled", th.BooleanType),
        th.Property("public_metadata", th.ObjectType(additional_properties=True)),
        th.Property("private_metadata", th.ObjectType(additional_properties=True)),
        th.Property("created_by", th.StringType),
        th.Property("created_at", th.IntegerType),
        th.Property("updated_at", th.IntegerType),
    ).to_dict()

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        yield from extract_jsonpath("$.data[*]", input=response.json())

    def get_child_context(self, record: dict, context: t.Optional[dict]) -> dict:
        return { "organization_id": record["id"] }

class OrganizationMembershipStream(ClerkStream):
    """OrganizationMembership stream class."""
    name = "organization_membership"
    parent_stream_type = OrganizationsStream
    ignore_parent_replication_keys = True
    path = "/organizations/{organization_id}/memberships"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.StringType, description="The unique identifier for the membership"),
        th.Property("object", th.StringType, description="Type of the object, should be 'organization_membership'"),
        th.Property("role", th.StringType, description="Role within the organization"),
        th.Property("permissions", th.ArrayType(th.StringType), description="List of permissions"),
        th.Property("public_metadata", th.ObjectType(additional_properties=True), description="Public metadata"),
        th.Property("private_metadata", th.ObjectType(additional_properties=True), description="Private metadata"),
        th.Property("organization", th.ObjectType(
            th.Property("object", th.StringType),
            th.Property("id", th.StringType),
            th.Property("name", th.StringType),
            th.Property("slug", th.StringType),
            th.Property("members_count", th.IntegerType),
            th.Property("max_allowed_memberships", th.IntegerType),
            th.Property("admin_delete_enabled", th.BooleanType),
            th.Property("public_metadata", th.ObjectType(additional_properties=True)),
            th.Property("private_metadata", th.ObjectType(additional_properties=True)),
            th.Property("created_by", th.StringType),
            th.Property("created_at", th.IntegerType),
            th.Property("updated_at", th.IntegerType)
        ), description="Embedded organization object"),
        th.Property("public_user_data", th.ObjectType(
            th.Property("user_id", th.StringType),
            th.Property("first_name", th.StringType),
            th.Property("last_name", th.StringType),
            th.Property("profile_image_url", th.StringType),
            th.Property("image_url", th.StringType),
            th.Property("has_image", th.BooleanType),
            th.Property("identifier", th.StringType)
        ), description="Public data of the user associated with the membership"),
        th.Property("created_at", th.IntegerType, description="Timestamp of when the membership was created"),
        th.Property("updated_at", th.IntegerType, description="Timestamp of when the membership was last updated")
    ).to_dict()

class UsersStream(ClerkStream):
    """Users stream class."""
    name = "users"
    path = "/users"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.StringType, description="The unique identifier for a user"),
        th.Property("object", th.StringType),
        th.Property("external_id", th.StringType),
        th.Property("primary_email_address_id", th.StringType),
        th.Property("primary_phone_number_id", th.StringType),
        th.Property("primary_web3_wallet_id", th.StringType),
        th.Property("username", th.StringType),
        th.Property("first_name", th.StringType),
        th.Property("last_name", th.StringType),
        th.Property("profile_image_url", th.StringType),
        th.Property("image_url", th.StringType),
        th.Property("has_image", th.BooleanType),
        th.Property("public_metadata", th.ObjectType(additional_properties=True)),
        th.Property("private_metadata", th.ObjectType(additional_properties=True)),
        th.Property("unsafe_metadata", th.ObjectType(additional_properties=True)),
        th.Property("email_addresses", th.ArrayType(th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("object", th.StringType),
            th.Property("email_address", th.StringType),
            th.Property("reserved", th.BooleanType),
            th.Property("verification", th.ObjectType(
                th.Property("status", th.StringType),
                th.Property("strategy", th.StringType),
                th.Property("attempts", th.IntegerType),
                th.Property("expire_at", th.IntegerType)
            )),
            th.Property("linked_to", th.ArrayType(th.ObjectType(
                th.Property("type", th.StringType),
                th.Property("id", th.StringType)
            ))),
            th.Property("created_at", th.IntegerType),
            th.Property("updated_at", th.IntegerType)
        ))),
        th.Property("phone_numbers", th.ArrayType(th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("object", th.StringType),
            th.Property("phone_number", th.StringType),
            th.Property("reserved_for_second_factor", th.BooleanType),
            th.Property("default_second_factor", th.BooleanType),
            th.Property("reserved", th.BooleanType),
            th.Property("verification", th.ObjectType(
                th.Property("status", th.StringType),
                th.Property("strategy", th.StringType),
                th.Property("attempts", th.IntegerType),
                th.Property("expire_at", th.IntegerType)
            )),
            th.Property("linked_to", th.ArrayType(th.ObjectType(
                th.Property("type", th.StringType),
                th.Property("id", th.StringType)
            ))),
            th.Property("backup_codes", th.ArrayType(th.StringType)),
            th.Property("created_at", th.IntegerType),
            th.Property("updated_at", th.IntegerType)
        ))),
        th.Property("web3_wallets", th.ArrayType(th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("object", th.StringType),
            th.Property("web3_wallet", th.StringType),
            th.Property("verification", th.ObjectType(
                th.Property("status", th.StringType),
                th.Property("strategy", th.StringType),
                th.Property("nonce", th.StringType),
                th.Property("attempts", th.IntegerType),
                th.Property("expire_at", th.IntegerType)
            )),
            th.Property("created_at", th.IntegerType),
            th.Property("updated_at", th.IntegerType)
        ))),
        th.Property("passkeys", th.ArrayType(th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("object", th.StringType),
            th.Property("name", th.StringType),
            th.Property("last_used_at", th.IntegerType),
            th.Property("verification", th.ObjectType(
                th.Property("status", th.StringType),
                th.Property("strategy", th.StringType),
                th.Property("nonce", th.StringType),
                th.Property("attempts", th.IntegerType),
                th.Property("expire_at", th.IntegerType)
            ))
        ))),
        th.Property("password_enabled", th.BooleanType),
        th.Property("two_factor_enabled", th.BooleanType),
        th.Property("totp_enabled", th.BooleanType),
        th.Property("backup_code_enabled", th.BooleanType),
        th.Property("external_accounts", th.ArrayType(th.ObjectType(additional_properties=True))),
        th.Property("saml_accounts", th.ArrayType(th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("object", th.StringType),
            th.Property("provider", th.StringType),
            th.Property("active", th.BooleanType),
            th.Property("email_address", th.StringType),
            th.Property("first_name", th.StringType),
            th.Property("last_name", th.StringType),
            th.Property("provider_user_id", th.StringType),
            th.Property("public_metadata", th.ObjectType(additional_properties=True)),
            th.Property("verification", th.ObjectType(
                th.Property("status", th.StringType),
                th.Property("strategy", th.StringType),
                th.Property("external_verification_redirect_url", th.StringType),
                th.Property("error", th.ObjectType(
                    th.Property("message", th.StringType),
                    th.Property("long_message", th.StringType),
                    th.Property("code", th.StringType),
                    th.Property("meta", th.ObjectType(additional_properties=True)),
                    th.Property("clerk_trace_id", th.StringType)
                )),
                th.Property("expire_at", th.IntegerType),
                th.Property("attempts", th.IntegerType)
            ))
        ))),
        th.Property("last_sign_in_at", th.IntegerType),
        th.Property("banned", th.BooleanType),
        th.Property("locked", th.BooleanType),
        th.Property("lockout_expires_in_seconds", th.IntegerType),
        th.Property("verification_attempts_remaining", th.IntegerType),
        th.Property("updated_at", th.IntegerType),
        th.Property("created_at", th.IntegerType),
        th.Property("delete_self_enabled", th.BooleanType),
        th.Property("create_organization_enabled", th.BooleanType),
        th.Property("last_active_at", th.IntegerType)
    ).to_dict()

    def get_url_params(self, context: dict | None, next_page_token: t.Any | None) -> dict[str, t.Any]:
        params: dict = {"limit": self.API_LIMIT_PAGE_SIZE}
        if next_page_token:
            params["offset"] = next_page_token
        if self.replication_key:
            params["order_by"] = f'+{self.replication_key}'
        self.logger.info(f"QUERY PARAMS: {params}")
        return params
