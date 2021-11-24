create table quote
(
    id         serial primary key,
    quote_text       text      not null,
    author       text      not null,
    created_at timestamp not null default now(),
    updated_at timestamp
);