// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract SimpleContract {
    uint256 public  number;

    function store(uint256 _number) public {
       number =_number;
    }
    function retrieve() public view  returns(uint256){
        return number;
    }
    struct People{
        uint256 number;
        string name;
    }

    People[] public peoples;

    function addPersons(string memory name,uint256 _number) public{
         peoples.push(People(_number,name));
    }


}