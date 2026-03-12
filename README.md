# Pasanaku Metadata

On-chain NFT metadata contract for [Pasanaku](https://github.com/moon-mint/pasanaku) — a rotating savings protocol on Arbitrum.

`TokenDescriptor` generates fully on-chain `tokenURI` responses (base64-encoded JSON with an SVG image) for each Pasanaku savings round NFT.

## Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/)
- [Ape Framework](https://docs.apeworx.io/ape/stable/) (installed via `uv`)

## Setup

```bash
uv sync
```

## Compile

```bash
uv run ape compile
```

## Test

```bash
uv run ape test -v -s
```

## Deploy

Create a `.env` file with your deployer account alias:

```
DEPLOYER=my-account
```

Then run:

```bash
uv run ape run deploy --network arbitrum:mainnet:alchemy
```

## Project Structure

```
contracts/
  TokenDescriptor.sol    # On-chain metadata generator
scripts/
  deploy.py              # Deployment script
tests/
  conftest.py            # Shared pytest fixtures
  test_token_descriptor.py  # Test suite (26 tests)
```

## Contract Overview

`TokenDescriptor.tokenURI(uint256, RotatingSavings)` is a `pure` function that takes a token ID and a `RotatingSavings` struct and returns a `data:application/json;base64,` URI. The decoded JSON contains:

| Field | Description |
|---|---|
| `name` | `"Pasanaku #<tokenId>"` |
| `description` | Protocol description |
| `image` | Base64-encoded SVG data URI |
| `attributes` | 11 trait entries (see below) |

### Attributes

| Trait | Type |
|---|---|
| Total Deposited | string (uint) |
| Current Index | string (uint) |
| Ended | boolean |
| Recovered | boolean |
| Creator | string (address) |
| Created At | string (timestamp) |
| Last Updated At | string (timestamp) |
| Participants | string (count) |
| Asset | string (address) |
| Amount | string (uint) |
| Token ID | string (uint) |

## Dependencies

- [OpenZeppelin Contracts v5.6.1](https://github.com/OpenZeppelin/openzeppelin-contracts) — `ERC721`, `Strings`, `Base64`

## License

MIT
