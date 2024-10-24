from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import soundfile as sf
import shutil

import uvicorn
from typing import Annotated, List
from sqlalchemy.orm import Session

from core.manager import get_db, UserBase, UserResp, UserListResp, \
    ArtBase, ArtResp, create_art, create_user, get_arts_by_user, get_users
from core.schema import User, Art

from sd.gen import gen_image
from stt.speech import from_file, from_stream
from stt.summary import summarize

app = FastAPI()

# React app url
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.post("/users/", response_model=UserResp)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.name == user.name).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    # Create new user
    user = create_user(db, name=user.name)
    return {"id": user.id, "name": user.name, "date": user.date, "arts": []}

# Endpoint to create a new art entry for a specific user
@app.post("/users/{user_name}/arts/", response_model=ArtResp)
def create_art(user_name: str, art_data: ArtBase, db: Session = Depends(get_db)):
    # Find user by name
    user = db.query(User).filter(User.name == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create new art for the user
    art = create_art(db, user_id=user.id, prompt=art_data.prompt, summary=art_data.summary, image=art_data.image)
    return {
        "id": art.id,
        "prompt": art.prompt,
        "summary": art.summary,
        "image": art.image,
        "date": art.date,
        "timestamp": art.timestamp
    }

@app.get("/users/{user_name}/", response_model=UserResp)
def get_user_arts(user_name: str, db: Session = Depends(get_db)):
    user_with_arts = get_arts_by_user(db, user_name)
    if not user_with_arts:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user_with_arts["user"].id,
        "name": user_with_arts["user"].name,
        "date": user_with_arts["user"].date,
        "arts": [
            {
                "id": art.id,
                "prompt": art.prompt,
                "summary": art.summary,
                "image": art.image,
                "date": art.date,
                "timestamp": art.timestamp
            } for art in user_with_arts["arts"]
        ]
    }

@app.get("/users/", response_model=List[UserListResp])
def list_users(db: Session = Depends(get_db)):
    users = get_users(db)
    return [{"id": user.id, "name": user.name, "date": user.date} for user in users]

# Endpoint to delete an art record for a specific user
@app.delete("/users/{user_name}/arts/{art_id}")
def delete_art(user_name: str, art_id: int, db: Session = Depends(get_db)):
    # Find user by name
    user = db.query(User).filter(User.name == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Find the art record by id for the user
    art = db.query(Art).filter(Art.id == art_id, Art.user_id == user.id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Art not found for the specified user")

    # Delete the art record
    db.delete(art)
    db.commit()
    
    return {"message": "Art record deleted successfully"}


async def transcript_audio(file: UploadFile = File(...)):
    # Read the uploaded audio file
    audio_data, samplerate = sf.read(file.file)

    # Initialize the Vosk recognizer with the correct sample rate
    # recognizer = vosk.KaldiRecognizer(model, samplerate)

    # Run the recognizer on the audio data (expects 16-bit PCM data)
    # recognizer.AcceptWaveform(audio_data.tobytes())

    # Get the final result (full transcript)
    # result = json.loads(recognizer.FinalResult())

    # return {"transcript": result.get("text", "")}

@app.post("/visualize/")
async def visualize(file: UploadFile = File(...)):
    db_dependency = Annotated[Session, Depends(get_db)]
    use_image = False

    try:
       # Log the uploaded file details
        print(f"Received file: {file.filename}, content type: {file.content_type}")
        # Save the uploaded file as a temporary WAV file
        # audio_path = "uploaded_audio.wav"
        with open(file.filename, "wb") as audio_file:
            shutil.copyfileobj(file.file, audio_file) 

        # Verify the file content type
        # if file.content_type != "audio/wav":
        #    raise HTTPException(status_code=400, detail="Invalid file type")

        # prompt = from_stream()
        results = await from_file(file.filename)
        print(f'visualize(): result = {results}\n')
        if results["status"] == 400:
            return JSONResponse(content={"message": results["err"]}, status_code=400)

        summary = await summarize(results["prompt"])

        print(f'visualize(): {summary}\n')

        # image_file = gen_image(use_image, prompt)
        # return {"message": "Image generated", "path": image_file}

        # return {"message": "Transcribing from speech", "transcripts": prompt}            
        results["summary"] = summary
        return JSONResponse(content={"message": results}, status_code=200)
    except Exception as e:
            print(f"visualize(): Error processing request: {e}")
            raise HTTPException(status_code=400, detail=str(e))

@app.get("/generate/")
async def generate_image(prompt: str):
    use_image = True
    prompt = "generate a cartoon cute version"
    input_image = "vv-frontyard conv.jpeg"
    output_file = "vv-frontyard-new"
    print(f'generate_image(): {prompt}\n')

    output = gen_image(use_image, prompt, input_image, output_file)
    return {"message": "Image generated", "path": output}


@app.get("/transcript/")
async def transcript_speech(prompt: str):
    db_dependency = Annotated[Session, Depends(get_db)]

    print(f'transcript_speech(): {prompt}\n')

    output = from_stream()
    return {"message": "Transcribing from speech", "transcripts": output}


@app.get("/summarize/")
async def summarize_text(prompt: str):
    use_image = True
    prompt = "generate a cartoon cute version"
    input_image = "vv-frontyard conv.jpeg"
    output_file = "vv-frontyard-new"
    print(f'generate_image(): {prompt}\n')

    output = summarize()
    return {"message": "Image generated", "path": output}



if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=6188)