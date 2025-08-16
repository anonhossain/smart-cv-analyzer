const usersTable = document.getElementById("usersTable").getElementsByTagName("tbody")[0];
const usertables = document.getElementById("dataPopulate");
const editUserModal = document.getElementById("editUserModal");
const editUserForm = document.getElementById("editUserForm");
const roleFilter = document.getElementById("roleFilter");

let users = [];
let currentUserId = null;

// Fetch users from backend
async function fetchUsers() {
    try {
        const response = await fetch("http://localhost:8080/api/users");
        
        if (!response.ok) {
            throw new Error("Failed to fetch users");
        }
        users = await response.json();
        console.log(users);

        const res = await fetch("http://localhost:8080/api/info");
        if (!res.ok) {
          throw new Error("Failed to fetch info");
      }
        const data = await res.json();
        console.log(data);
        // Populate the table with all users initially
        populateTable(users, data);
    } catch (error) {
        console.error("Error fetching users:", error);
        alert("Error fetching users: " + error.message);
    }
}

function populateTable(users, data) {
    usertables.innerHTML = ""; // Clear previous entries
    let i = 1;
    users.forEach((user) => {
        const row = usertables.insertRow();
        row.insertCell(0).textContent = i;
        row.insertCell(1).textContent = user.first_name;
        row.insertCell(2).textContent = user.last_name;
        row.insertCell(3).textContent = user.username;
        row.insertCell(4).textContent = user.phone;
        row.insertCell(5).textContent = user.email;
        row.insertCell(6).textContent = user.role;

        // Add action buttons
        const actionsCell = row.insertCell(7);
        const editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.onclick = () => openEditModal(user);
        actionsCell.appendChild(editButton);

        const deleteCell = row.insertCell(8);
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.onclick = function () {
            if (confirm("Are you sure you want to delete this user?")) {
                fetch("http://localhost:8080/api/delete-users/" + user.id)
                    .then((response) => {
                        if (response.ok) {
                            alert("User deleted successfully!");
                            fetchUsers(); // Refresh the user list
                        } else {
                            alert("Failed to delete user.");
                        }
                    })
                    .catch((error) => {
                        console.error("Error:", error);
                        alert("An error occurred while deleting the user.");
                    });
            }
        };
        deleteCell.appendChild(deleteButton);
        i++;
    });

    // Update dashboard counts
    document.getElementById("Candidate").innerHTML = data.candidate;
    document.getElementById("HR").innerHTML = data.hr;
    document.getElementById("Admin").innerHTML = data.admin;
}

// Open edit modal with user data
function openEditModal(user) {
    currentUserId = user.id;
    document.getElementById("editFirstName").value = user.first_name;
    document.getElementById("editLastName").value = user.last_name;
    document.getElementById("editUsername").value = user.username;
    document.getElementById("editPhone").value = user.phone;
    document.getElementById("editEmail").value = user.email;
    document.getElementById("editRole").value = user.role;
    editUserModal.style.display = "block";
}

// Filter users based on selected role
roleFilter.onchange = function() {
    const selectedRole = roleFilter.value.toLowerCase();
    const filteredUsers = selectedRole === "all" 
        ? users 
        : users.filter(user => user.role.toLowerCase() === selectedRole);

    populateTable(filteredUsers, {
        candidate: document.getElementById("Candidate").innerHTML,
        hr: document.getElementById("HR").innerHTML,
        admin: document.getElementById("Admin").innerHTML
    });
};


// Close edit modal
function closeEditModal() {
    editUserModal.style.display = "none";
    currentUserId = null;
}

// Handle form submission to save changes
editUserForm.onsubmit = async function (e) {
    e.preventDefault();
    const updatedUser = {
        id: currentUserId,
        first_name: document.getElementById("editFirstName").value,
        last_name: document.getElementById("editLastName").value,
        username: document.getElementById("editUsername").value,
        phone: document.getElementById("editPhone").value,
        email: document.getElementById("editEmail").value,
        role: document.getElementById("editRole").value,
    };

    try {
        const response = await fetch(
            `http://localhost:8080/api/users/${currentUserId}`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(updatedUser),
            }
        );

        if (response.ok) {
            alert("User updated successfully!");
            closeEditModal();
            fetchUsers(); // Refresh the user list
        } else {
            const errorData = await response.json();
            alert(
                "Failed to update user: " +
                    (errorData.detail || JSON.stringify(errorData))
            );
        }
    } catch (error) {
        console.error("Error updating user:", error);
        alert("Error updating user: " + error.message);
    }
};

// Filter users based on selected role
roleFilter.onchange = function() {
    const selectedRole = roleFilter.value.toLowerCase();
    const filteredUsers = selectedRole === "all" 
        ? users 
        : users.filter(user => user.role.toLowerCase() === selectedRole);

    populateTable(filteredUsers, {
        candidate: document.getElementById("Candidate").innerHTML,
        hr: document.getElementById("HR").innerHTML,
        admin: document.getElementById("Admin").innerHTML
    });
};

// Initial fetch of users
fetchUsers();
