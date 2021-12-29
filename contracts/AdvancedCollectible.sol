// SPDX-License-Identifier: MIT

pragma solidity ^0.8.8;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@chainlink/contracts/src/v0.8/dev/VRFConsumerBase.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase, ERC721URIStorage {
    using Counters for Counters.Counter;
    Counters.Counter public tokenIds;
    bytes32 keyHash;
    uint256 fee;
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;
    event requestCollectible(bytes32 indexed requestId, address requestor);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    enum Breed {
        Agumono,
        Armadillomon,
        Chibomon,
        DemiVeeimon,
        Gomamon,
        Hawkmon,
        Leafmon,
        Minomon,
        Palmon,
        Patamon,
        Poromon,
        Tokomon,
        Upamon,
        Veemon,
        Wormmon
    }

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    ) VRFConsumerBase(_vrfCoordinator, _linkToken) ERC721("Digimon", "DGM") {
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestCollectible(requestId, msg.sender);
        return requestId;
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        uint256 newTokenId = tokenIds.current();
        uint8 breedLength = uint8(type(AdvancedCollectible.Breed).max) + 1;
        Breed breed = Breed(randomness % breedLength);
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        _safeMint(requestIdToSender[requestId], newTokenId);
        // _setTokenURI(newTokenId, tokenURI);
        tokenIds.increment();
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner nor approved."
        );
        _setTokenURI(tokenId, _tokenURI);
    }

    function _burn(uint256 tokenId)
        internal
        override(ERC721, ERC721URIStorage)
    {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner nor approved."
        );
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
}
