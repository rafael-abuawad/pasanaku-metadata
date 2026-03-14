// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.30;

import {RotatingSavings} from "./IRotatingSavings.sol";

interface ILayout {
    function layout(RotatingSavings memory rotatingSavings) external pure returns (string memory);
}