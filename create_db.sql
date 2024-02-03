drop table if exists ACTIVE_CLIENTS;
drop table if exists OFFERS;
drop table if exists EXCHANGE_RATES;
drop table if exists CARDS;
drop table if exists BONUS;
drop table if exists MCC_CATEGORIES;

-- Задание 1
create table ACTIVE_CLIENTS
(
    report_month,
    client_id
);

insert into ACTIVE_CLIENTS (report_month, client_id)
values ('2018-01-01', '1847982357'),
       ('2018-01-01', '938475'),
       ('2018-04-01', '1847982357'),
       ('2018-02-01', '6789998'),
       ('2018-03-01', '67900001');

-- Задание 2
create table OFFERS
(
    offer_id,
    offer_start_date,
    offer_expiration_date
);

insert into OFFERS (offer_id, offer_start_date, offer_expiration_date)
values (83942, '2017-12-01', '2018-02-01'),
       (94859, '2018-05-03', '2018-10-19');

-- Задание 3
create table CARDS
(
    client_id,
    card_id,
    open_date,
    close_date,
    card_type
);

insert into CARDS (client_id, card_id, open_date, close_date, card_type)
values (1232110, 49582985729, '2019-01-12', NULL, 'DC'),
       (234235, 48574092749, '2017-03-29', '2018-09-01', 'CC'),
       ---Запись от себя, чтобы хоть что-то выбиралось
       (322322, 1234567890, '2018-06-12', '2018-12-01', 'DC');

--Задание 4
create table BONUS
(
    client_id,
    bonus_date,
    bonus_cnt,
    mcc_code
);

create table MCC_CATEGORIES
(
    mcc_code,
    mcc_category
);

insert into BONUS (client_id, bonus_date, bonus_cnt, mcc_code)
values (1232110, '2018-01-01', 12, 3617),
       (234235, '2018-06-17', 5, 5931),
       (10, '2018-06-17', 400, 4000),
       (20, '2020-06-17', 600, 3031),
       (10, '2020-12-01', 600, 3031),
       (20, '2021-01-01', 600, 4000),
       (20, '2022-01-01', 1000, 4000),
       (30, '2023-01-01', 3000, 4000),
       (40, '2010-01-01', 1300, 3031);

insert into MCC_CATEGORIES (mcc_code, mcc_category)
values (3031, 'Авиабилеты'),
       (5735, 'Музыка'),
       (4000, 'Отели');

-- Задание 5
create table EXCHANGE_RATES
(
    code,
    rate,
    value_day
);

insert into EXCHANGE_RATES (code, rate, value_day)
values ('USD', 60, '2020-02-01'),
       ('EUR', 78, '2020-03-01'),
       ('USD', 65, '2021-05-01'),
       ('EUR', 88, '2022-06-01'),
       ('USD', 70, '2022-08-01'),
       ('USD', 75, '2023-09-01');