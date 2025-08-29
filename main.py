from fastapi import FastAPI, HTTPException
from WordViner import WordViner

word_viner = WordViner()

app = FastAPI()

# /
@app.get("/")
async def home():
    return {"message": "welcome to word vines"}

# /map/{word}
@app.get("/map/{word}")
async def map_word(word: str):
    if not word_viner.in_vocab(word):
        raise HTTPException(status_code=404, detail="Word not found")
    else:
        return {"centre": word,
                "synonyms": word_viner.get_synonyms(word),
                "positions": word_viner.get_positions(word)}