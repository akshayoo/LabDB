document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("pushForm");

    form.addEventListener("submit", async (e) => {
        e.preventDefault(); 

        const formData = new FormData(form);

        try {
            const response = await fetch("http://localhost:4000/push/submit", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.message || "Submission failed");
            }

            alert("Project data uploaded successfully \n");
            form.reset();

        } catch (error) {
            console.error("Upload error:", error);
            alert("Error uploading data\n" + error.message);
        }
    });
});





