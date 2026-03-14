// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";
import {Base64} from "@openzeppelin/contracts/utils/Base64.sol";
import {RotatingSavings} from "../interfaces/IRotatingSavings.sol";
import {ILayout} from "../interfaces/ILayout.sol";

contract LayoutA is ILayout {
    using Strings for uint256; 

    function layout(RotatingSavings memory rotatingSavings) external pure returns (string memory) {
        return string.concat('data:image/svg+xml;base64,', Base64.encode(bytes(rotatingSavings.tokenId.toString())));
    }
}