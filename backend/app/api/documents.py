import fitz
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/api/documents", tags=["Documents"])

MAX_FILE_SIZE = 10 * 1024 * 1024

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
	if not file.filename:
		raise HTTPException(
			status_code=400,
			detail="Failename is required."
		)

	extension = file.filename.rsplit(".", 1)[-1].lower()

	if extension not in ["pdf", "txt"]:
		raise HTTPException(
			status_code=400,
			detail="Only PDF and TXT files are supported."
		)


	content = await file.read(MAX_FILE_SIZE + 1)

	if len(content) > MAX_FILE_SIZE:
		raise HTTPException(
			status_code=413,
			detail="File exceeds the 10MB limit."
		)


	if not content:
		raise HTTPException(
			status_code=400,
			detail="The uploaded file is empty"
		)


	try:
		if extension == "pdf":
			if not content.startswith(b"%PDF-"):
				raise HTTPException(
					status_code=400,
					detail="Invalid PDF file."
				)

			with fitz.open(stream=content, filetype="pdf") as document:
				text = "\n".join(page.get_text() for page in document)
				pages = document.page_count


		else:
			text = content.decode("utf-8-sig")
			pages = None


	except UnicodeDecodeError:
		raise HTTPException(
			status_code=400,
			detail="TXT files must be UTF-8 encoding."
		)


	except HTTPException:
		raise


	except Exception as error:
		raise HTTPException(
			status_code=400,
			detail=f"Document processing failed: {str(error)}"
		)

	text = text.strip()

	if not text:
		raise HTTPException(
			status_code=400,
			detail="No extractable text found in this document"
		)

	return {
		"success": True,
		"filename": file.filename,
		"file_type": extension,
		"pages": pages,
		"character_count": len(text),
		"text": text
	}
