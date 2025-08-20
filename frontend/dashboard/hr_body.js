let selectedCV = [];

document.addEventListener("DOMContentLoaded", function () {
//all codes
});

// ------------------ File Upload ------------------
document.getElementById("upload-form").addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior

    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch("http://localhost:8080/api/hr-upload/", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);
            return;
        }

        await response.json();
        alert("File uploaded successfully");
    } catch (error) {
        console.error("Error submitting form:", error);
        alert("Failed to upload file. Please try again.");
    }
});


// ------------------ Analyze Existing Resumes ------------------
document.getElementById("analyze_existing").addEventListener("click", async function () {
    const matching_table = document.getElementById("cv-matching-table-body");
    matching_table.innerHTML = "";
    document.getElementById("loading11").style.display = "block";

    try {
        const response = await fetch("http://localhost:8080/api/hr-resumes-sort", {
            method: "GET", // ✅ must match backend
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);
            return;
        }

        const result = await response.json();

        document.getElementById("table12").style.display = "block";
        document.getElementById("loading11").style.display = "none";

        let rowID = 0;
        for (let [key, value] of Object.entries(result.data)) {  // ✅ backend returns "data"
            const newRow = document.createElement("tr");
            const id = "row" + rowID;
            newRow.setAttribute("id", id);

            const td1 = document.createElement("td");
            td1.textContent = key;
            selectedCV.push(key);

            const td2 = document.createElement("td");
            td2.textContent = value + '%';

            const td3 = document.createElement("td");
            td3.innerHTML = `
                <button style="padding: 8px 16px; font-size: 14px; cursor: pointer; border: none; border-radius: 4px; background-color: #f44336; color: white; transition: background-color 0.3s ease;" 
                        onmouseover="this.style.backgroundColor='#d32f2f'" 
                        onmouseout="this.style.backgroundColor='#f44336'" 
                        onclick="rowDelete('${id}', '${key}')">Delete</button>
            `;

            newRow.appendChild(td1);
            newRow.appendChild(td2);
            newRow.appendChild(td3);

            matching_table.appendChild(newRow);
            rowID++;
        }
    } catch (error) {
        console.error("Error submitting form:", error);
        alert("Failed to analyze resumes. Please try again.");
    }
});


// ------------------ Delete Row ------------------
function rowDelete(rowID, cvName) {
    const row = document.getElementById(rowID);
    if (row) row.remove();

    // Remove from selectedCV array
    selectedCV = selectedCV.filter(item => item !== cvName);
    console.log("Updated selectedCV:", selectedCV);
}


// ------------------ Extract Resume Info ------------------
document.getElementById("extract_trig").addEventListener("click", async function () {
    console.log("Selected CVs:", JSON.stringify(selectedCV));

    try {
        const response = await fetch("http://localhost:8080/api/extract_resume_info", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(selectedCV),
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData}`);
            return;
        }

        const result = await response.json();
        console.log("Extracted Resume Info:", result);

        sessionStorage.setItem('resultData', JSON.stringify(result));
        alert("Information extracted successfully!");
    } catch (error) {
        console.error("Error submitting form:", error);
        alert("Failed to extract resume info. Please try again.");
    }
});


// ------------------ Extract Info via Button ------------------
document.querySelector('button[name="action"][value="extract_info"]').addEventListener('click', async () => {
    try {
        // Fetch filenames from the server
        const filenamesResponse = await fetch('http://localhost:8080/api/extract_resume_info/', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify([])  // send empty body if backend doesn't need input
        });

        const filenamesData = await filenamesResponse.json();

        if (filenamesData.error) {
            console.error("Error fetching filenames:", filenamesData.error);
            alert("Failed to retrieve resume filenames.");
            return;
        }

        const fileNames = filenamesData.filenames;

        // Send filenames to extract_resume_info API
        const response = await fetch('http://localhost:8080/api/extract_resume_info/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(fileNames)
        });

        if (!response.ok) throw new Error(`Failed to extract resume info: ${response.status}`);

        const data = await response.json();
        console.log("Extracted Resume Info:", data);

        document.getElementById("resumeResult").innerHTML = "<pre>" + JSON.stringify(data, null, 2) + "</pre>";

        alert("All information extracted and saved.");
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to extract information. Please try again.");
    }
});


// ------------------ Generate Questions ------------------
document.getElementById("generateQuestion").addEventListener("click", async function () {
    const loading = document.getElementById("loading11");
    const loadingMessage = document.getElementById("loadingMessage");
    const progressFill = document.getElementById("progressFill");

    loading.style.display = "block";
    loadingMessage.innerHTML = "Generating Questions...";
    loadingMessage.style.fontSize = "20px";
    loadingMessage.style.fontWeight = "bold";

    try {
        const response = await fetch("http://localhost:8080/api/generate-hr-questions", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.message || "Generating Questions"}`);
        } else {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let result = "";
            let done = false;

            while (!done) {
                const { value, done: readerDone } = await reader.read();
                done = readerDone;
                result += decoder.decode(value, { stream: true });

                if (result.includes("data:")) {
                    const progressMatch = result.match(/data: (\d+)/);
                    if (progressMatch) {
                        const progress = parseInt(progressMatch[1], 10);
                        progressFill.style.width = progress + "%";
                        loadingMessage.innerHTML = `Generated: ${progress}%`;
                    }
                }
            }

            console.log("Questions generated:", result);
            alert("Questions generated successfully!");
        }
    } catch (error) {
        console.error("Error generating questions:", error);
        alert("Failed to generate questions. Please make sure the server is running.");
    } finally {
        loading.style.display = "none";
    }
});

// ------------------ Save Selected CVs Individually ------------------
    const saveBtn = document.getElementById("save_btn");
    if (saveBtn) {
        saveBtn.addEventListener("click", async function () {
            if (selectedCV.length === 0) {
                alert("No CVs selected to save!");
                return;
            }

            try {
                for (let cvName of selectedCV) {
                    const link = document.createElement("a");
                    link.href = `http://localhost:8080/api/download_cv/${encodeURIComponent(cvName)}`;
                    link.download = cvName;
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                }
                alert("Selected CVs downloaded successfully!");
            } catch (error) {
                console.error("Error saving CVs:", error);
                alert("Failed to save CVs. Please try again.");
            }
        });
    }


