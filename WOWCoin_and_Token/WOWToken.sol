pragma solidity ^0.5.0;


import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";

// Create a constructor for the KaseiCoin contract and have the contract inherit the libraries that you imported from OpenZeppelin.
contract WOWToken is ERC20,  ERC20Detailed, ERC20Mintable {
    constructor(
        string memory wowToken,
        string memory WOW,
        uint initial_supply
    )
        ERC20Detailed(wowToken, WOW, 18)
        public
    {
        //
    }
}

