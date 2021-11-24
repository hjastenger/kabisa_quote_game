create table quote_game
(
    id         serial primary key,
    seed         serial not null,
    created_at timestamp not null default now(),
    updated_at timestamp
);

create table game_square
(
    id         serial primary key,
    quote_game_id         serial not null references quote_game (id),
    quote_id         serial not null references quote (id),
    x_pos       serial      not null,
    y_pos       serial      not null,
    guessed       boolean      not null,
    created_at timestamp not null default now(),
    updated_at timestamp
);