document.addEventListener("DOMContentLoaded", () => {
    const dashboardLink = document.getElementById("dashboardLink");
    const usersLink = document.getElementById("usersLink");
    const dashboardSection = document.getElementById("dashboardSection");
    const usersSection = document.getElementById("usersSection");

    const usersTableBody = document.getElementById("dataPopulate");
    const editUserModal = document.getElementById("editUserModal");
    const editUserForm = document.getElementById("editUserForm");
    const Logout = document.getElementById("logoutBtn");

    let users = [];
    let currentUserId = null;

    // Function to show the correct section based on hash
    function showSection() {
        const hash = window.location.hash || "#dashboard"; // Default to dashboard if no hash
        if (hash === "#users") {
            dashboardSection.style.display = "none";
            usersSection.style.display = "block";
            dashboardLink.classList.remove("active");
            usersLink.classList.add("active");
        } else {
            dashboardSection.style.display = "block";
            usersSection.style.display = "none";
            dashboardLink.classList.add("active");
            usersLink.classList.remove("active");
        }
    }

    // Switch sections and update URL hash
    dashboardLink.addEventListener("click", (e) => {
        e.preventDefault();
        window.location.hash = "dashboard";
        showSection();
    });

    usersLink.addEventListener("click", (e) => {
        e.preventDefault();
        window.location.hash = "users";
        showSection();
    });

    // Listen for hash changes (e.g., back/forward navigation or refresh)
    window.addEventListener("hashchange", showSection);

    // Show the correct section on initial load
    showSection();

    // Fetch users from backend
    async function fetchUsers() {
        try {
            const url = `http://localhost:8080/api/users?t=${Date.now()}`; // Cache-busting timestamp
            const res = await fetch(url, { cache: "no-cache" });
            if (!res.ok) throw new Error("Failed to fetch users");
            users = await res.json();
            console.log("Fetched users:", users); // For debugging
            populateTable(users);
            updateDashboard(users);
        } catch (err) {
        console.error(err);
        alert("Error fetching users: " + err.message);
        }
    }

    // Populate Table
    function populateTable(users) {
        usersTableBody.innerHTML = "";
        users.forEach((user, index) => {
            const row = usersTableBody.insertRow();
            row.insertCell(0).textContent = index + 1;
            row.insertCell(1).textContent = user.first_name;
            row.insertCell(2).textContent = user.last_name;
            row.insertCell(3).textContent = user.username;
            row.insertCell(4).textContent = user.phone;
            row.insertCell(5).textContent = user.email;
            row.insertCell(6).textContent = user.role;

            const editCell = row.insertCell(7);
            const editBtn = document.createElement("button");
            editBtn.textContent = "Edit";
            editBtn.onclick = () => openEditModal(user);
            editCell.appendChild(editBtn);

            const delCell = row.insertCell(8);
            const delBtn = document.createElement("button");
            delBtn.textContent = "Delete";
            delBtn.onclick = () => deleteUser(user.id);
            delCell.appendChild(delBtn);
        });
    }

    // Update Dashboard Cards and Charts
    function updateDashboard(users) {
        const totalAdmin = users.filter(u => u.role.toLowerCase() === "admin").length;
        const totalHR = users.filter(u => u.role === "HR").length;
        const totalCandidate = users.filter(u => u.role === "Candidate").length;

        const totalAdminEl = document.getElementById("totalAdmin");
        const totalHREl = document.getElementById("totalHR");
        const totalCandidateEl = document.getElementById("totalCandidate");

        if(totalAdminEl) totalAdminEl.textContent = totalAdmin;
        if(totalHREl) totalHREl.textContent = totalHR;
        if(totalCandidateEl) totalCandidateEl.textContent = totalCandidate;

        // Destroy old pie chart if it exists
        if (window.pieChartInstance) window.pieChartInstance.destroy();

        // Pie Chart
        const ctxPieEl = document.getElementById("pieChart");
        if(ctxPieEl) {
            const ctxPie = ctxPieEl.getContext("2d");
            window.pieChartInstance = new Chart(ctxPie, {
                type: "pie",
                data: {
                    labels: ["Admin","HR","Candidate"],
                    datasets: [{
                        data: [totalAdmin, totalHR, totalCandidate],
                        backgroundColor: ["#205072","#329D9C","#7BE495"]
                    }]
                }
            });
        }
    }

    // Edit Modal
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

    function closeEditModal() {
        editUserModal.style.display = "none";
        currentUserId = null;
    }

    editUserForm.onsubmit = async (e) => {
        e.preventDefault();
        const updatedUser = {
            first_name: document.getElementById("editFirstName").value,
            last_name: document.getElementById("editLastName").value,
            username: document.getElementById("editUsername").value,
            phone: document.getElementById("editPhone").value,
            email: document.getElementById("editEmail").value,
            role: document.getElementById("editRole").value
        };

        try {
            const res = await fetch(`http://localhost:8080/api/users/${currentUserId}`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(updatedUser)
            });
            if (res.ok) {
                alert("User updated successfully!");
                closeEditModal();
                fetchUsers();
                console.log("Update successful, refetching users"); // Added for debugging
            } else {
                alert("Failed to update user");
                console.error("Update failed with status:", res.status); // Added for debugging
            }
        } catch (err) {
            console.error(err);
            alert("Error updating user: " + err.message);
        }
    };

    // Delete user
    async function deleteUser(id) {
        if (confirm("Are you sure to delete this user?")) {
            try {
                const res = await fetch(`http://localhost:8080/api/users/${id}`, 
                    { method: "DELETE" });
                if (res.ok) {
                    alert("User deleted successfully!");
                    fetchUsers();
                } else {
                    alert("Failed to delete user");
                }
            } catch (err) {
                console.error(err);
                alert("Error deleting user: " + err.message);
            }
        }
    }

    Logout.addEventListener("click", () => {
        window.location.href = "/frontend/login_page/login.html";
    });

    // Initial fetch
    fetchUsers();
});