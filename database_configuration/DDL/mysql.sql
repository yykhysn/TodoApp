create table Users
(
    id              int auto_increment
        primary key,
    username        varchar(32)       not null,
    email           varchar(128)      not null,
    first_name      varchar(64)       not null,
    last_name       varchar(64)       not null,
    hashed_password varchar(256)      not null,
    is_enabled      tinyint default 0 not null,
    constraint email_UNIQUE
        unique (email),
    constraint username_UNIQUE
        unique (username)
)
    engine = InnoDB;

create table ToDoList
(
    id            int auto_increment
        primary key,
    title         varchar(256)              not null,
    description   varchar(1024)             not null,
    priority      tinyint                   not null,
    is_completed  tinyint  default 0        not null,
    public_uuid   char(36) default (uuid()) not null,
    owner_user_id int                       not null,
    constraint fk_ToDoList_1
        foreign key (owner_user_id) references Users (id)
)
    engine = InnoDB;

create index fk_ToDoList_1_idx
    on ToDoList (owner_user_id);