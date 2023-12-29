create table "address" ("id" bigint not null, "address_line" varchar(255), "city" varchar(255), "coordinates" varchar(255), "country" varchar(255), "postal_code" varchar(255), "street_number" varchar(255), "unit_number" varchar(255), primary key ("id"));
create table "billing_info" ("id" bigserial not null, "order_id" bigint unique, "credit_card_number" varchar(255), primary key ("id"));
create table "customer" ("user_id" bigint not null, primary key ("user_id"));
create table "customer_addresses" ("addresses_id" bigint not null unique, "customer_user_id" bigint not null);
create table "delivery" ("address_id" bigint unique, "delivery_time" timestamp(6), "driver_user_id" bigint unique, "id" bigserial not null, "order_id" bigint unique, "status" varchar(255), primary key ("id"));
create table "employee" ("rating" float4, "user_id" bigint not null, "vehicle" varchar(255), primary key ("user_id"));
create table "menu" ("category_id" bigint, "id" bigserial not null, "restaurant_id" bigint, "name" varchar(255), primary key ("id"));
create table "order" ("customer_id" bigint, "delivery_id" bigint unique, "id" bigserial not null, "order_date" timestamp(6), "restaurant_id" bigint, "order_status" varchar(255), primary key ("id"));
create table "order_item" ("quantity" integer not null, "id" bigserial not null, "order_id" bigint, "product_id" bigint, primary key ("id"));
create table "payment_transaction" ("amount" numeric(38,2), "id" bigserial not null, "order_id" bigint unique, "payment_gateway" varchar(255), primary key ("id"));
create table "product" ("price" float(53) not null, "category_id" bigint, "id" bigserial not null, "menu_id" bigint, "description" varchar(255), "name" varchar(255), primary key ("id"));
create table "product_category" ("id" bigserial not null, "name" varchar(255), primary key ("id"));
create table "product_image" ("id" bigserial not null, "product_id" bigint, "image_url" varchar(255), primary key ("id"));
create table "restaurant" ("address_id" bigint unique, "id" bigint not null, "name" varchar(255), "operating_hours" varchar(255), "phone_number" varchar(255), primary key ("id"));
create table "users" ("id" bigserial not null, "email" varchar(255) unique, "name" varchar(255), "password" varchar(255), "role" varchar(255), primary key ("id"));
alter table if exists "billing_info" add constraint "FKa68o5entfwlkly80nikb4yrp7" foreign key ("order_id") references "order";
alter table if exists "customer" add constraint "FK9p1ojd734l61nw7m7ydwk9lpe" foreign key ("user_id") references "users";
alter table if exists "customer_addresses" add constraint "FKexa5qcqpyhweqmrdjm3tcn6n1" foreign key ("addresses_id") references "address";
alter table if exists "customer_addresses" add constraint "FK4a9uandxk6of3x5co4cnxhp2p" foreign key ("customer_user_id") references "customer";
alter table if exists "delivery" add constraint "FKmrgjl8phe21xowyvhi23xh5rf" foreign key ("address_id") references "address";
alter table if exists "delivery" add constraint "FK6v6xbwaewi91rpk1fbrf8o2kt" foreign key ("driver_user_id") references "employee";
alter table if exists "delivery" add constraint "FKp9fvm2l23kr74hqouqb3ymm6h" foreign key ("order_id") references "order";
alter table if exists "employee" add constraint "FKhmy4evga5v9p6o5jw1ynve0e2" foreign key ("user_id") references "users";
alter table if exists "menu" add constraint "FK237gi34t55g3fxcfxqiqibnsy" foreign key ("category_id") references "product_category";
alter table if exists "menu" add constraint "FKhbvr97ilq3hnh6tuti9vfmvd4" foreign key ("restaurant_id") references "restaurant";
alter table if exists "order" add constraint "FKk1m6gjs4m7rtgb5lw01g35yca" foreign key ("customer_id") references "customer";
alter table if exists "order" add constraint "FKbjd4l7kbg6g7nxkvcxi75t85n" foreign key ("delivery_id") references "delivery";
alter table if exists "order" add constraint "FKcxidsvnoyt6wt7fs54y01edd8" foreign key ("restaurant_id") references "restaurant";
alter table if exists "order_item" add constraint "FKsxgfmcie6oo67uxtk9hqk02mq" foreign key ("product_id") references "product";
alter table if exists "order_item" add constraint "FKl1bqqbilx1hdy29vykrqkgu3p" foreign key ("order_id") references "order";
alter table if exists "payment_transaction" add constraint "FKddabnj5mynilpqpresb7v8dxh" foreign key ("order_id") references "order";
alter table if exists "product" add constraint "FKqtl9rdhgv7o69thj61wr4b40r" foreign key ("category_id") references "product_category";
alter table if exists "product" add constraint "FKbou5v9p0h6r0ur16a0a4mf2lg" foreign key ("menu_id") references "menu";
alter table if exists "product_image" add constraint "FK404iut26wg4pq85osw3vn0kwd" foreign key ("product_id") references "product";
alter table if exists "restaurant" add constraint "FK7mkdc95j4tarcv59dg4uecwe0" foreign key ("address_id") references "address";
