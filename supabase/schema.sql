-- Being Lillian SDS schema (Phases 1–2)
-- Run in the Supabase SQL editor, then optionally run seed.sql

create extension if not exists "pgcrypto";

do $$ begin
  create type service_type as enum ('MUA', 'Brand_Collab', 'Event', 'General');
exception when duplicate_object then null; end $$;

do $$ begin
  create type lead_status as enum ('New', 'Contacted', 'Quoted', 'Booked', 'Completed', 'Legacy');
exception when duplicate_object then null; end $$;

do $$ begin
  create type post_category as enum ('Motivation', 'Self_Promotion', 'Reviews', 'Journey_POV');
exception when duplicate_object then null; end $$;

do $$ begin
  create type portfolio_category as enum ('MUA_Clients', 'Photoshoots', 'Events', 'Testimonials');
exception when duplicate_object then null; end $$;

do $$ begin
  create type media_type as enum ('Image', 'Video');
exception when duplicate_object then null; end $$;

create table if not exists leads (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  full_name text not null,
  phone_number text not null,
  email text,
  service_type service_type not null,
  event_date date,
  status lead_status not null default 'New',
  notes text
);

create index if not exists leads_phone_idx on leads (phone_number);
create index if not exists leads_status_idx on leads (status);

create table if not exists content_posts (
  id uuid primary key default gen_random_uuid(),
  published_at timestamptz not null default now(),
  title text not null,
  slug text not null unique,
  category post_category not null,
  body_markdown text not null,
  media_urls text[] not null default '{}',
  is_featured boolean not null default false
);

create table if not exists portfolio_items (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  category portfolio_category not null,
  media_type media_type not null,
  media_url text not null,
  video_url text,
  instagram_url text,
  testimonial_text text,
  display_order integer not null default 0
);

alter table leads enable row level security;
alter table content_posts enable row level security;
alter table portfolio_items enable row level security;

drop policy if exists "public read posts" on content_posts;
create policy "public read posts" on content_posts for select using (true);

drop policy if exists "public read portfolio" on portfolio_items;
create policy "public read portfolio" on portfolio_items for select using (true);

-- Leads: no public select. Inserts go through the Next.js API with the service role key.
-- If you only have the anon key, uncomment the insert policy below.
-- drop policy if exists "anon insert leads" on leads;
-- create policy "anon insert leads" on leads for insert with check (true);
