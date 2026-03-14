// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

struct RotatingSavings {
    address[] participants;
    address asset;
    uint256 amount;
    uint256 currentIndex;
    uint256 totalDeposited;
    uint256 tokenId;
    bool ended;
    bool recovered;
    address creator;
    uint256 createdAt;
    uint256 lastUpdatedAt;
}
