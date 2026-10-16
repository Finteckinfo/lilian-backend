-- Optional seed after schema.sql. Media URLs point at this Next.js /public folder.

insert into content_posts (published_at, title, slug, category, body_markdown, is_featured) values
(
  '2026-08-15',
  'Building My Beauty Empire',
  'building-my-beauty-empire',
  'Journey_POV',
  E'> Confidence isn''t something you wear on top. It''s something that radiates from within when someone finally sees themselves the way they deserve to be seen.\n\nEvery morning I wake up and choose myself. Not in a selfish way — in the way that says I am building something that outlasts trends, outlasts algorithms, outlasts the noise. Being Lillian isn''t just a brand. It''s a declaration.\n\nWhen I first picked up a makeup brush professionally, people asked me why I didn''t just get a normal job. What they didn''t understand is that artistry is not a fallback — it''s a calling. Every face I work on tells a story, and I''ve made it my mission to tell those stories with precision and intention.\n\nThis journey has taught me that building a personal brand means being intentional about every detail — from the clients you take on, to the content you publish, to the collaborations you align with. Not every opportunity is the right one.\n\nThis is just the beginning. The platform you''re looking at right now is the next chapter — a space where my artistry, my voice, and my community come together under one roof. Welcome to Being Lillian.',
  true
),
(
  '2026-07-22',
  'Morning Routines That Keep Me Going',
  'morning-routines-that-keep-me-going',
  'Motivation',
  E'> The first hour of the day belongs to me. Everything else is a gift I give from a full cup.\n\nBridal mornings start before sunrise. If I don''t protect my own first hour, the rest of the day becomes reaction instead of intention.\n\nI drink water, stretch, and review the look notes for the day — skin type, lighting, timeline. Then I pack kits in the same order every time so nothing is forgotten when the schedule tightens.\n\nCreativity is not chaos. It is a practiced sequence that leaves room for instinct once I am in the chair.\n\nIf you are building a beauty practice, treat your mornings as part of the craft. Clients feel the difference between an artist who arrived prepared and one who arrived scrambled.',
  true
),
(
  '2026-06-10',
  'Product Review: My Holy Grail Foundation',
  'my-holy-grail-foundation',
  'Reviews',
  E'> I don''t recommend products I won''t stake a twelve-hour wedding on.\n\nThis is not a sponsored list. It is the base I reach for when the lighting is unforgiving and the timeline is not.\n\nCoverage is buildable without turning heavy. On combination skin it holds through heat; on dry skin it needs a hydrating primer and a damp sponge, not extra powder.\n\nWear time on a typical bridal day is eight to ten hours with one blot and a cream highlight refresh. Flash photography stays even if you set the T-zone only.\n\nIf a client asks for drugstore alternatives, I am honest: this one earns the price because I do not have to fight it. That time belongs to the rest of the face.',
  true
),
(
  '2026-05-18',
  'Behind the Scenes: Wedding Season',
  'behind-the-scenes-wedding-season',
  'Journey_POV',
  E'> The work is technical. The moment she sees herself is the reason I stay.\n\nWedding season is logistics dressed as glamour. Call times, parking, kit doubles, emergency blotting papers, and a calm voice when the timeline slips.\n\nI arrive early enough to set a quiet station. Music low. Brushes laid out. The bride should walk into a room that already feels held.\n\nThe look is decided weeks before, but the skin in front of me is never identical to the trial. I adjust, I don''t panic.\n\nWhen she looks in the mirror, I step back. That pause is the job as much as the liner.',
  false
),
(
  '2026-04-02',
  'Self-Care Is Not Selfish',
  'self-care-is-not-selfish',
  'Motivation',
  E'> Rest is not a reward for finishing. It is part of the work.\n\nCreators are praised for output and punished for pausing. I used to believe that too.\n\nNow I block recovery days after stacked events. No content filming. No late-night kit rebuilds unless something is actually broken.\n\nMy reset is simple: sleep, a long walk, and a face I don''t have to perform on. Then I can return to clients as an artist, not a machine.\n\nIf you are building beside me, protect your off hours. The brand only lasts as long as the person behind it.',
  false
),
(
  '2026-03-08',
  'A Milestone Season for Being Lillian',
  'a-milestone-season-for-being-lillian',
  'Self_Promotion',
  E'> Visibility is useful. Alignment is better.\n\nThis season brought editorial bookings, a regional feature, and two brand collaborations I actually wanted to put my name on.\n\nI am sharing the wins because they were built slowly — trials, referrals, and work that showed up on time. Not because a single post went viral.\n\nThe next chapter is this platform: one place for bookings, stories, and the portfolio, so clients don''t have to hunt across apps.\n\nIf you are a brand looking to collaborate, or a client ready to book, start on WhatsApp. I read every message myself.',
  false
)
on conflict (slug) do nothing;

insert into portfolio_items (title, category, media_type, media_url, video_url, instagram_url, testimonial_text, display_order) values
('Bridal close-up', 'MUA_Clients', 'Image', '/media/bridal-closeup.jpg', null, 'https://www.instagram.com/p/CcYc0FDaxo/', null, 1),
('In the chair — 2 Feb 2020', 'Photoshoots', 'Video', '/media/craft-video-still.jpg', '/media/craft-video.mp4', 'https://www.instagram.com/reel/B4EZIUf5Ztb/', null, 2),
('Collaboration Month', 'Photoshoots', 'Image', '/media/editorial-hat.jpg', null, 'https://www.instagram.com/p/CSbqO-Qe9Hs/', null, 3),
('Challenge accepted', 'Photoshoots', 'Image', '/media/editorial-fullbody.jpg', null, 'https://www.instagram.com/p/CDNZ65wveA/', null, 4),
('Client note', 'Testimonials', 'Image', '/media/bridal-closeup.jpg', null, 'https://www.instagram.com/p/CcYc0FDaxo/', 'To you too darling.', 10),
('Client note', 'Testimonials', 'Image', '/media/bridal-closeup.jpg', null, 'https://www.instagram.com/p/CcYc0FDaxo/', 'Wow!', 11),
('Client note', 'Testimonials', 'Image', '/media/craft-video-still.jpg', null, 'https://www.instagram.com/reel/B4EZIUf5Ztb/', 'Beautiful women right there.', 12);
