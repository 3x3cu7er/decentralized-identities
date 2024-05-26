// HealthcareDataSharing.sol
pragma solidity ^0.8.13;

contract HealthcareDataSharing {
    struct Patient {
        string name;
        address owner;
        mapping(address => bool) providers; // Mapping of provider addresses allowed to access patient data
    }

    mapping(address => Patient) public patients;

    event PatientRegistered(address indexed owner, string name);
    event ProviderAdded(address indexed patient, address indexed provider);
    event ProviderRemoved(address indexed patient, address indexed provider);
    event DataAccessed(address indexed patient, address indexed provider);

    function registerPatient(string memory _name) public {
        require(bytes(_name).length > 0, "Name cannot be empty");
        require(patients[msg.sender].owner == address(0), "Patient already registered");

        patients[msg.sender] = Patient(_name, msg.sender);
        emit PatientRegistered(msg.sender, _name);
    }

    function grantAccess(address _provider) public {
        require(patients[msg.sender].owner != address(0), "Patient not registered");
        patients[msg.sender].providers[_provider] = true;
        emit ProviderAdded(msg.sender, _provider);
    }

    function revokeAccess(address _provider) public {
        require(patients[msg.sender].owner != address(0), "Patient not registered");
        patients[msg.sender].providers[_provider] = false;
        emit ProviderRemoved(msg.sender, _provider);
    }

    function accessData(address _patient) public view returns (string memory) {
        require(patients[_patient].providers[msg.sender], "Provider not authorized");
        emit DataAccessed(_patient, msg.sender);
        return patients[_patient].name; // Return patient's name as an example
    }
}
