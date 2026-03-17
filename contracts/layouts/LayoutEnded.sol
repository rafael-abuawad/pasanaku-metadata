// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";
import {Base64} from "@openzeppelin/contracts/utils/Base64.sol";
import {IERC20Metadata} from "@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol";
import {RotatingSavings} from "../interfaces/IRotatingSavings.sol";
import {ILayout} from "../interfaces/ILayout.sol";

contract LayoutEnded is ILayout {
    using Strings for uint256;

    function layout(RotatingSavings memory rotatingSavings) external view returns (string memory) {
        return string.concat("data:image/svg+xml;base64,", Base64.encode(bytes(_imageData(rotatingSavings))));
    }

    function _imageData(RotatingSavings memory rotatingSavings) private view returns (string memory) {
        address asset = rotatingSavings.asset;
        uint256 decimals = uint256(IERC20Metadata(asset).decimals());
        string memory symbol = IERC20Metadata(asset).symbol();
        uint256 amount = rotatingSavings.amount;

        uint256 id = rotatingSavings.tokenId;
        uint256 players = rotatingSavings.participants.length;
        // total distributed = (total distributed per round) * rounds
        uint256 totalDistributed = (rotatingSavings.amount * (players - 1)) * players;
        address creator = rotatingSavings.creator;

        return string.concat(
            '<?xml version="1.0" encoding="UTF-8"?> <svg fill="none" viewBox="0 0 720 720" xmlns="http://www.w3.org/2000/svg"><defs><style>@font-face { font-family: "Fifties"; src: url("data:font/truetype;charset=utf-8;base64,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") format("truetype"); } .fifties { font-family: "Fifties", sans-serif; } .sans { font-family: "Inter", Arial, Helvetica, sans-serif; }</style></defs><g clip-path="url(#clip0_12_99)"><rect width="720" height="720" fill="url(#paint0_radial_12_99)"/><circle cx="605" cy="645" r="215" fill="url(#paint1_radial_12_99)"/><circle cx="120" cy="590" r="230" fill="url(#paint2_radial_12_99)"/><circle cx="240" cy="140" r="130" fill="url(#paint3_radial_12_99)"/><g filter="url(#filter0_d_12_99)" opacity=".52" shape-rendering="crispEdges"><rect x="80" y="503" width="560" height="122" rx="16" fill="url(#paint4_linear_12_99)"/><rect x="81" y="504" width="558" height="120" rx="15" stroke="#fff" stroke-opacity=".53" stroke-width="2"/></g><text class="sans" fill="white" font-size="32" font-weight="bold" letter-spacing="0em" style="white-space:pre" xml:space="preserve"> <tspan x="120" y="589.136">',
            _abbreviateAddress(creator),
            '</tspan> </text><text class="sans" fill="white" font-size="20" letter-spacing="0em" style="white-space:pre" xml:space="preserve"> <tspan x="120" y="550.273">Created by</tspan> </text><g filter="url(#filter1_d_12_99)" opacity=".52" shape-rendering="crispEdges"><rect x="80" y="369" width="560" height="122" rx="16" fill="url(#paint5_linear_12_99)"/><rect x="81" y="370" width="558" height="120" rx="15" stroke="#fff" stroke-opacity=".53" stroke-width="2"/></g><text class="sans" fill="white" font-size="32" font-weight="bold" letter-spacing="0em" style="white-space:pre" xml:space="preserve"> <tspan x="120" y="455.136">',
            players.toString(),
            '</tspan> </text><text class="sans" fill="white" font-size="20" letter-spacing="0em" style="white-space:pre" xml:space="preserve"> <tspan x="120" y="416.273">Players</tspan> </text><g filter="url(#filter2_d_12_99)" opacity=".52" shape-rendering="crispEdges"><rect x="80" y="235" width="560" height="122" rx="16" fill="url(#paint6_linear_12_99)"/><rect x="81" y="236" width="558" height="120" rx="15" stroke="#fff" stroke-opacity=".53" stroke-width="2"/></g><text class="sans" fill="white" font-size="32" font-weight="bold" letter-spacing="0em" style="white-space:pre" xml:space="preserve"> <tspan x="120" y="321.136">',
            formatWithDecimals(totalDistributed, decimals),
            " ",
            symbol,
            '</tspan> </text><text class="sans" fill="white" font-size="20" letter-spacing="0em" style="white-space:pre" xml:space="preserve"> <tspan x="120" y="282.273">Total distributed</tspan> </text><line x1="73" x2="647" y1="201" y2="201" opacity=".32" stroke="#fff" stroke-width="4"/><text class="fifties" fill="white" font-size="66" letter-spacing="0em" style="white-space:pre" xml:space="preserve"> <tspan x="158" y="144.5">PASANAKU #',
            id.toString(),
            '</tspan> </text></g><defs><filter id="filter0_d_12_99" x="47" y="483" width="626" height="188" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feColorMatrix in="SourceAlpha" result="hardAlpha" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"/><feOffset dy="13"/><feGaussianBlur stdDeviation="16.5"/><feComposite in2="hardAlpha" operator="out"/><feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.3 0"/><feBlend in2="BackgroundImageFix" result="effect1_dropShadow_12_99"/><feBlend in="SourceGraphic" in2="effect1_dropShadow_12_99" result="shape"/></filter><filter id="filter1_d_12_99" x="47" y="349" width="626" height="188" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feColorMatrix in="SourceAlpha" result="hardAlpha" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"/><feOffset dy="13"/><feGaussianBlur stdDeviation="16.5"/><feComposite in2="hardAlpha" operator="out"/><feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.3 0"/><feBlend in2="BackgroundImageFix" result="effect1_dropShadow_12_99"/><feBlend in="SourceGraphic" in2="effect1_dropShadow_12_99" result="shape"/></filter><filter id="filter2_d_12_99" x="47" y="215" width="626" height="188" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feColorMatrix in="SourceAlpha" result="hardAlpha" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"/><feOffset dy="13"/><feGaussianBlur stdDeviation="16.5"/><feComposite in2="hardAlpha" operator="out"/><feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.3 0"/><feBlend in2="BackgroundImageFix" result="effect1_dropShadow_12_99"/><feBlend in="SourceGraphic" in2="effect1_dropShadow_12_99" result="shape"/></filter><radialGradient id="paint0_radial_12_99" cx="0" cy="0" r="1" gradientTransform="translate(360 360) rotate(90) scale(360)" gradientUnits="userSpaceOnUse"><stop stop-color="#00A646" offset="0"/><stop stop-color="#001C18" offset="1"/></radialGradient><radialGradient id="paint1_radial_12_99" cx="0" cy="0" r="1" gradientTransform="translate(605 645) rotate(90) scale(215)" gradientUnits="userSpaceOnUse"><stop stop-color="#00A31E" stop-opacity=".34" offset="0"/><stop stop-color="#00A31E" stop-opacity="0" offset="1"/></radialGradient><radialGradient id="paint2_radial_12_99" cx="0" cy="0" r="1" gradientTransform="translate(120 590) rotate(90) scale(230)" gradientUnits="userSpaceOnUse"><stop stop-color="#007C7B" stop-opacity=".52" offset="0"/><stop stop-color="#007C7B" stop-opacity="0" offset="1"/></radialGradient><radialGradient id="paint3_radial_12_99" cx="0" cy="0" r="1" gradientTransform="translate(240 140) rotate(90) scale(130)" gradientUnits="userSpaceOnUse"><stop stop-color="#0095D8" stop-opacity=".39" offset="0"/><stop stop-color="#0095D8" stop-opacity="0" offset="1"/></radialGradient><linearGradient id="paint4_linear_12_99" x1="360" x2="360" y1="503" y2="625" gradientUnits="userSpaceOnUse"><stop stop-color="#001C18" stop-opacity=".96" offset="0"/><stop stop-color="#001C18" stop-opacity=".94" offset="1"/></linearGradient><linearGradient id="paint5_linear_12_99" x1="360" x2="360" y1="369" y2="491" gradientUnits="userSpaceOnUse"><stop stop-color="#001C18" stop-opacity=".96" offset="0"/><stop stop-color="#001C18" stop-opacity=".94" offset="1"/></linearGradient><linearGradient id="paint6_linear_12_99" x1="360" x2="360" y1="235" y2="357" gradientUnits="userSpaceOnUse"><stop stop-color="#001C18" stop-opacity=".96" offset="0"/><stop stop-color="#001C18" stop-opacity=".94" offset="1"/></linearGradient><clipPath id="clip0_12_99"><rect width="720" height="720" fill="#fff"/></clipPath></defs></svg>'
        );
    }

    function formatWithDecimals(uint256 value, uint256 decimals) internal pure returns (string memory) {
        uint256 divisor = 10 ** decimals;
        uint256 wholePart = value / divisor;
        uint256 fractionalPart = value % divisor;

        if (fractionalPart == 0) {
            return wholePart.toString();
        }

        string memory fractionalStr = fractionalPart.toString();
        // Pad with leading zeros
        while (bytes(fractionalStr).length < decimals) {
            fractionalStr = string.concat("0", fractionalStr);
        }
        // Trim trailing zeros
        bytes memory fracBytes = bytes(fractionalStr);
        uint256 end = fracBytes.length;
        while (end > 0 && fracBytes[end - 1] == 0x30) {
            end--;
        } // 0x30 = '0'
        if (end == 0) return wholePart.toString();

        bytes memory trimmed = new bytes(end);
        for (uint256 i = 0; i < end; i++) {
            trimmed[i] = fracBytes[i];
        }

        return string.concat(wholePart.toString(), ".", string(trimmed));
    }

    function _abbreviateAddress(address addr) internal pure returns (string memory) {
        string memory full = Strings.toHexString(uint256(uint160(addr)), 20);
        bytes memory fullBytes = bytes(full);
        bytes memory result = new bytes(13);
        result[0] = fullBytes[0]; // '0'
        result[1] = fullBytes[1]; // 'x'
        result[2] = fullBytes[2];
        result[3] = fullBytes[3];
        result[4] = fullBytes[4];
        result[5] = fullBytes[5];
        result[6] = 0x2e; // '.'
        result[7] = 0x2e;
        result[8] = 0x2e;
        result[9] = fullBytes[38];
        result[10] = fullBytes[39];
        result[11] = fullBytes[40];
        result[12] = fullBytes[41];
        return string(result);
    }
}
