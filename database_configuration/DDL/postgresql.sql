create table "Users"
(
    id              serial
        primary key,
    username        text                  not null
        unique,
    email           text                  not null
        unique,
    first_name      text                  not null,
    last_name       text                  not null,
    hashed_password text                  not null,
    is_enabled      boolean default false not null
);

alter table "Users"
    owner to todoapp;

create table "ToDoList"
(
    id            serial
        primary key,
    title         text                              not null,
    description   text                              not null,
    priority      smallint                          not null,
    is_completed  boolean default false             not null,
    public_uuid   uuid    default gen_random_uuid() not null
        unique,
    owner_user_id integer                           not null
        references "Users"
);

alter table "ToDoList"
    owner to todoapp;

create index idx_todolist_owner_user_id
    on "ToDoList" (owner_user_id);