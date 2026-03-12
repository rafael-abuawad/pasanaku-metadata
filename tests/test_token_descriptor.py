import base64
import json


DATA_URI_PREFIX = "data:application/json;base64,"
IMAGE_URI_PREFIX = "data:image/svg+xml;base64,"

EXPECTED_TRAIT_TYPES = [
    "Total Deposited",
    "Current Index",
    "Ended",
    "Recovered",
    "Creator",
    "Created At",
    "Last Updated At",
    "Participants",
    "Asset",
    "Amount",
    "Token ID",
]


def decode_token_uri(uri: str) -> dict:
    """Strip the data-URI prefix and base64-decode the JSON payload."""
    assert uri.startswith(DATA_URI_PREFIX)
    encoded = uri[len(DATA_URI_PREFIX) :]
    return json.loads(base64.b64decode(encoded).decode("utf-8"))


def get_attribute(metadata: dict, trait_type: str):
    """Return the 'value' for a given trait_type inside attributes."""
    for attr in metadata["attributes"]:
        if attr["trait_type"] == trait_type:
            return attr["value"]
    raise KeyError(f"trait_type '{trait_type}' not found in attributes")


# ---------------------------------------------------------------------------
# Output format
# ---------------------------------------------------------------------------


class TestOutputFormat:
    def test_returns_data_uri_prefix(self, token_descriptor, make_rotating_savings):
        uri = token_descriptor.tokenURI(1, make_rotating_savings())
        assert uri.startswith(DATA_URI_PREFIX)

    def test_is_valid_base64_json(self, token_descriptor, make_rotating_savings):
        uri = token_descriptor.tokenURI(1, make_rotating_savings())
        metadata = decode_token_uri(uri)
        assert isinstance(metadata, dict)


# ---------------------------------------------------------------------------
# Top-level JSON fields
# ---------------------------------------------------------------------------


class TestTopLevelFields:
    def test_name_contains_token_id(self, token_descriptor, make_rotating_savings):
        metadata = decode_token_uri(
            token_descriptor.tokenURI(1, make_rotating_savings())
        )
        assert metadata["name"] == "Pasanaku #1"

    def test_description_is_correct(self, token_descriptor, make_rotating_savings):
        metadata = decode_token_uri(
            token_descriptor.tokenURI(1, make_rotating_savings())
        )
        assert (
            metadata["description"]
            == "A rotating savings protocol onchain, deployed on the Arbitrum network."
        )

    def test_image_field_prefix(self, token_descriptor, make_rotating_savings):
        metadata = decode_token_uri(
            token_descriptor.tokenURI(1, make_rotating_savings())
        )
        assert metadata["image"].startswith(IMAGE_URI_PREFIX)

    def test_all_attributes_present(self, token_descriptor, make_rotating_savings):
        metadata = decode_token_uri(
            token_descriptor.tokenURI(1, make_rotating_savings())
        )
        actual_traits = [a["trait_type"] for a in metadata["attributes"]]
        assert actual_traits == EXPECTED_TRAIT_TYPES


# ---------------------------------------------------------------------------
# Attribute values
# ---------------------------------------------------------------------------


class TestAttributeValues:
    def test_total_deposited(self, token_descriptor, make_rotating_savings):
        savings = make_rotating_savings(totalDeposited=5_000)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        assert get_attribute(metadata, "Total Deposited") == "5000"

    def test_current_index(self, token_descriptor, make_rotating_savings):
        savings = make_rotating_savings(currentIndex=3)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        assert get_attribute(metadata, "Current Index") == "3"

    def test_ended_false(self, token_descriptor, make_rotating_savings):
        savings = make_rotating_savings(ended=False)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        assert get_attribute(metadata, "Ended") is False

    def test_ended_true(self, token_descriptor, make_rotating_savings):
        savings = make_rotating_savings(ended=True)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        assert get_attribute(metadata, "Ended") is True

    def test_recovered_false(self, token_descriptor, make_rotating_savings):
        savings = make_rotating_savings(recovered=False)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        assert get_attribute(metadata, "Recovered") is False

    def test_recovered_true(self, token_descriptor, make_rotating_savings):
        savings = make_rotating_savings(recovered=True)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        assert get_attribute(metadata, "Recovered") is True

    def test_creator_address_hex_format(
        self, token_descriptor, make_rotating_savings, accounts
    ):
        savings = make_rotating_savings(creator=accounts[0].address)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        creator = get_attribute(metadata, "Creator")
        assert creator.startswith("0x")
        assert len(creator) == 42
        assert creator == accounts[0].address.lower()

    def test_created_at(self, token_descriptor, make_rotating_savings):
        savings = make_rotating_savings(createdAt=1_700_000_000)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        assert get_attribute(metadata, "Created At") == "1700000000"

    def test_last_updated_at(self, token_descriptor, make_rotating_savings):
        savings = make_rotating_savings(lastUpdatedAt=1_700_100_000)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        assert get_attribute(metadata, "Last Updated At") == "1700100000"

    def test_participants_count(
        self, token_descriptor, make_rotating_savings, accounts
    ):
        savings = make_rotating_savings(
            participants=[accounts[0].address, accounts[1].address, accounts[2].address]
        )
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        assert get_attribute(metadata, "Participants") == "3"

    def test_asset_address_hex_format(
        self, token_descriptor, make_rotating_savings, accounts
    ):
        savings = make_rotating_savings(asset=accounts[2].address)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        asset = get_attribute(metadata, "Asset")
        assert asset.startswith("0x")
        assert len(asset) == 42
        assert asset == accounts[2].address.lower()

    def test_amount(self, token_descriptor, make_rotating_savings):
        savings = make_rotating_savings(amount=999)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        assert get_attribute(metadata, "Amount") == "999"

    def test_token_id_attribute_matches_input(
        self, token_descriptor, make_rotating_savings
    ):
        metadata = decode_token_uri(
            token_descriptor.tokenURI(42, make_rotating_savings())
        )
        assert get_attribute(metadata, "Token ID") == "42"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_token_id_zero(self, token_descriptor, make_rotating_savings):
        metadata = decode_token_uri(
            token_descriptor.tokenURI(0, make_rotating_savings())
        )
        assert metadata["name"] == "Pasanaku #0"
        assert get_attribute(metadata, "Token ID") == "0"

    def test_large_token_id(self, token_descriptor, make_rotating_savings):
        large_id = 2**128
        metadata = decode_token_uri(
            token_descriptor.tokenURI(large_id, make_rotating_savings())
        )
        assert metadata["name"] == f"Pasanaku #{large_id}"
        assert get_attribute(metadata, "Token ID") == str(large_id)

    def test_multiple_participants(
        self, token_descriptor, make_rotating_savings, accounts
    ):
        participants = [accounts[i].address for i in range(5)]
        savings = make_rotating_savings(participants=participants)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        assert get_attribute(metadata, "Participants") == "5"

    def test_empty_participants(self, token_descriptor, make_rotating_savings):
        savings = make_rotating_savings(participants=[])
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        assert get_attribute(metadata, "Participants") == "0"

    def test_zero_amounts(self, token_descriptor, make_rotating_savings):
        savings = make_rotating_savings(amount=0, totalDeposited=0, currentIndex=0)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        assert get_attribute(metadata, "Amount") == "0"
        assert get_attribute(metadata, "Total Deposited") == "0"
        assert get_attribute(metadata, "Current Index") == "0"

    def test_different_token_ids_produce_different_names(
        self, token_descriptor, make_rotating_savings
    ):
        savings = make_rotating_savings()
        meta_a = decode_token_uri(token_descriptor.tokenURI(1, savings))
        meta_b = decode_token_uri(token_descriptor.tokenURI(2, savings))
        assert meta_a["name"] != meta_b["name"]
        assert meta_a["name"] == "Pasanaku #1"
        assert meta_b["name"] == "Pasanaku #2"

    def test_pure_function_no_sender_required(
        self, token_descriptor, make_rotating_savings
    ):
        uri = token_descriptor.tokenURI(1, make_rotating_savings())
        assert uri.startswith(DATA_URI_PREFIX)
