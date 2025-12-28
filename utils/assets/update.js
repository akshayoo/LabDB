async function updateproject() {
    const proj_Id = document.getElementById("updateprojectId").value.trim();

    if (!proj_Id) {
        alert("Please enter a project Id");
        return;
    }

    try {
        const req = await fetch("http://localhost:4000/update/populate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ project_id: proj_Id })
        });

        const response = await req.json();

        if (!req.ok) {
            throw new Error(response.message || "Project ID not found");
        }

        function setVal(id, val) {
            const el = document.getElementById(id);
            if (!el) return;
            el.value = val ?? "";
        }


        setVal("updateprojectTitle", response.project?.title);
        setVal("updateprojectCustomer", response.project?.customer);
        setVal("updateOrg", response.project?.organization);

        setVal("updateSampletype", response.sample?.type);
        setVal("updatesampleNos", response.sample?.count);
        setVal("updateSamplepreservation", response.sample?.preservation);
        setVal("updateSampleinfo", response.sample?.other_info);

        setVal("updateMethod", response.method?.name);
        setVal("updatemethodWritup", response.method?.writeup);
        setVal("updatemethodSummary", response.method?.method_summary);

        setVal("qcSummary", response.qc?.qc_summary);

        setVal("libMethod", response.library?.lib_method);
        setVal("lib_Summary", response.library?.library_summary);

        setFileLink(
            "quantitationQcInfo",
            response.qc?.qc_files?.quantification
        );

        setFileLink(
            "integrityQcInfo",
            response.qc?.qc_files?.integrity
        );

        setFileLink(
            "libReportInfo",
            response.library?.library_files?.report
        );

        setFileLink(
            "libTapeInfo",
            response.library?.library_files?.tapestation_report
        );

    } catch (error) {
        console.error("Req not sent", error.message);
        alert(error.message);
    }
}


function setFileLink(pId, filePath) {
    const p = document.getElementById(pId);
    if (!p) return;

    p.innerHTML = "";

    if (!filePath) {
        p.textContent = "No file uploaded";
        return;
    }

    const fileName = filePath.split("/").pop() || "Download to vie file";

    const link = document.createElement("a");
    link.href = filePath;
    link.textContent = fileName;
    link.download = "";
    link.target = "_blank";

    p.appendChild(link);
}


async function submitUpdate() {
    const projectId = document.getElementById("updateprojectId").value.trim();

    if (!projectId) {
        alert("Project ID missing");
        return;
    }

    const formData = new FormData();

    formData.append("project_id", projectId);

    formData.append("title", document.getElementById("updateprojectTitle").value);
    formData.append("customer", document.getElementById("updateprojectCustomer").value);
    formData.append("organization", document.getElementById("updateOrg").value);

    formData.append("updated_by", document.getElementById("updatedBy").value);
    formData.append("updated_date", document.getElementById("updateDate").value);

    formData.append("sam_type", document.getElementById("updateSampletype").value);
    formData.append("count", document.getElementById("updatesampleNos").value);
    formData.append("preservation", document.getElementById("updateSamplepreservation").value);
    formData.append("other_info", document.getElementById("updateSampleinfo").value);

    formData.append("method_name", document.getElementById("updateMethod").value);
    formData.append("writeup", document.getElementById("updatemethodWritup").value);
    formData.append("method_summary", document.getElementById("updatemethodSummary").value);

    formData.append("qc_summary", document.getElementById("qcSummary").value);

    formData.append("lib_method", document.getElementById("libMethod").value);
    formData.append("lib_summary", document.getElementById("lib_Summary").value);

    const quant = document.getElementById("quantitationQc").files[0];
    const integ = document.getElementById("integrityQc").files[0];
    const libRep = document.getElementById("libReport").files[0];
    const libTape = document.getElementById("libTapeReport").files[0];

    if (quant) formData.append("quantification", quant);
    if (integ) formData.append("integrity", integ);
    if (libRep) formData.append("lib_report", libRep);
    if (libTape) formData.append("lib_tape", libTape);

    try {
        const res = await fetch("http://localhost:4000/update/submit", {
            method: "POST",
            body: formData   
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "Update failed");
        }

        alert(`Project ${projectId} updated successfully!`);

    } catch (err) {
        console.error(err);
        alert(err.message);
    }
    window.location.reload();
}

