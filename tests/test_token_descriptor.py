import pytest
import ape

@pytest.fixture
def deployer(accounts):
    return accounts[0]

@pytest.fixture
def token_descriptor(deployer):
    return ape.project.TokenDescriptor.deploy(sender=deployer)

def test_token_uri(token_descriptor, accounts):
    token_id = 1
    rotating_savings = {
        "participants": [accounts[0]],
        "asset": accounts[1],
        "amount": 1000000000000000000,
        "currentIndex": 0,
        "totalDeposited": 1000000000000000000,
        "tokenId": token_id,
        "ended": False,
        "recovered": False,
        "creator": accounts[0],
        "createdAt": 1000000000000000000,
        "lastUpdatedAt": 1000000000000000000,
    }

    token_uri = token_descriptor.tokenURI(token_id, rotating_savings, sender=accounts[0])
    print(token_uri)