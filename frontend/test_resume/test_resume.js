async function submitForm() {
  const jobDesc = document.querySelector('textarea[name="job_desc"]').value;
  const resumeFile = document.querySelector('input[name="resume"]').files[0];

  // Create a FormData object and append data
  const formData = new FormData();
  formData.append("job_desc", jobDesc);
  formData.append("resume", resumeFile);
  formData.append("action", "submit");

  // Send the request with fetch
  try {
    const response = await fetch("http://localhost:8080/api/candidate-upload/", {
      method: "POST",
      body: formData,
    });

    // Check if the request was successful
    if (response.ok) {
      document.getElementById("analyzeButton").disabled = false;
      document.getElementById("generateButton").disabled = false;
      alert(
        "Files uploaded successfully. You can now analyze the resume or generate questions."
      );
    } else {
      alert("File upload failed. " + response.statusText);
    }
  } catch (error) {
    loadingIndicator.style.display = "none"; // Hide loading indicator
    console.error("Error uploading files:", error);
    alert("An error occurred during file upload.");
  }
}
async function analyzeResume() {
  const loading = document.getElementById("loading");
  const container = document.getElementById("container");

  loading.style.display = "block";
  container.style.display = "none";
  try {
    const response = await fetch("http://localhost:8080/api/candidate-resume-process", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });


    const data = await response.json();

    if (response.ok) {
      // Show a success alert
      // alert("Resume analysis successful");
      // var text = JSON.stringify(data.response);
      var text = data.data;
      // text = text.replace(/\\n/g, "<br>");
      // text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
      // text = text.replace(/\*(.*?)\*/g, "<em>$1</em>");
      // text = text.replace(/__(.*?)__/g, "<u>$1</u>");
      // text = text.replace('"', " ");
      // text = text.replace(/\\"/g, ' " ');
      var text = data.data;

      console.log(text);


      // Headings (## Heading)
      text = text.replace(/^## (.*?)$/gm, "<h2 style='margin-top:15px;'>$1</h2>");

      // Subheadings (### Heading)
      text = text.replace(/^### (.*?)$/gm, "<h3 style='margin-top:10px;'>$1</h3>");

      // // Bold text
      // text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

      // // Remove single asterisks (for list points)
      // text = text.replace(/^\* (.*)/gm, "<li>$1</li>");

      // Wrap <li> groups inside <ul>
      text = text.replace(/(<li>.*<\/li>)/gs, "<ul>$1</ul>");

      // Underline text
      text = text.replace(/__(.*?)__/g, "<u>$1</u>");

      // Line breaks (but avoid breaking inside <li>)
      text = text.replace(/\n(?!<li>)/g, "<br>");

      // Clean escaped quotes
      text = text.replace(/\\"/g, '"');

      // 1. Bold text with double asterisks (keep as <strong>)
      text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

      // 2. Triple asterisks or more → remove only the first one
      text = text.replace(/^\s*\*{3,}\s*/gm, "");

      // 3. Single asterisk (bullet points) → remove it
      text = text.replace(/^\s*\*\s*/gm, "");

      // Dynamically display the result on the frontend
      const resultContainer = document.getElementById("resultContent");
      resultContainer.innerHTML = `
        <h3>Resume Analysis Result:</h3>
        <p class="p-10">${text}</p>
      `;

      loading.style.display = "none";
      document.getElementById("resultPanel").style.display = "block";
    } else {
      // Handle API errors
      alert(`Resume analysis failed: ${data.detail}`);
    }
  } catch (error) {
    // Handle network or other unexpected errors
    alert("An error occurred while analyzing the resume");
    console.error(error);
  }
}

function generateQuestions() {
  // Displaying simulated questions for testing
  const resultPanel = document.getElementById("resultPanel");
  const resultContent = document.getElementById("resultContent");

  resultPanel.style.display = "block";
  resultContent.textContent =
    "Generated Questions:\n1. What are your strengths?\n2. Describe your experience with similar roles.\n3. How would you contribute to our team?";
}

function loginPage() {
  window.location.href = "/frontend/login_page/login.html";
}

// document.addEventListener("DOMContentLoaded", function () {
//   document.getElementById("loginButton").onclick = function () {
//     window.location.href = "/frontend/login_page/login.html";
//   };
// });
