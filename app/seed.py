"""In-memory seed when Supabase is not configured — mirrors frontend/lib/seed.ts."""

from app.schemas.models import MediaType, PortfolioCategory, PostCategory

SEED_POSTS = [
    {
        "id": "empire",
        "slug": "building-my-beauty-empire",
        "title": "Building My Beauty Empire",
        "category": PostCategory.Journey_POV,
        "published_at": "2026-08-15",
        "excerpt": "The raw truth about turning a passion for makeup artistry into a full-fledged personal brand — from first clients to repeat bookings.",
        "quote": "Confidence isn't something you wear on top. It's something that radiates from within when someone finally sees themselves the way they deserve to be seen.",
        "is_featured": True,
        "media_urls": [],
        "body_markdown": (
            "> Confidence isn't something you wear on top. It's something that radiates from within when someone finally sees themselves the way they deserve to be seen.\n\n"
            "Every morning I wake up and choose myself. Not in a selfish way — in the way that says I am building something that outlasts trends, outlasts algorithms, outlasts the noise. Being Lillian isn't just a brand. It's a declaration.\n\n"
            "When I first picked up a makeup brush professionally, people asked me why I didn't just get a normal job. What they didn't understand is that artistry is not a fallback — it's a calling. Every face I work on tells a story, and I've made it my mission to tell those stories with precision and intention.\n\n"
            "This journey has taught me that building a personal brand means being intentional about every detail — from the clients you take on, to the content you publish, to the collaborations you align with. Not every opportunity is the right one.\n\n"
            "This is just the beginning. The platform you're looking at right now is the next chapter — a space where my artistry, my voice, and my community come together under one roof. Welcome to Being Lillian."
        ),
    },
    {
        "id": "mornings",
        "slug": "morning-routines-that-keep-me-going",
        "title": "Morning Routines That Keep Me Going",
        "category": PostCategory.Motivation,
        "published_at": "2026-07-22",
        "excerpt": "How I structure my mornings to stay creative, energized, and ready for back-to-back client sessions.",
        "quote": "The first hour of the day belongs to me. Everything else is a gift I give from a full cup.",
        "is_featured": True,
        "media_urls": [],
        "body_markdown": (
            "> The first hour of the day belongs to me. Everything else is a gift I give from a full cup.\n\n"
            "Bridal mornings start before sunrise. If I don't protect my own first hour, the rest of the day becomes reaction instead of intention.\n\n"
            "I drink water, stretch, and review the look notes for the day — skin type, lighting, timeline. Then I pack kits in the same order every time so nothing is forgotten when the schedule tightens.\n\n"
            "Creativity is not chaos. It is a practiced sequence that leaves room for instinct once I am in the chair.\n\n"
            "If you are building a beauty practice, treat your mornings as part of the craft. Clients feel the difference between an artist who arrived prepared and one who arrived scrambled."
        ),
    },
    {
        "id": "foundation",
        "slug": "my-holy-grail-foundation",
        "title": "Product Review: My Holy Grail Foundation",
        "category": PostCategory.Reviews,
        "published_at": "2026-06-10",
        "excerpt": "An honest breakdown of the foundation I reach for on every bridal and editorial job — coverage, wear time, and why it earns its price tag.",
        "quote": "I don't recommend products I won't stake a twelve-hour wedding on.",
        "is_featured": True,
        "media_urls": [],
        "body_markdown": (
            "> I don't recommend products I won't stake a twelve-hour wedding on.\n\n"
            "This is not a sponsored list. It is the base I reach for when the lighting is unforgiving and the timeline is not.\n\n"
            "Coverage is buildable without turning heavy. On combination skin it holds through heat; on dry skin it needs a hydrating primer and a damp sponge, not extra powder.\n\n"
            "Wear time on a typical bridal day is eight to ten hours with one blot and a cream highlight refresh. Flash photography stays even if you set the T-zone only.\n\n"
            "If a client asks for drugstore alternatives, I am honest: this one earns the price because I do not have to fight it. That time belongs to the rest of the face."
        ),
    },
    {
        "id": "wedding",
        "slug": "behind-the-scenes-wedding-season",
        "title": "Behind the Scenes: Wedding Season",
        "category": PostCategory.Journey_POV,
        "published_at": "2026-05-18",
        "excerpt": "What a typical wedding weekend looks like — early mornings, bridal prep, and the magic of seeing a bride's reaction.",
        "quote": "The work is technical. The moment she sees herself is the reason I stay.",
        "is_featured": False,
        "media_urls": [],
        "body_markdown": (
            "> The work is technical. The moment she sees herself is the reason I stay.\n\n"
            "Wedding season is logistics dressed as glamour. Call times, parking, kit doubles, emergency blotting papers, and a calm voice when the timeline slips.\n\n"
            "I arrive early enough to set a quiet station. Music low. Brushes laid out. The bride should walk into a room that already feels held.\n\n"
            "The look is decided weeks before, but the skin in front of me is never identical to the trial. I adjust, I don't panic.\n\n"
            "When she looks in the mirror, I step back. That pause is the job as much as the liner."
        ),
    },
    {
        "id": "selfcare",
        "slug": "self-care-is-not-selfish",
        "title": "Self-Care Is Not Selfish",
        "category": PostCategory.Motivation,
        "published_at": "2026-04-02",
        "excerpt": "A reminder to fellow creatives: you cannot pour from an empty cup. Here's how I recharge between projects.",
        "quote": "Rest is not a reward for finishing. It is part of the work.",
        "is_featured": False,
        "media_urls": [],
        "body_markdown": (
            "> Rest is not a reward for finishing. It is part of the work.\n\n"
            "Creators are praised for output and punished for pausing. I used to believe that too.\n\n"
            "Now I block recovery days after stacked events. No content filming. No late-night kit rebuilds unless something is actually broken.\n\n"
            "My reset is simple: sleep, a long walk, and a face I don't have to perform on. Then I can return to clients as an artist, not a machine.\n\n"
            "If you are building beside me, protect your off hours. The brand only lasts as long as the person behind it."
        ),
    },
    {
        "id": "press",
        "slug": "a-milestone-season-for-being-lillian",
        "title": "A Milestone Season for Being Lillian",
        "category": PostCategory.Self_Promotion,
        "published_at": "2026-03-08",
        "excerpt": "Press, campaigns, and the collaborations that marked this chapter — and what comes next.",
        "quote": "Visibility is useful. Alignment is better.",
        "is_featured": False,
        "media_urls": [],
        "body_markdown": (
            "> Visibility is useful. Alignment is better.\n\n"
            "This season brought editorial bookings, a regional feature, and two brand collaborations I actually wanted to put my name on.\n\n"
            "I am sharing the wins because they were built slowly — trials, referrals, and work that showed up on time. Not because a single post went viral.\n\n"
            "The next chapter is this platform: one place for bookings, stories, and the portfolio, so clients don't have to hunt across apps.\n\n"
            "If you are a brand looking to collaborate, or a client ready to book, start on WhatsApp. I read every message myself."
        ),
    },
]

SEED_PORTFOLIO = [
    {"id": "bridal-closeup", "title": "Bridal close-up", "category": PortfolioCategory.MUA_Clients, "media_type": MediaType.Image, "media_url": "/media/bridal-closeup.jpg", "video_url": None, "instagram_url": "https://www.instagram.com/p/CcYcOfjDaxo/", "testimonial_text": None, "display_order": 1},
    {"id": "craft-video", "title": "In the chair — 2 Feb 2020", "category": PortfolioCategory.Photoshoots, "media_type": MediaType.Video, "media_url": "/media/craft-video-still.jpg", "video_url": "/media/craft-video.mp4", "instagram_url": "https://www.instagram.com/reel/B8ZliJFg5Zb/", "testimonial_text": None, "display_order": 2},
    {"id": "editorial-hat", "title": "Collaboration Month", "category": PortfolioCategory.Photoshoots, "media_type": MediaType.Image, "media_url": "/media/editorial-hat.jpg", "video_url": None, "instagram_url": "https://www.instagram.com/p/CSbgO-Qo9Hs/", "testimonial_text": None, "display_order": 3},
    {"id": "editorial-fullbody", "title": "Challenge accepted", "category": PortfolioCategory.Photoshoots, "media_type": MediaType.Image, "media_url": "/media/editorial-fullbody.jpg", "video_url": None, "instagram_url": "https://www.instagram.com/p/CDNz6SwgveA/", "testimonial_text": None, "display_order": 4},
    {"id": "bridal-02", "title": "Bridal detail", "category": PortfolioCategory.MUA_Clients, "media_type": MediaType.Image, "media_url": "/media/bridal-02.jpg", "video_url": None, "instagram_url": "https://www.instagram.com/p/CcYcOfjDaxo/", "testimonial_text": None, "display_order": 5},
    {"id": "editorial-02", "title": "Editorial color", "category": PortfolioCategory.Photoshoots, "media_type": MediaType.Image, "media_url": "/media/editorial-02.jpg", "video_url": None, "instagram_url": "https://www.instagram.com/p/CSbgO-Qo9Hs/", "testimonial_text": None, "display_order": 6},
    {"id": "editorial-03", "title": "On set", "category": PortfolioCategory.Photoshoots, "media_type": MediaType.Image, "media_url": "/media/editorial-03.jpg", "video_url": None, "instagram_url": "https://www.instagram.com/reel/B8ZliJFg5Zb/", "testimonial_text": None, "display_order": 7},
    {"id": "events-01", "title": "Event glam", "category": PortfolioCategory.Events, "media_type": MediaType.Image, "media_url": "/media/events-01.jpg", "video_url": None, "instagram_url": "https://www.instagram.com/p/CcYcOfjDaxo/", "testimonial_text": None, "display_order": 8},
    {"id": "events-02", "title": "Session day", "category": PortfolioCategory.Events, "media_type": MediaType.Image, "media_url": "/media/events-02.jpg", "video_url": None, "instagram_url": "https://www.instagram.com/p/CDNz6SwgveA/", "testimonial_text": None, "display_order": 9},
    {"id": "quote-penny", "title": "Client note", "category": PortfolioCategory.Testimonials, "media_type": MediaType.Image, "media_url": "/media/bridal-closeup.jpg", "video_url": None, "instagram_url": "https://www.instagram.com/p/CcYcOfjDaxo/", "testimonial_text": "To you too darling.", "display_order": 10},
    {"id": "quote-winnie", "title": "Client note", "category": PortfolioCategory.Testimonials, "media_type": MediaType.Image, "media_url": "/media/bridal-closeup.jpg", "video_url": None, "instagram_url": "https://www.instagram.com/p/CcYcOfjDaxo/", "testimonial_text": "Wow!", "display_order": 11},
    {"id": "quote-illyasigo", "title": "Client note", "category": PortfolioCategory.Testimonials, "media_type": MediaType.Image, "media_url": "/media/craft-video-still.jpg", "video_url": None, "instagram_url": "https://www.instagram.com/reel/B8ZliJFg5Zb/", "testimonial_text": "Beautiful women right there.", "display_order": 12},
]

LOCAL_LEADS: list[dict] = []
LOCAL_LEAD_EVENTS: list[dict] = []
