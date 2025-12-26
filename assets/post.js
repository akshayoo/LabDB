document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const submitBtn = form.querySelector("button[type='submit']");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        submitBtn.disabled = true;

        const formData = new FormData(form);

        try {
            const response = await fetch("http://localhost:4000/submit", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error("Server not founde");
            }

            const result = await response.json();
            console.log("Success:", result);

            alert(`Database entry created successfully for Project ID: ${result.project_id}\nMongo ID: ${result.mongo_id}`);

        } catch (error) {
            console.error("Error:", error);
            alert("Submission failed........");

        } finally {
            submitBtn.disabled = false;
        }
    });
});



