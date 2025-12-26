from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "/home/akshay/Projects/theraCUESDB"
os.makedirs(UPLOAD_DIR, exist_ok= True)

CLIENT = MongoClient("mongodb://localhost:27017")
db = CLIENT.theraCUES
collection = db['projects']


@app.post('/submit')
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






