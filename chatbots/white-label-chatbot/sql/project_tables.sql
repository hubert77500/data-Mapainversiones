
create table if not exists public.csv_files
(
    id      serial
        primary key,
    name    varchar,
    content text,
    date    timestamp
);

create table if not exists public.allowed_numbers
(
    id     serial
        primary key,
    name   varchar,
    number varchar
        unique
);


create table if not exists public.chat_sessions
(
    id              serial
        primary key,
    sender_id       varchar,
    created_at      timestamp,
    last_message_at timestamp
);

create table if not exists public.chat_messages
(
    id                     serial
        primary key,
    conversation_sender_id varchar,
    content                varchar,
    is_system              boolean,
    date                   timestamp,
    session_id             integer
        constraint chat_messages_session_id_fk
            references public.chat_sessions
);

CREATE TABLE IF NOT EXISTS public.tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE
);


CREATE TABLE IF NOT EXISTS public.sender_tags
(
    id serial PRIMARY KEY,
    sender_id varchar,
    tag_id integer REFERENCES public.tags,
    assigned_at timestamp DEFAULT current_timestamp
);

