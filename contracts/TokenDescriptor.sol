// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";
import {Base64} from "@openzeppelin/contracts/utils/Base64.sol";
import {RotatingSavings} from "./interfaces/IRotatingSavings.sol";
import {ILayout} from "./interfaces/ILayout.sol";

contract TokenDescriptor {
    using Strings for uint256;

    ILayout public immutable layoutA;
    ILayout public immutable layoutB;

    constructor(address _layoutA, address _layoutB) {
        layoutA = ILayout(_layoutA);
        layoutB = ILayout(_layoutB);
    }

    function tokenURI(
        uint256 tokenId,
        RotatingSavings memory rotatingSavings
    ) public view returns (string memory) {
        string memory imageURI = _imageURI(rotatingSavings);

        string memory dataURI = string.concat(
            '{"name": "Pasanaku #',
            tokenId.toString(),
            '", "description": "A rotating savings protocol onchain, deployed on the Arbitrum network.", "image": "',
            imageURI,
            '", "attributes": [',
            '{"trait_type": "Total Deposited", "value": "',
            rotatingSavings.totalDeposited.toString(),
            '"},',
            '{"trait_type": "Current Index", "value": "',
            rotatingSavings.currentIndex.toString(),
            '"},',
            '{"trait_type": "Ended", "value": ',
            rotatingSavings.ended ? "true" : "false",
            '},',
            '{"trait_type": "Recovered", "value": ',
            rotatingSavings.recovered ? "true" : "false",
            '},',
            '{"trait_type": "Creator", "value": "',
            Strings.toHexString(uint256(uint160(rotatingSavings.creator)), 20),
            '"},',
            '{"trait_type": "Created At", "value": "',
            rotatingSavings.createdAt.toString(),
            '"},',
            '{"trait_type": "Last Updated At", "value": "',
            rotatingSavings.lastUpdatedAt.toString(),
            '"},',
            '{"trait_type": "Participants", "value": "',
            rotatingSavings.participants.length.toString(),
            '"},',
            '{"trait_type": "Asset", "value": "',
            Strings.toHexString(uint256(uint160(rotatingSavings.asset)), 20),
            '"},',
            '{"trait_type": "Amount", "value": "',
            rotatingSavings.amount.toString(),
            '"},',
            '{"trait_type": "Token ID", "value": "',
            tokenId.toString(),
            '"}'
            ']}'
        );
        return
            string.concat(
                "data:application/json;base64,",
                Base64.encode(bytes(dataURI))
            );
    }

    function _imageURI(RotatingSavings memory rotatingSavings) private view returns (string memory) {
        if (rotatingSavings.ended) {
            return layoutB.layout(rotatingSavings);
        }
        return layoutA.layout(rotatingSavings);
    }
}
