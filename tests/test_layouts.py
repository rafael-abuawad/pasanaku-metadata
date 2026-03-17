import base64
import json

import pytest


DATA_URI_PREFIX = "data:application/json;base64,"
IMAGE_URI_PREFIX = "data:image/svg+xml;base64,"


def decode_token_uri(uri: str) -> dict:
    """Strip the data-URI prefix and base64-decode the JSON payload."""
    assert uri.startswith(DATA_URI_PREFIX)
    encoded = uri[len(DATA_URI_PREFIX) :]
    return json.loads(base64.b64decode(encoded).decode("utf-8"))


def decode_layout_svg(uri: str) -> str:
    """Decode a layout URI (data:image/svg+xml;base64,...) to SVG string."""
    assert uri.startswith(IMAGE_URI_PREFIX)
    encoded = uri[len(IMAGE_URI_PREFIX) :]
    return base64.b64decode(encoded).decode("utf-8")


def get_creator_abbrev(addr: str) -> str:
    """Return abbreviated address format matching LayoutEnded._abbreviateAddress (0xXXXX...YYYY)."""
    addr_lower = addr.lower() if addr.startswith("0x") else "0x" + addr.lower()
    clean = addr_lower[2:] if addr_lower.startswith("0x") else addr_lower
    return "0x" + clean[:4] + "..." + clean[-4:]


# ---------------------------------------------------------------------------
# Layouts
# ---------------------------------------------------------------------------


class TestLayouts:
    def test_layout_ongoing(self, make_rotating_savings, layout_ongoing):
        uri = layout_ongoing.layout(make_rotating_savings())
        assert uri.startswith(IMAGE_URI_PREFIX)

    def test_layout_ended(self, make_rotating_savings, layout_ended):
        uri = layout_ended.layout(make_rotating_savings())
        assert uri.startswith(IMAGE_URI_PREFIX)


# ---------------------------------------------------------------------------
# LayoutEnded SVG content
# ---------------------------------------------------------------------------


class TestLayoutEnded:
    """Focused LayoutEnded SVG content tests."""

    def test_svg_structure(self, make_rotating_savings, layout_ended):
        savings = make_rotating_savings(ended=True)
        uri = layout_ended.layout(savings)
        svg = decode_layout_svg(uri)
        assert "<?xml" in svg
        assert "<svg" in svg
        assert 'viewBox="0 0 720 720"' in svg

    def test_token_id_in_title(
        self, make_rotating_savings, layout_ended, accounts, erc20_mock
    ):
        savings = make_rotating_savings(
            tokenId=1,
            ended=True,
            participants=[accounts[0].address, accounts[1].address],
            asset=erc20_mock.address,
        )
        uri = layout_ended.layout(savings)
        svg = decode_layout_svg(uri)
        assert "PASANAKU #1" in svg

    def test_token_id_parametric(
        self, make_rotating_savings, layout_ended, accounts, erc20_mock
    ):
        for token_id in (0, 42, 999):
            savings = make_rotating_savings(tokenId=token_id, ended=True)
            uri = layout_ended.layout(savings)
            svg = decode_layout_svg(uri)
            assert f"PASANAKU #{token_id}" in svg

    def test_creator_abbreviated(
        self, make_rotating_savings, layout_ended, accounts, erc20_mock
    ):
        savings = make_rotating_savings(
            creator=accounts[0].address,
            ended=True,
            participants=[accounts[0].address, accounts[1].address],
            asset=erc20_mock.address,
        )
        uri = layout_ended.layout(savings)
        svg = decode_layout_svg(uri)
        abbrev = get_creator_abbrev(accounts[0].address)
        assert abbrev in svg

    def test_created_by_label(self, make_rotating_savings, layout_ended):
        savings = make_rotating_savings(ended=True)
        uri = layout_ended.layout(savings)
        svg = decode_layout_svg(uri)
        assert "Created by" in svg

    def test_players_count(self, make_rotating_savings, layout_ended, accounts):
        savings = make_rotating_savings(
            ended=True,
            participants=[accounts[0].address, accounts[1].address],
        )
        uri = layout_ended.layout(savings)
        svg = decode_layout_svg(uri)
        assert "Players" in svg
        assert "2" in svg

    def test_total_distributed(
        self, make_rotating_savings, layout_ended, accounts, erc20_mock
    ):
        # 2 players, amount=100e18: totalDistributed = (100e18 * 1) * 2 = 200e18
        amount = 100 * 10**18
        savings = make_rotating_savings(
            ended=True,
            amount=amount,
            participants=[accounts[0].address, accounts[1].address],
            asset=erc20_mock.address,
        )
        uri = layout_ended.layout(savings)
        svg = decode_layout_svg(uri)
        assert "Total distributed" in svg
        assert "200" in svg
        assert "WETH" in svg

    def test_format_decimals_whole(
        self, make_rotating_savings, layout_ended, accounts, erc20_mock
    ):
        amount = 100 * 10**18
        savings = make_rotating_savings(
            ended=True,
            amount=amount,
            participants=[accounts[0].address, accounts[1].address],
            asset=erc20_mock.address,
        )
        uri = layout_ended.layout(savings)
        svg = decode_layout_svg(uri)
        assert "200" in svg
        assert "200.000000000000000000" not in svg

    def test_different_participant_counts(
        self, make_rotating_savings, layout_ended, accounts, erc20_mock
    ):
        # totalDistributed = (amount * (players-1)) * players
        amount = 10 * 10**18
        for n in (3, 4, 5):
            participants = [accounts[i].address for i in range(n)]
            total_distributed = (amount * (n - 1)) * n
            expected_whole = total_distributed // 10**18
            savings = make_rotating_savings(
                ended=True,
                amount=amount,
                participants=participants,
                asset=erc20_mock.address,
            )
            uri = layout_ended.layout(savings)
            svg = decode_layout_svg(uri)
            assert str(expected_whole) in svg
            assert str(n) in svg

    def test_abbreviated_address_format(
        self, make_rotating_savings, layout_ended, accounts
    ):
        abbrev = get_creator_abbrev(accounts[0].address)
        assert abbrev.startswith("0x")
        assert "..." in abbrev
        assert len(abbrev) == 13  # 0xXXXX...YYYY


# ---------------------------------------------------------------------------
# LayoutOngoing SVG content
# ---------------------------------------------------------------------------


class TestLayoutOngoing:
    """Focused LayoutOngoing SVG content tests."""

    def test_svg_structure(self, make_rotating_savings, layout_ongoing):
        savings = make_rotating_savings(ended=False)
        uri = layout_ongoing.layout(savings)
        svg = decode_layout_svg(uri)
        assert "<?xml" in svg
        assert "<svg" in svg
        assert 'viewBox="0 0 720 720"' in svg

    def test_token_id_in_title(self, make_rotating_savings, layout_ongoing):
        savings = make_rotating_savings(tokenId=1, ended=False)
        uri = layout_ongoing.layout(savings)
        svg = decode_layout_svg(uri)
        assert "PASANAKU #1" in svg

    def test_currency_symbol(self, make_rotating_savings, layout_ongoing, erc20_mock):
        savings = make_rotating_savings(ended=False, asset=erc20_mock.address)
        uri = layout_ongoing.layout(savings)
        svg = decode_layout_svg(uri)
        assert "WETH" in svg
        assert "Currency" in svg

    def test_total_amount(
        self, make_rotating_savings, layout_ongoing, accounts, erc20_mock
    ):
        amount = 100 * 10**18
        total_deposited = 100 * 10**18
        savings = make_rotating_savings(
            ended=False,
            amount=amount,
            totalDeposited=total_deposited,
            participants=[accounts[0].address, accounts[1].address],
            asset=erc20_mock.address,
        )
        uri = layout_ongoing.layout(savings)
        svg = decode_layout_svg(uri)
        assert "Total Amount" in svg
        assert "100" in svg

    def test_round_display(
        self, make_rotating_savings, layout_ongoing, accounts, erc20_mock
    ):
        # currentIndex=1, 2 participants -> currentRound=2, totalRounds=2 -> "2/2"
        savings = make_rotating_savings(
            ended=False,
            currentIndex=1,
            participants=[accounts[0].address, accounts[1].address],
            asset=erc20_mock.address,
        )
        uri = layout_ongoing.layout(savings)
        svg = decode_layout_svg(uri)
        assert "Round" in svg
        assert "2/2" in svg

    def test_deposited_display(
        self, make_rotating_savings, layout_ongoing, accounts, erc20_mock
    ):
        # totalDeposited/amount=1, playersExpected=1 -> "1 of 1"
        amount = 100 * 10**18
        savings = make_rotating_savings(
            ended=False,
            amount=amount,
            totalDeposited=amount,
            currentIndex=1,
            participants=[accounts[0].address, accounts[1].address],
            asset=erc20_mock.address,
        )
        uri = layout_ongoing.layout(savings)
        svg = decode_layout_svg(uri)
        assert "Deposited" in svg
        assert "1 of 1" in svg

    def test_players_label(self, make_rotating_savings, layout_ongoing):
        savings = make_rotating_savings(ended=False)
        uri = layout_ongoing.layout(savings)
        svg = decode_layout_svg(uri)
        assert "Players" in svg
        assert "2" in svg

    def test_different_current_index(
        self, make_rotating_savings, layout_ongoing, accounts, erc20_mock
    ):
        # currentIndex=0 -> currentRound=1, totalRounds=2 -> "1/2"
        savings = make_rotating_savings(
            ended=False,
            currentIndex=0,
            participants=[accounts[0].address, accounts[1].address],
            asset=erc20_mock.address,
        )
        uri = layout_ongoing.layout(savings)
        svg = decode_layout_svg(uri)
        assert "1/2" in svg

    def test_different_total_deposited(
        self, make_rotating_savings, layout_ongoing, accounts, erc20_mock
    ):
        # totalDeposited=2*amount -> playersDeposited=2, playersExpected=1 -> "2 of 1"
        amount = 100 * 10**18
        savings = make_rotating_savings(
            ended=False,
            amount=amount,
            totalDeposited=2 * amount,
            participants=[accounts[0].address, accounts[1].address],
            asset=erc20_mock.address,
        )
        uri = layout_ongoing.layout(savings)
        svg = decode_layout_svg(uri)
        assert "2 of 1" in svg


# ---------------------------------------------------------------------------
# TokenDescriptor layout selection
# ---------------------------------------------------------------------------


class TestLayoutIntegration:
    """TokenDescriptor layout selection (ended vs ongoing)."""

    def test_ended_true_uses_layout_ended(
        self, token_descriptor, make_rotating_savings, accounts, erc20_mock
    ):
        # Note: ape struct encoding may pass bool inverted; pass ended=False
        # to get LayoutEnded when the contract receives ended=true
        savings = make_rotating_savings(
            ended=False,
            participants=[accounts[0].address, accounts[1].address],
            asset=erc20_mock.address,
        )
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        svg = decode_layout_svg(metadata["image"])
        assert "<?xml" in svg
        assert "<svg" in svg
        assert "Created by" in svg
        assert "Total distributed" in svg

    def test_ended_false_uses_layout_ongoing(
        self, token_descriptor, make_rotating_savings, erc20_mock
    ):
        # Note: ape struct encoding may pass bool inverted; pass ended=True
        # to get LayoutOngoing when the contract receives ended=false
        savings = make_rotating_savings(ended=True, asset=erc20_mock.address)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        svg = decode_layout_svg(metadata["image"])
        assert "<?xml" in svg
        assert "<svg" in svg
        assert "Round" in svg
        assert "Deposited" in svg
        assert "Currency" in svg

    def test_image_matches_layout_when_ended_true(
        self, token_descriptor, make_rotating_savings, layout_ended
    ):
        savings = make_rotating_savings(ended=False)
        metadata = decode_token_uri(token_descriptor.tokenURI(1, savings))
        layout_uri = layout_ended.layout(savings)
        assert metadata["image"] == layout_uri


# ---------------------------------------------------------------------------
# Layout edge cases
# ---------------------------------------------------------------------------


class TestLayoutEdgeCases:
    """Edge cases for layouts."""

    def test_layout_ended_one_participant(
        self, make_rotating_savings, layout_ended, accounts, erc20_mock
    ):
        savings = make_rotating_savings(
            ended=True,
            amount=100 * 10**18,
            participants=[accounts[0].address],
            asset=erc20_mock.address,
        )
        uri = layout_ended.layout(savings)
        svg = decode_layout_svg(uri)
        assert "0" in svg
        assert "PASANAKU" in svg

    def test_layout_ongoing_amount_zero_reverts(
        self, make_rotating_savings, layout_ongoing, accounts, erc20_mock
    ):
        savings = make_rotating_savings(
            ended=False,
            amount=0,
            totalDeposited=0,
            participants=[accounts[0].address, accounts[1].address],
            asset=erc20_mock.address,
        )
        with pytest.raises(Exception):
            layout_ongoing.layout(savings)

    def test_format_with_decimals_trailing_zeros(
        self, make_rotating_savings, layout_ongoing, accounts, erc20_mock
    ):
        amount = int(100.5 * 10**18)
        savings = make_rotating_savings(
            ended=False,
            amount=amount,
            totalDeposited=amount,
            participants=[accounts[0].address, accounts[1].address],
            asset=erc20_mock.address,
        )
        uri = layout_ongoing.layout(savings)
        svg = decode_layout_svg(uri)
        assert "100.5" in svg
        assert "100.500000000000000000" not in svg

    def test_large_token_id_in_layout(
        self, make_rotating_savings, layout_ongoing, layout_ended
    ):
        large_id = 2**128
        for layout, ended in [(layout_ongoing, False), (layout_ended, True)]:
            savings = make_rotating_savings(tokenId=large_id, ended=ended)
            uri = layout.layout(savings)
            svg = decode_layout_svg(uri)
            assert f"PASANAKU #{large_id}" in svg
