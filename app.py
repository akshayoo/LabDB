from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "/home/akshay/Projects/theraCUESDB"
os.makedirs(UPLOAD_DIR, exist_ok=True)

CLIENT = MongoClient("mongodb://localhost:27017")
db = CLIENT.theraCUES
collection = db["projects"]

BASE_URL = "http://localhost:4000"

ALLOWED_BASE = "/home/akshay/Projects/theraCUESDB"





 #__________________________________#
#________________PUSH________________#



@app.post('/push/submit')
async def submit_form(
    updated_by : str = Form(...),
    updated_date : str = Form(...),
    project_id : str = Form(...),
    title : str = Form(...),
    customer : str = Form(...),
    organization : str = Form(...),
    sam_type : str = Form(...),
    count : int = Form(...),
    preservation : str = Form(...),
    other_info : str = Form(...),
    name : str = Form(...),
    writeup : str = Form(...),
    method_summary : str = Form(...),
    quantification : UploadFile = File(...),
    integrity : UploadFile = File(...),
    qc_summary : str = Form(...),
    lib_method : str = Form(...),
    lib_report : UploadFile = File(...),
    lib_tape : UploadFile = File(...),
    lib_summary : str = Form(...)

):
    project_dir = f"{UPLOAD_DIR}/{project_id}"
    os.makedirs(project_dir, exist_ok=True)
    
    qc_report_dir = f"{project_dir}/QC"
    lib_report_dir = f"{project_dir}/LIB"

    os.makedirs(qc_report_dir, exist_ok= True)
    os.makedirs(lib_report_dir, exist_ok= True)

    qcQuant_reportPath = f"{qc_report_dir}/{quantification.filename}"
    qcInt_reportPath = f"{qc_report_dir}/{integrity.filename}"

    lib_reportPath = f"{lib_report_dir}/{lib_report.filename}"
    libTape_reportPath = f"{lib_report_dir}/{lib_tape.filename}"
    
    with open (qcQuant_reportPath, 'wb') as f:
        f.write(await quantification.read())

    with open (qcInt_reportPath, 'wb') as f:
        f.write(await integrity.read())

    with open (lib_reportPath, 'wb') as f:
        f.write(await lib_report.read())

    with open (libTape_reportPath, 'wb') as f:
        f.write(await lib_tape.read())

    document = {
        "project": {
        "project_id": project_id,
        "title": title,
        "customer": customer,
        "organization": organization
        },

        "sample": {
            "type": sam_type,
            "count": count,
            "preservation": preservation,
            "other_info": other_info
        },

        "method": {
            "name": name,
            "writeup": writeup,
            "method_summary": method_summary
        },

        "qc": {
            "qc_summary": qc_summary,
            "qc_files": {
                "quantification": qcQuant_reportPath,
                "integrity": qcInt_reportPath
            }
        },

        "library": {
            "lib_method" : lib_method, 
            "library_summary" : lib_summary,
            "library_files" : {
                "report": lib_reportPath,
                "tapestation_report": libTape_reportPath
            }
        },

        "audit": {
            "updated_by": updated_by,
            "updated_date": updated_date
        },
    }

    add_data = collection.insert_one(document)
    ins_id = add_data.inserted_id

    document["_id"] = str(ins_id)

    metadataJsonPath = f"{project_dir}/metadata.json"

    with open(metadataJsonPath, "w", encoding="utf-8") as f:
        json.dump(document, f, indent=2)

    await quantification.close()
    await integrity.close()
    await lib_report.close()
    await lib_tape.close()

    return {
        "status": "success",
        "project_id": project_id,
        "mongo_id": str(ins_id)
    }





 #__________________________________#
#________________PULL________________#



class ProjectRequest(BaseModel):
    project_id: str

@app.post("/pull/populate")
async def pull_populate(data: ProjectRequest):

    project_inf = collection.find_one({
        "project.project_id": data.project_id
    })

    if not project_inf:
        raise HTTPException(status_code=404, detail="Project not found")

    project_inf["_id"] = str(project_inf["_id"])
    return project_inf


@app.get("/pull/download")
async def download_file(path: str):

    abs_path = os.path.abspath(path)
    base = os.path.abspath(ALLOWED_BASE)

    if not abs_path.startswith(base + os.sep):
        raise HTTPException(status_code=403, detail="Access denied")

    if not os.path.exists(abs_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        abs_path,
        filename=os.path.basename(abs_path),
        media_type="application/octet-stream"
    )





 #__________________________________#   
#________________UPDATE________________#



@app.post("/update/populate")
async def update_populate(data: ProjectRequest):
    project_inf = collection.find_one(
        {"project.project_id": data.project_id},
        {"_id": 0} 
    )

    if not project_inf:
        raise HTTPException(status_code=404, detail="Project not found")

    return project_inf


@app.post("/update/submit")
async def update_submit(
    project_id: str = Form(...),

    title: str = Form(...),
    customer: str = Form(...),
    organization: str = Form(...),

    updated_by: str = Form(...),
    updated_date: str = Form(...),

    sam_type: str = Form(...),
    count: int = Form(...),
    preservation: str = Form(...),
    other_info: str = Form(...),

    method_name: str = Form(...),
    writeup: str = Form(...),
    method_summary: str = Form(...),

    qc_summary: str = Form(...),

    lib_method: str = Form(...),
    lib_summary: str = Form(...),

    quantification: UploadFile | None = File(None),
    integrity: UploadFile | None = File(None),
    lib_report: UploadFile | None = File(None),
    lib_tape: UploadFile | None = File(None),
):
    project = collection.find_one({"project.project_id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project_dir = f"{UPLOAD_DIR}/{project_id}"
    qc_dir = f"{project_dir}/QC"
    lib_dir = f"{project_dir}/LIB"

    os.makedirs(qc_dir, exist_ok=True)
    os.makedirs(lib_dir, exist_ok=True)

    update_doc = {
        "project.title": title,
        "project.customer": customer,
        "project.organization": organization,

        "sample.type": sam_type,
        "sample.count": count,
        "sample.preservation": preservation,
        "sample.other_info": other_info,

        "method.name": method_name,
        "method.writeup": writeup,
        "method.method_summary": method_summary,

        "qc.qc_summary": qc_summary,

        "library.lib_method": lib_method,
        "library.library_summary": lib_summary,

        "audit.updated_by": updated_by,
        "audit.updated_date": updated_date,
    }

    if quantification:
        qcQuant_path = f"{qc_dir}/{quantification.filename}"
        with open(qcQuant_path, "wb") as f:
            f.write(await quantification.read())

        update_doc["qc.qc_files.quantification"] = qcQuant_path

    if integrity:
        qcInt_path = f"{qc_dir}/{integrity.filename}"
        with open(qcInt_path, "wb") as f:
            f.write(await integrity.read())

        update_doc["qc.qc_files.integrity"] = qcInt_path

    if lib_report:
        libRep_path = f"{lib_dir}/{lib_report.filename}"
        with open(libRep_path, "wb") as f:
            f.write(await lib_report.read())

        update_doc["library.library_files.report"] = libRep_path

    if lib_tape:
        libTape_path = f"{lib_dir}/{lib_tape.filename}"
        with open(libTape_path, "wb") as f:
            f.write(await lib_tape.read())

        update_doc["library.library_files.tapestation_report"] = libTape_path

    collection.update_one(
        {"project.project_id": project_id},
        {"$set": update_doc}
    )

    return {"status": "success", "project_id": project_id}
