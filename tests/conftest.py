import pytest


@pytest.fixture(scope="session")
def deployer(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def erc20_mock(deployer, project):
    return deployer.deploy(project.ERC20Mock, deployer.address)


@pytest.fixture(scope="session")
def layout_ongoing(deployer, project):
    return deployer.deploy(project.LayoutOngoing)


@pytest.fixture(scope="session")
def layout_ended(deployer, project):
    return deployer.deploy(project.LayoutEnded)


@pytest.fixture(scope="session")
def token_descriptor(
    deployer,
    project,
    layout_ended,
    layout_ongoing,
):
    return deployer.deploy(
        project.TokenDescriptor, layout_ended.address, layout_ongoing.address
    )


@pytest.fixture
def make_rotating_savings(accounts, erc20_mock):
    """Factory fixture that returns a default RotatingSavings dict with keyword overrides."""

    def _factory(**overrides):
        defaults = {
            "participants": [accounts[0].address, accounts[1].address],
            "asset": erc20_mock.address,
            "amount": int(100.50 * 10**18),
            "currentIndex": 1,
            "totalDeposited": int(100.50 * 10**18),
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
