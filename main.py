import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from database import create_document, get_documents
from schemas import Novel as NovelSchema, Comic as ComicSchema, Anime as AnimeSchema, Movie as MovieSchema

app = FastAPI(title="MediaHub API", description="API untuk membaca novel/komik dan menonton anime/film")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "MediaHub Backend siap!"}

# ---------- Utility ----------
class PaginatedResponse(BaseModel):
    items: List[Dict[str, Any]]
    total: int


def list_collection(collection: str, q: Optional[str] = None, limit: int = 24):
    try:
        query = {}
        if q:
            # Simple regex search across common fields
            query = {"$or": [
                {"title": {"$regex": q, "$options": "i"}},
                {"author": {"$regex": q, "$options": "i"}},
                {"studio": {"$regex": q, "$options": "i"}},
                {"director": {"$regex": q, "$options": "i"}},
                {"tags": {"$elemMatch": {"$regex": q, "$options": "i"}}}
            ]}
        items = get_documents(collection, query, limit)
        # Convert ObjectId to string safely
        from bson import ObjectId
        for it in items:
            for key, val in list(it.items()):
                if isinstance(val, ObjectId):
                    it[key] = str(val)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- Create endpoints ----------
@app.post("/api/novels")
def create_novel(payload: NovelSchema):
    _id = create_document("novel", payload)
    return {"id": _id}

@app.post("/api/comics")
def create_comic(payload: ComicSchema):
    _id = create_document("comic", payload)
    return {"id": _id}

@app.post("/api/animes")
def create_anime(payload: AnimeSchema):
    _id = create_document("anime", payload)
    return {"id": _id}

@app.post("/api/movies")
def create_movie(payload: MovieSchema):
    _id = create_document("movie", payload)
    return {"id": _id}

# Convenience seeding endpoint for a single sample novel
@app.post("/api/novels/sample")
def seed_sample_novel():
    try:
        # Check if sample already exists
        existing = get_documents("novel", {"title": "Contoh Novel: Bintang Senja"}, 1)
        if existing:
            return {"status": "exists", "message": "Sample novel already present"}
        sample = NovelSchema(
            title="Contoh Novel: Bintang Senja",
            author="Ayu Laras",
            synopsis="Kisah romansa dua sahabat masa kecil yang dipertemukan kembali oleh senja di kota pesisir.",
            cover_url="https://picsum.photos/seed/novel-sample/800/1200",
            content=(
                "Bab 1\n"
                "Angin sore berhembus dari arah laut, membawa aroma garam dan kenangan yang lama terkunci.\n\n"
                "Bab 2\n"
                "Di tepian dermaga, mereka kembali berjumpa saat langit menguning, seperti janji yang tak pernah usai."
            ),
            tags=["romansa", "drama", "indo"]
        )
        _id = create_document("novel", sample)
        return {"status": "created", "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------- List/search endpoints ----------
@app.get("/api/novels")
def get_novels(q: Optional[str] = None, limit: int = 24):
    return {"items": list_collection("novel", q, limit)}

@app.get("/api/comics")
def get_comics(q: Optional[str] = None, limit: int = 24):
    return {"items": list_collection("comic", q, limit)}

@app.get("/api/animes")
def get_animes(q: Optional[str] = None, limit: int = 24):
    return {"items": list_collection("anime", q, limit)}

@app.get("/api/movies")
def get_movies(q: Optional[str] = None, limit: int = 24):
    return {"items": list_collection("movie", q, limit)}


# Health/database test
@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
