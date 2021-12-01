pragma solidity ^0.5.0;

import "./WOWCoin.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";


contract WOWToken is ERC20, ERC20Detailed, ERC20Mintable {
    mapping(address => uint) public balances;
    mapping(address => mapping(address => uint)) public allowance;

    // event Transfer(address indexed from, address indexed to, uint value);
    // event Approval(address indexed owener, address indexed spender, uint value);
    
    constructor (
        uint totalSupply,
        string name,
        string symbol,
        uint decimals,
        WOWCoin token
    ) public ERC20Mintable(0x8E3dd544e1617507D9162F44E14A78a484942256) {

    }
}
contract WOWCoinTokenDeployer {
    // Create an `address public` variable called `kasei_token_address`.
    address public WOWToken;
    // Create an `address public` variable called `kasei_crowdsale_address`.
    address public WOWCoin;

    //Add the constructor
    constructor(
       string memory name,
       string memory symbol,
       address payable wallet,
       uint supply
    ) public {
       // Create a new instance of the KaseiCoin contract.
    
    WOWCoin token = new wowToken(name, symbol, supply);
        
        // Assign the token contract’s address to the `kasei_token_address` variable.
        
    WOW_token_address = address(0x8E3dd544e1617507D9162F44E14A78a484942256);

       
        // Set the `KaseiCoinCrowdsale` contract as a minter
    
    token.addMinter(WOW_token_address);

        // Have the `KaseiCoinCrowdsaleDeployer` renounce its minter role.
    
    token.renounceMinter();
    }
}