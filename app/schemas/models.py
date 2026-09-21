from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ServiceType(str, Enum):
    MUA = "MUA"
    Brand_Collab = "Brand_Collab"
    Event = "Event"
    General = "General"


class LeadStatus(str, Enum):
    New = "New"
    Contacted = "Contacted"
    Quoted = "Quoted"
    Booked = "Booked"
    Completed = "Completed"
    Legacy = "Legacy"


class PostCategory(str, Enum):
    Motivation = "Motivation"
    Self_Promotion = "Self_Promotion"
    Reviews = "Reviews"
    Journey_POV = "Journey_POV"


class PortfolioCategory(str, Enum):
    MUA_Clients = "MUA_Clients"
    Photoshoots = "Photoshoots"
    Events = "Events"
    Testimonials = "Testimonials"


class MediaType(str, Enum):
    Image = "Image"
    Video = "Video"


class LeadCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    phone_number: str = Field(min_length=7, max_length=32)
    email: Optional[str] = None
    service_type: ServiceType
    event_date: Optional[date] = None
    location: Optional[str] = None
    budget: Optional[str] = None
    notes: Optional[str] = None


class LeadOut(BaseModel):
    id: UUID
    created_at: str
    full_name: str
    phone_number: str
    email: Optional[str] = None
    service_type: ServiceType
    event_date: Optional[str] = None
    status: LeadStatus
    notes: Optional[str] = None


class LeadStatusUpdate(BaseModel):
    status: LeadStatus
    note: Optional[str] = None


class PostOut(BaseModel):
    id: str
    slug: str
    title: str
    category: PostCategory
    published_at: str
    body_markdown: str
    excerpt: str
    quote: Optional[str] = None
    media_urls: list[str] = []
    is_featured: bool = False


class PortfolioOut(BaseModel):
    id: str
    title: str
    category: PortfolioCategory
    media_type: MediaType
    media_url: str
    video_url: Optional[str] = None
    instagram_url: Optional[str] = None
    testimonial_text: Optional[str] = None
    display_order: int = 0


class PostWrite(BaseModel):
    slug: str = Field(min_length=1, max_length=120)
    title: str = Field(min_length=1, max_length=200)
    category: PostCategory
    published_at: str = Field(min_length=8, max_length=32)
    body_markdown: str = ""
    excerpt: str = ""
    quote: Optional[str] = None
    media_urls: list[str] = []
    is_featured: bool = False


class PortfolioWrite(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    category: PortfolioCategory
    media_type: MediaType = MediaType.Image
    media_url: str = Field(min_length=1, max_length=500)
    video_url: Optional[str] = None
    instagram_url: Optional[str] = None
    testimonial_text: Optional[str] = None
    display_order: int = 0


class SiteSettings(BaseModel):
    site_name: str = "Being Lillian"
    tagline: str = "Makeup artistry, brand consulting, and collaborations."
    hero_headline: str = "Beauty with intention"
    accent_color: str = "#C9A88A"
    paper_color: str = "#F7F4EF"
    ink_color: str = "#2A2420"
    whatsapp_number: str = "0000000000"
    instagram_url: str = "https://www.instagram.com/lilianbeauty_studio"
    show_whatsapp_fab: bool = True
    show_journal: bool = True
    show_portfolio: bool = True
    show_book_cta: bool = True
    default_theme: str = "system"


class SiteSettingsPatch(BaseModel):
    site_name: Optional[str] = None
    tagline: Optional[str] = None
    hero_headline: Optional[str] = None
    accent_color: Optional[str] = None
    paper_color: Optional[str] = None
    ink_color: Optional[str] = None
    whatsapp_number: Optional[str] = None
    instagram_url: Optional[str] = None
    show_whatsapp_fab: Optional[bool] = None
    show_journal: Optional[bool] = None
    show_portfolio: Optional[bool] = None
    show_book_cta: Optional[bool] = None
    default_theme: Optional[str] = None


class AuthSignup(BaseModel):
    email: str = Field(min_length=5, max_length=200)
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=200)


class AuthLogin(BaseModel):
    email: str = Field(min_length=5, max_length=200)
    password: str = Field(min_length=1, max_length=128)


class AuthUserOut(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    created_at: Optional[str] = None


class AuthTokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUserOut
