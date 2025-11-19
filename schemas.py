"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (kept for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Application-specific schemas
# Each class name maps to a collection of the same name in lowercase

class Novel(BaseModel):
    title: str = Field(..., description="Judul novel")
    author: Optional[str] = Field(None, description="Penulis")
    synopsis: Optional[str] = Field(None, description="Sinopsis singkat")
    cover_url: Optional[HttpUrl] = Field(None, description="Gambar sampul")
    content: Optional[str] = Field(None, description="Konten teks (opsional)")
    tags: Optional[List[str]] = Field(default=None, description="Tag/kategori")

class Comic(BaseModel):
    title: str = Field(..., description="Judul komik")
    author: Optional[str] = Field(None, description="Penulis/Ilustrator")
    synopsis: Optional[str] = Field(None, description="Sinopsis singkat")
    cover_url: Optional[HttpUrl] = Field(None, description="Gambar sampul")
    pages: Optional[List[HttpUrl]] = Field(default=None, description="Daftar URL halaman gambar")
    tags: Optional[List[str]] = Field(default=None, description="Tag/kategori")

class Anime(BaseModel):
    title: str = Field(..., description="Judul anime")
    studio: Optional[str] = Field(None, description="Studio produksi")
    synopsis: Optional[str] = Field(None, description="Sinopsis singkat")
    cover_url: Optional[HttpUrl] = Field(None, description="Gambar poster")
    video_url: Optional[HttpUrl] = Field(None, description="URL streaming video")
    episode: Optional[int] = Field(None, ge=1, description="Nomor episode (opsional)")
    tags: Optional[List[str]] = Field(default=None, description="Tag/kategori")

class Movie(BaseModel):
    title: str = Field(..., description="Judul film")
    director: Optional[str] = Field(None, description="Sutradara")
    synopsis: Optional[str] = Field(None, description="Sinopsis singkat")
    cover_url: Optional[HttpUrl] = Field(None, description="Poster")
    video_url: Optional[HttpUrl] = Field(None, description="URL streaming video")
    duration_min: Optional[int] = Field(None, ge=1, description="Durasi dalam menit")
    tags: Optional[List[str]] = Field(default=None, description="Tag/kategori")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
