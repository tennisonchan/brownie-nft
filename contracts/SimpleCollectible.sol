// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract SimpleCollectible is ERC721 {
    using Counters for Counters.Counter;
    Counters.Counter public tokenIds;

    constructor() public ERC721("Digimon", "DGM") {}

    function createCollectible(string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 newTokenId = tokenIds.current();
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        tokenIds.increment();
        return newTokenId;
    }
}
