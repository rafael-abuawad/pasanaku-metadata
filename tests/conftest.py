import pytest
import ape


@pytest.fixture(scope="session")
def deployer(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def token_descriptor(deployer, project):
    return deployer.deploy(project.TokenDescriptor)


@pytest.fixture
def make_rotating_savings(accounts):
    """Factory fixture that returns a default RotatingSavings dict with keyword overrides."""

    def _factory(**overrides):
        defaults = {
            "participants": [accounts[0].address, accounts[1].address],
            "asset": accounts[2].address,
            "amount": 1_000_000_000_000_000_000,
            "currentIndex": 1,
            "totalDeposited": 2_000_000_000_000_000_000,
            "tokenId": 1,
            "ended": False,
            "recovered": False,
            "creator": accounts[0].address,
            "createdAt": 1_700_000_000,
            "lastUpdatedAt": 1_700_100_000,
        }
        defaults.update(overrides)
        return defaults

    return _factory
