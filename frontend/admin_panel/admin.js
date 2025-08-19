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

    // Switch sections
    dashboardLink.addEventListener("click", () => {
        dashboardSection.style.display = "block";
        usersSection.style.display = "none";
        dashboardLink.classList.add("active");
        usersLink.classList.remove("active");
    });

    usersLink.addEventListener("click", () => {
        dashboardSection.style.display = "none";
        usersSection.style.display = "block";
        dashboardLink.classList.remove("active");
        usersLink.classList.add("active");
    });

    // Fetch users from backend
    async function fetchUsers() {
        try {
            const res = await fetch("http://localhost:8080/api/users");
            if (!res.ok) throw new Error("Failed to fetch users");
            users = await res.json();
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
        const totalAdmin = users.filter(u => u.role === "admin").length;
        const totalHR = users.filter(u => u.role === "HR").length;
        const totalCandidate = users.filter(u => u.role === "Candidate").length;

        const totalAdminEl = document.getElementById("totalAdmin");
        const totalHREl = document.getElementById("totalHR");
        const totalCandidateEl = document.getElementById("totalCandidate");

        if(totalAdminEl) totalAdminEl.textContent = totalAdmin;
        if(totalHREl) totalHREl.textContent = totalHR;
        if(totalCandidateEl) totalCandidateEl.textContent = totalCandidate;

        // Destroy old charts if they exist
        if (window.barChartInstance) window.barChartInstance.destroy();
        if (window.pieChartInstance) window.pieChartInstance.destroy();
        if (window.lineChartInstance) window.lineChartInstance.destroy();

        // Bar Chart
        const ctxBarEl = document.getElementById("barChart");
        if(ctxBarEl) {
            const ctxBar = ctxBarEl.getContext("2d");
            window.barChartInstance = new Chart(ctxBar, {
                type: "bar",
                data: {
                    labels: ["Admin", "HR", "Candidate"],
                    datasets: [{
                        label: "Users",
                        data: [totalAdmin, totalHR, totalCandidate],
                        backgroundColor: ["#205072","#329D9C","#7BE495"]
                    }]
                }
            });
        }

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

        // Line Chart - Monthly User Growth by Role
        const ctxLineEl = document.getElementById("lineChart");
        if(ctxLineEl) {
            const growthData = { Admin: {}, HR: {}, Candidate: {} };

            // Aggregate monthly counts with normalized role
            users.forEach(u => {
                if (u.created_at && u.role) {
                    const roleKey = u.role.toLowerCase() === "admin" ? "Admin" :
                                    u.role.toLowerCase() === "hr" ? "HR" :
                                    u.role.toLowerCase() === "candidate" ? "Candidate" :
                                    null;
                    if (!roleKey) return; // skip unknown roles

                    const date = new Date(u.created_at);
                    const monthKey = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}`;

                    if (!growthData[roleKey][monthKey]) growthData[roleKey][monthKey] = 0;
                    growthData[roleKey][monthKey]++;
                }
            });

            // Get all months sorted
            const allMonthsSet = new Set([
                ...Object.keys(growthData.Admin),
                ...Object.keys(growthData.HR),
                ...Object.keys(growthData.Candidate)
            ]);
            const allMonths = Array.from(allMonthsSet).sort();

            // Counts for each role
            const adminCounts = allMonths.map(m => growthData.Admin[m] || 0);
            const hrCounts = allMonths.map(m => growthData.HR[m] || 0);
            const candidateCounts = allMonths.map(m => growthData.Candidate[m] || 0);

            const ctxLine = ctxLineEl.getContext("2d");
            window.lineChartInstance = new Chart(ctxLine, {
                type: "line",
                data: {
                    labels: allMonths,
                    datasets: [
                        { label: "Admin", data: adminCounts, borderColor: "#205072", fill: false, tension: 0.1 },
                        { label: "HR", data: hrCounts, borderColor: "#329D9C", fill: false, tension: 0.1 },
                        { label: "Candidate", data: candidateCounts, borderColor: "#7BE495", fill: false, tension: 0.1 }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: 'top' } },
                    scales: {
                        x: { title: { display: true, text: 'Month' } },
                        y: { title: { display: true, text: 'Number of Users' }, beginAtZero: true }
                    }
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
            } else {
                alert("Failed to update user");
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
