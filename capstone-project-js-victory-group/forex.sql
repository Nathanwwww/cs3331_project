create table User (
    id serial primary key,
    username text unique,
    password text,
    email text unique,
    phone integer unique,
    register_date timestamp not null default CURRENT_TIME,
    CONSTRAINT Vailid_email CHECK (email ~ ^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$),
    -- a valid email is in the form of xxx@xxx(.xxx).xxx
    CONSTRAINT valid_Phone_Number CHECK(phone ~ ^[0-9]{9,10})
    -- a valid phone number in Australia is 9 or 10 bits digits
)
create table Account(
    id serial primary key,
    balance float default (0.00)
)

create table Currency_in_Account(
    currency_id integer references Currency(id),
    account_id integer references Account(id),
    primary key (account_id, currency_id)
)
create table currency(
    id serial primary key,
    full_name text unique,
    name_code text unique
)
create table transaction(
    transaction_id serial primary key,
    user_id integer references User(id),
    time timestamp not null default CURRENT_TIME,
    currency_id integer references Currency(id),
    exange_rate float not null,
    status char(7) not null,
    type char(10) not null,
    CONSTRAINT Valid_Status CHECK(status in ('successed', 'failiure', 'pending')),
    CONSTRAINT Valid_Type CHECK(type in ('BUY', 'buy','Buy', 'Sell','SELL','sell'))
)
create table bankaccount(
    user_id integer references User(id),
    bank_name text ,
    card_number integer primary key,
    security_number integer NOT NULL,
    expire_date date NOT NULL,
    holder_name text NOT NULL
)