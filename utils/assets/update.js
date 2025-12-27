async function updateproject() {
    const proj = document.getElementById("updateprojectId").value.trim();
    if (!proj) {
        alert("Please enter a project ID");
        return;
    }

    try {
        const response = await fetch("http://localhost:4000/pull/populate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ project_id: proj })
        });

        const resp = await response.json();
        if (!response.ok) throw new Error(resp.detail);

        // Populate INPUT fields
        document.getElementById("updateprojectTitle").value = resp.project.title;
        document.getElementById("updateprojectCustomer").value = resp.project.customer;
        document.getElementById("updateOrg").value = resp.project.organization;

        document.getElementById("updateSampletype").value = resp.sample.type;
        document.getElementById("updatesampleNos").value = resp.sample.count;
        document.getElementById("updateSamplepreservation").value = resp.sample.preservation;
        document.getElementById("updateSampleinfo").value = resp.sample.other_info;

        document.getElementById("updateMethod").value = resp.method.name;
        document.getElementById("updatemethodWritup").value = resp.method.writeup;
        document.getElementById("updatemethodSummary").value = resp.method.method_summary;

        document.getElementById("qcSummary").value = resp.qc.qc_summary;
        document.getElementById("libMethod").value = resp.library.lib_method;
        document.getElementById("lib_Summary").value = resp.library.library_summary;

        document.getElementById("updatedBy").value = resp.audit.updated_by;
        document.getElementById("updateDate").value = resp.audit.updated_date;

        // Show existing files
        setupFileInfo("quantitationQcInfo", resp.qc.qc_files.quantification);
        setupFileInfo("integrityQcInfo", resp.qc.qc_files.integrity);
        setupFileInfo("libReportInfo", resp.library.library_files.report);
        setupFileInfo("libTapeInfo", resp.library.library_files.tapestation_report);

    } catch (err) {
        console.error(err);
        alert("Project not found");
    }
}


function setupFileInfo(elementId, path) {
    const el = document.getElementById(elementId);
    if (!path) return;

    const fileName = path.split("/").pop();

    el.innerHTML = `
        Existing file:
        <strong>${fileName}</strong>
        |
        <a href="http://localhost:4000/download?path=${encodeURIComponent(path)}" target="_blank">
            View / Download
        </a>
    `;
}


async function submitUpdate() {
    const formData = new FormData();

    formData.append("project_id", document.getElementById("updateprojectId").value);
    formData.append("title", document.getElementById("updateprojectTitle").value);

    const qcFile = document.getElementById("quantitationQc").files[0];
    if (qcFile) formData.append("quantification", qcFile);

    const intFile = document.getElementById("integrityQc").files[0];
    if (intFile) formData.append("integrity", intFile);

    const libFile = document.getElementById("libReport").files[0];
    if (libFile) formData.append("lib_report", libFile);

    const tapeFile = document.getElementById("libTapeReport").files[0];
    if (tapeFile) formData.append("lib_tape", tapeFile);

    await fetch("http://localhost:4000/update/submit", {
        method: "POST",
        body: formData
    });

    alert("Updated successfully");
}
