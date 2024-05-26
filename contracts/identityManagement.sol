// IdentityManagement.sol
pragma solidity ^0.8.13;

contract IdentityManagement {
    struct Identity {
        string name;
        string email;
        address owner;
        bool verified;
    }

    mapping(address => Identity) public identities;

    event IdentityRegistered(address indexed owner, string name, string email);
    event IdentityUpdated(address indexed owner, string name, string email);
    event IdentityVerified(address indexed owner);
    event IdentityRevoked(address indexed owner);

    function registerIdentity(string memory _name, string memory _email) public {
        require(bytes(_name).length > 0, "Name cannot be empty");
        require(bytes(_email).length > 0, "Email cannot be empty");
        require(identities[msg.sender].owner == address(0), "Identity already registered");

        identities[msg.sender] = Identity(_name, _email, msg.sender, false);
        emit IdentityRegistered(msg.sender, _name, _email);
    }

    function updateIdentity(string memory _name, string memory _email) public {
        require(bytes(_name).length > 0, "Name cannot be empty");
        require(bytes(_email).length > 0, "Email cannot be empty");
        require(identities[msg.sender].owner != address(0), "Identity not registered");

        identities[msg.sender].name = _name;
        identities[msg.sender].email = _email;
        emit IdentityUpdated(msg.sender, _name, _email);
    }

    function verifyIdentity(address _owner) public {
        require(msg.sender == _owner || msg.sender == owner(), "Not authorized");
        require(identities[_owner].owner != address(0), "Identity not registered");

        identities[_owner].verified = true;
        emit IdentityVerified(_owner);
    }

    function revokeIdentity(address _owner) public {
        require(msg.sender == _owner || msg.sender == owner(), "Not authorized");
        require(identities[_owner].owner != address(0), "Identity not registered");

        delete identities[_owner];
        emit IdentityRevoked(_owner);
    }

    function owner() private view returns (address) {
        return address(this);
    }
}
