create table Users
(
    email           text              not null
        unique,
    username        text              not null
        unique,
    first_name      text              not null,
    last_name       text              not null,
    hashed_password text              not null,
    is_enabled      integer default 0 not null,
    id              integer           not null
        primary key autoincrement
);

create table ToDoList
(
    id            INTEGER                                      not null
        primary key autoincrement,
    title         TEXT                                         not null,
    description   TEXT                                         not null,
    priority      INTEGER                                      not null,
    is_completed  INTEGER default 0                            not null,
    owner_user_id integer                                      not null
        references Users,
    public_uuid   text    default (lower(hex(randomblob(16)))) not null
        unique
);

create index ToDoList_owner_user_id_index
    on ToDoList (owner_user_id);