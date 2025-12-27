async function pullByID() {
    const projID = document.getElementById("updateprojectId").value.trim();

    if (!projID) {
        alert("Please enter a Project ID");
        return;
    }

    try {
        const response = await fetch("http://localhost:4000/pull/populate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ project_id: projID })
        });

        const resp = await response.json();

        if (!response.ok) {
            throw new Error(resp.message || "Project ID not found");
        }

        const setText = (id, val) =>
            document.getElementById(id).textContent = val ?? "No data";

        setText("project_id", resp.project.project_id);
        setText("title", resp.project.title);
        setText("customer", resp.project.customer);
        setText("organization", resp.project.organization);

        setText("sam_type", resp.sample.type);
        setText("count", resp.sample.count);
        setText("preservation", resp.sample.preservation);
        setText("other_info", resp.sample.other_info);

        setText("method_name", resp.method.name);
        setText("method_writeup", resp.method.writeup);
        setText("method_summary", resp.method.method_summary);

        setText("qc_summary", resp.qc.qc_summary);

        setText("lib_method", resp.library.lib_method);
        setText("lib_summary", resp.library.library_summary);

        setText("updated_by", resp.audit.updated_by);
        setText("updated_date", resp.audit.updated_date);
        const setupBtn = (id, path) => {
            const btn = document.getElementById(id);
            if (path) {
                btn.dataset.path = path;
                btn.disabled = false;
            }
        };

        setupBtn("qc_quant_btn", resp.qc.qc_files.quantification);
        setupBtn("qc_integrity_btn", resp.qc.qc_files.integrity);
        setupBtn("lib_report_btn", resp.library.library_files.report);
        setupBtn("lib_tape_btn", resp.library.library_files.tapestation_report);

    } catch (error) {
        console.error("Server error:", error);
        alert("Please check the server");
    }
}

function downloadFile(buttonId) {
    const btn = document.getElementById(buttonId);
    const path = btn?.dataset.path;

    if (!path) {
        alert("File path missing");
        return;
    }

    const url =
        `http://localhost:4000/pull/download?path=${encodeURIComponent(path)}`;

    window.open(url, "_blank");
}
