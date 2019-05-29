--
-- Файл сгенерирован с помощью SQLiteStudio v3.2.1 в Пт май 17 08:25:51 2019
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: admin
DROP TABLE IF EXISTS admin;

CREATE TABLE admin (
    id      INTEGER NOT NULL
                    PRIMARY KEY,
    user_id INTEGER NOT NULL,
    status  INTEGER NOT NULL
);

INSERT INTO admin (
                      id,
                      user_id,
                      status
                  )
                  VALUES (
                      1,
                      5675578,
                      1
                  );

INSERT INTO admin (
                      id,
                      user_id,
                      status
                  )
                  VALUES (
                      2,
                      697651824,
                      1
                  );


-- Таблица: adminconsumerstata
DROP TABLE IF EXISTS adminconsumerstata;

CREATE TABLE adminconsumerstata (
    id      INTEGER  NOT NULL
                     PRIMARY KEY,
    user_id INTEGER  NOT NULL,
    sellers INTEGER  NOT NULL,
    buyers  INTEGER  NOT NULL,
    date    DATETIME NOT NULL
);

INSERT INTO adminconsumerstata (
                                   id,
                                   user_id,
                                   sellers,
                                   buyers,
                                   date
                               )
                               VALUES (
                                   1,
                                   5675578,
                                   60,
                                   50,
                                   '2019-05-16 15:53:05.470827'
                               );

INSERT INTO adminconsumerstata (
                                   id,
                                   user_id,
                                   sellers,
                                   buyers,
                                   date
                               )
                               VALUES (
                                   2,
                                   697651824,
                                   54,
                                   32,
                                   '2019-05-14 10:06:15.303258'
                               );


-- Таблица: agentconsumertask
DROP TABLE IF EXISTS agentconsumertask;

CREATE TABLE agentconsumertask (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    date_create DATETIME      NOT NULL,
    date_start  DATETIME      NOT NULL,
    name        VARCHAR (255) NOT NULL,
    consumer_id INTEGER       NOT NULL,
    agent_id    INTEGER       NOT NULL,
    sid         INTEGER       NOT NULL,
    description TEXT          NOT NULL,
    date_alert  DATETIME      NOT NULL,
    sended      INTEGER       NOT NULL
);


-- Таблица: clientssteps
DROP TABLE IF EXISTS clientssteps;

CREATE TABLE clientssteps (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    role        VARCHAR (255) NOT NULL,
    consumer_id INTEGER       NOT NULL,
    agent_id    INTEGER       NOT NULL,
    step_name   VARCHAR (255) NOT NULL
);


-- Таблица: clientsstepshistory
DROP TABLE IF EXISTS clientsstepshistory;

CREATE TABLE clientsstepshistory (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    consumer_id INTEGER       NOT NULL,
    agent_id    INTEGER       NOT NULL,
    step_name   VARCHAR (255) NOT NULL,
    date        DATETIME      NOT NULL,
    date_end    DATETIME      NOT NULL
);


-- Таблица: consumer
DROP TABLE IF EXISTS consumer;

CREATE TABLE consumer (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    date_create DATETIME      NOT NULL,
    name        VARCHAR (255) NOT NULL,
    phone       VARCHAR (255) NOT NULL,
    role        VARCHAR (255) NOT NULL,
    group_id    INTEGER       NOT NULL,
    district_id INTEGER       NOT NULL,
    price       REAL          NOT NULL,
    prices_id   INTEGER       NOT NULL,
    address     TEXT          NOT NULL,
    area        REAL          NOT NULL,
    rooms       REAL          NOT NULL,
    manager_id  INTEGER       NOT NULL,
    info        TEXT          NOT NULL,
    status      INTEGER       NOT NULL,
    var_id      INTEGER       NOT NULL
                              DEFAULT (0) 
);


-- Таблица: consumergroup
DROP TABLE IF EXISTS consumergroup;

CREATE TABLE consumergroup (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    name        VARCHAR (255) NOT NULL,
    description TEXT          NOT NULL,
    info        TEXT          NOT NULL,
    status      INTEGER       NOT NULL
);


-- Таблица: consumerstatuses
DROP TABLE IF EXISTS consumerstatuses;

CREATE TABLE consumerstatuses (
    id            INTEGER       NOT NULL
                                PRIMARY KEY,
    name          VARCHAR (255) NOT NULL,
    status_number INTEGER       NOT NULL,
    info          TEXT          NOT NULL
);


-- Таблица: district
DROP TABLE IF EXISTS district;

CREATE TABLE district (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    date_create DATETIME      NOT NULL,
    name        VARCHAR (255) NOT NULL,
    description TEXT          NOT NULL,
    info        TEXT          NOT NULL,
    status      INTEGER       NOT NULL
);

INSERT INTO district (
                         id,
                         date_create,
                         name,
                         description,
                         info,
                         status
                     )
                     VALUES (
                         1,
                         '2019-05-02 12:31:40',
                         'Центр',
                         '',
                         '{}',
                         1
                     );

INSERT INTO district (
                         id,
                         date_create,
                         name,
                         description,
                         info,
                         status
                     )
                     VALUES (
                         2,
                         '2019-05-02 12:32:21',
                         'Микрорайон',
                         '',
                         '{}',
                         1
                     );

INSERT INTO district (
                         id,
                         date_create,
                         name,
                         description,
                         info,
                         status
                     )
                     VALUES (
                         4,
                         '2019-05-03 01:41:57',
                         'Район станции',
                         '',
                         '{}',
                         1
                     );

INSERT INTO district (
                         id,
                         date_create,
                         name,
                         description,
                         info,
                         status
                     )
                     VALUES (
                         5,
                         '2019-05-03 01:42:05',
                         'Венюково',
                         '',
                         '{}',
                         1
                     );

INSERT INTO district (
                         id,
                         date_create,
                         name,
                         description,
                         info,
                         status
                     )
                     VALUES (
                         6,
                         '2019-05-03 01:42:32',
                         'Центр',
                         '',
                         '{}',
                         1
                     );

INSERT INTO district (
                         id,
                         date_create,
                         name,
                         description,
                         info,
                         status
                     )
                     VALUES (
                         7,
                         '2019-05-03 01:42:46',
                         'Чеховский район',
                         '',
                         '{}',
                         1
                     );

INSERT INTO district (
                         id,
                         date_create,
                         name,
                         description,
                         info,
                         status
                     )
                     VALUES (
                         8,
                         '2019-05-03 02:45:23',
                         'Губернский',
                         ' ',
                         '{}',
                         1
                     );


-- Таблица: group
DROP TABLE IF EXISTS [group];

CREATE TABLE [group] (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    owner_id    INTEGER       NOT NULL,
    name        VARCHAR (255) NOT NULL,
    description TEXT          NOT NULL,
    info        TEXT          NOT NULL,
    status      INTEGER       NOT NULL
);


-- Таблица: manager
DROP TABLE IF EXISTS manager;

CREATE TABLE manager (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    date_create DATETIME      NOT NULL,
    user_id     INTEGER       NOT NULL,
    name        VARCHAR (255) NOT NULL,
    phone       VARCHAR (255) NOT NULL,
    role        VARCHAR (255) NOT NULL,
    group_id    INTEGER       NOT NULL,
    description TEXT          NOT NULL,
    info        TEXT          NOT NULL,
    status      INTEGER       NOT NULL
);


-- Таблица: managercheknote
DROP TABLE IF EXISTS managercheknote;

CREATE TABLE managercheknote (
    id      INTEGER NOT NULL
                    PRIMARY KEY,
    user_id INTEGER NOT NULL,
    note_id INTEGER NOT NULL,
    status  INTEGER NOT NULL
);


-- Таблица: managergroup
DROP TABLE IF EXISTS managergroup;

CREATE TABLE managergroup (
    id       INTEGER NOT NULL
                     PRIMARY KEY,
    user_id  INTEGER NOT NULL,
    group_id INTEGER NOT NULL
);


-- Таблица: managerstadies
DROP TABLE IF EXISTS managerstadies;

CREATE TABLE managerstadies (
    id                 INTEGER  NOT NULL
                                PRIMARY KEY,
    date_start         DATETIME NOT NULL,
    stadies_id         INTEGER  NOT NULL,
    manager_id         INTEGER  NOT NULL,
    consumer_id        INTEGER  NOT NULL,
    sub_stadies_id     INTEGER  NOT NULL,
    sub_sub_stadies_id INTEGER  NOT NULL
                                DEFAULT (0),
    status             INTEGER  NOT NULL
);


-- Таблица: managertask
DROP TABLE IF EXISTS managertask;

CREATE TABLE managertask (
    id      INTEGER NOT NULL
                    PRIMARY KEY,
    user_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL
);


-- Таблица: note
DROP TABLE IF EXISTS note;

CREATE TABLE note (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    name        VARCHAR (255) NOT NULL,
    note_text   TEXT          NOT NULL,
    description TEXT          NOT NULL,
    group_id    INTEGER       NOT NULL,
    info        TEXT          NOT NULL
);


-- Таблица: notegroup
DROP TABLE IF EXISTS notegroup;

CREATE TABLE notegroup (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    name        VARCHAR (255) NOT NULL,
    description TEXT          NOT NULL,
    info        TEXT          NOT NULL
);


-- Таблица: prices
DROP TABLE IF EXISTS prices;

CREATE TABLE prices (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    name        VARCHAR (255) NOT NULL,
    price_min   REAL          NOT NULL,
    price_max   REAL          NOT NULL,
    description TEXT          NOT NULL,
    info        TEXT          NOT NULL,
    status      INTEGER       NOT NULL
);


-- Таблица: report
DROP TABLE IF EXISTS report;

CREATE TABLE report (
    id          INTEGER NOT NULL
                        PRIMARY KEY,
    manager_id  INTEGER NOT NULL,
    report_text TEXT    NOT NULL,
    status      INTEGER NOT NULL,
    send        INTEGER NOT NULL
);


-- Таблица: stadies
DROP TABLE IF EXISTS stadies;

CREATE TABLE stadies (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    to_role     VARCHAR (255) NOT NULL,
    name        VARCHAR (255) NOT NULL,
    time_before INTEGER       NOT NULL,
    time_past   INTEGER       NOT NULL,
    details     TEXT          NOT NULL,
    steps       INTEGER       NOT NULL
                              DEFAULT (0) 
);

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        1,
                        'seller',
                        'Подготовка ко встрече',
                        2,
                        0,
                        '[{"id": 1, "sub_st_name": "Взять договор с приложениями", "do": "Взял"}, {"id": 2, "sub_st_name": "Взять анализ рынка по аналогичным объектам", "do": "Взял"}, {"id": 3, "sub_st_name": "Бахилы", "do": "Взял"}, {"id": 4, "sub_st_name": "Журнал С21", "do": "Взял"}, {"id": 5, "sub_st_name": "Паспорт", "do": "Взял"}, {"id": 6, "sub_st_name": "Визитки", "do": "Взял"}, {"id": 7, "sub_st_name": "Презентационная папка", "do": "Взял"}, {"id": 8, "sub_st_name": "Бейдж", "do": "Взял"}, {"id": 9, "sub_st_name": "Планшет/ручка/компас/рулетка/губка для обуви/щетка для одежды/влажные салфетки", "do": "Взял"}]',
                        1
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        2,
                        'seller',
                        'Встреча',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "Отказ от сотрудничества", "do": "клиент перемещается в общую базу"}, {"id": 2, "sub_st_name": "Подписан договор", "do": "клиент перемещается в стадию Подписан договор, предлагается задача Предпродажная подготовка"}, {"id": 3, "sub_st_name": "Готов подписать", "do": "клиент перемещается в стадию Проведена встреча, предлагается задача Подписание"}, {"id": 4, "sub_st_name": "Перенос", "do": "клиент остается в текущей стадии, предлагается задача Встреча"}]',
                        0
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        3,
                        'seller',
                        'Подготовка к подписанию',
                        2,
                        0,
                        '[{"id": 1, "sub_st_name": "Взять договор с приложениями", "do": "Взял"}, {"id": 2, "sub_st_name": "Взять анализ рынка по аналогичным объектам", "do": "Взял"}, {"id": 3, "sub_st_name": "Бахилы", "do": "Взял"}, {"id": 4, "sub_st_name": "Журнал С21", "do": "Взял"}, {"id": 5, "sub_st_name": "Паспорт", "do": "Взял"}, {"id": 6, "sub_st_name": "Визитки", "do": "Взял"}, {"id": 7, "sub_st_name": "Презентационная папка", "do": "Взял"}, {"id": 8, "sub_st_name": "Бейдж", "do": "Взял"}, {"id": 9, "sub_st_name": "Планшет/ручка/компас/рулетка/губка для обуви/щетка для одежды/влажные салфетки", "do": "Взял"}]',
                        1
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        4,
                        'seller',
                        'Подписание',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "Перенос", "do": "клиент остается в текущей стадии, предлагается задача Подписание"}, {"id": 2, "sub_st_name": "Отказ от сотрудничества", "do": "клиент перемещается в общую базу"}, {"id": 3, "sub_st_name": "Подписан договор", "do": "клиент перемещается в стадию Подписан договор, предлагается задача Предпродажная подготовка и последовательность вопросов"}]',
                        0
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        5,
                        'seller',
                        'Предпродажная подготовка',
                        0,
                        0,
                        '[{"id": 1, "sub_st_name": "Внести информацию по Договору в «Квартус»", "do": "Внес"}, {"id": 2, "sub_st_name": "Передай весь пакет документов по объекту офис-менеджеру", "do": "Передал"}, {"id": 3, "sub_st_name": "Передай информацию об объекте РОП для выгрузки в рекламные базы", "do": "Передал"}]',
                        1
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        6,
                        'seller',
                        'Предпродажная подготовка',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "Перенос", "do": "клиент остается в текущей стадии, предлагается задача Предпродажная подготовка"}, {"id": 2, "sub_st_name": "Отказ от сотрудничества", "do": "клиент перемещается в общую базу"}, {"id": 3, "sub_st_name": "Выполнена", "do": "клиент остается в текущей стадии, предлагается задача Запуск рекламы"}]',
                        0
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        7,
                        'seller',
                        'Запуск рекламы',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "Перенос", "do": "клиент остается в текущей стадии, предлагается задача Запуск рекламы"}, {"id": 2, "sub_st_name": "Отказ от сотрудничества", "do": "клиент перемещается в общую базу"}, {"id": 3, "sub_st_name": "Выполнена", "do": "клиент остается в текущей стадии, следующая задача не предлагается"}]',
                        0
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        8,
                        'seller',
                        'Напоминание об отчете',
                        0,
                        168,
                        '[{"id": 1, "sub_st_name": "Перенос", "do": "клиент остается в текущей стадии, предлагается задача Отчет"}, {"id": 2, "sub_st_name": "Отказ от сотрудничества", "do": "клиент перемещается в общую базу"}, {"id": 3, "sub_st_name": "Выполнена", "do": "клиент остается в текущей стадии, следующая задача не предлагается"}]',
                        0
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        9,
                        'seller',
                        'Корректировка цены',
                        0,
                        336,
                        '[{"id": 1, "sub_st_name": "Перенос", "do": "клиент остается в текущей стадии, предлагается задача Корректировка цены"}, {"id": 2, "sub_st_name": "Отказ от сотрудничества", "do": "клиент перемещается в общую базу"}, {"id": 3, "sub_st_name": "Выполнена", "do": "клиент остается в текущей стадии, следующая задача не предлагается"}]',
                        0
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        10,
                        'buyer',
                        'Подготовка к показу',
                        2,
                        0,
                        '[{"id": 1, "sub_st_name": "Контрольный звонок участникам показа", "do": "Сделал"}, {"id": 2, "sub_st_name": "Проверить «БАТАРЕЮ ПРОДАЖ»", "do": "Проверил"}, {"id": 3, "sub_st_name": "Бахилы", "do": "Взял"}, {"id": 4, "sub_st_name": "Планшет/ручка/компас/рулетка/губка для обуви/щетка для одежды/влажные салфетки", "do": "Взял"}, {"id": 5, "sub_st_name": "Журнал С21", "do": "Взял"}, {"id": 6, "sub_st_name": "Визитки", "do": "Взял"}, {"id": 7, "sub_st_name": "Бейдж", "do": "Взял"}, {"id": 8, "sub_st_name": "Листинг и лист осмотра объекта", "do": "Взял"}]',
                        1
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        11,
                        'buyer',
                        'Показ',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "Перенос", "do": "клиент остается в текущей стадии, предлагается задача Показ"}, {"id": 2, "sub_st_name": "Отказ от сотрудничества", "do": "клиент перемещается в общую базу"}, {"id": 3, "sub_st_name": "Объект подобран", "do": "клиент перемещается в стадию “Объект подобран, предлагается задача Аванс"}, {"id": 4, "sub_st_name": "Заключен договор", "do": "клиент переносится в стадию Проведен показ, ему присваивается параметр Договор на подбор, предлагается задача Показ. В дальнейшем при выполнении задачи Показ для клиентов с параметром Договор на подбор вариант Заключен договор не предлагается"}]',
                        0
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        12,
                        'buyer',
                        'Подготовка к авансу',
                        2,
                        0,
                        '[{"id": 1, "sub_st_name": "Запросить у продавца подтверждение намерения", "do": "Получил"}, {"id": 2, "sub_st_name": "Определить способ обеспечения обязательств (аванс или задаток)", "do": "Определил"}, {"id": 3, "sub_st_name": "Пригласить покупателя в офис", "do": "Пригласил"}, {"id": 4, "sub_st_name": "Предупредить ответственного по сопровождению сделки", "do": "Предупредил"}, {"id": 5, "sub_st_name": "Сделать копию паспорта покупателя (лицо, прописка, семейное положение)", "do": "Сделал"}, {"id": 6, "sub_st_name": "Подготовить бланки ДОГОВОРА АВАНСА", "do": "Подготовил"}, {"id": 7, "sub_st_name": "Подготовить документы продавца (договор и документы на объект)", "do": "Подготовил"}, {"id": 8, "sub_st_name": "Передать все документы юристу для заключения договора аванса и уточнения всех деталей сделки", "do": "Передал"}, {"id": 9, "sub_st_name": "Схема сделки", "do": "Передал"}, {"id": 10, "sub_st_name": "Обновление данных по объекту (актуальные выписки ЕГРН) - площадь, адрес, обременение", "do": "Подготовил"}]',
                        1
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        13,
                        'buyer',
                        'Аванс',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "Перенос", "do": "клиент остается в текущей стадии, предлагается задача “Аванс”"}, {"id": 2, "sub_st_name": "Отказ от сотрудничества", "do": "клиент перемещается в общую базу"}, {"id": 3, "sub_st_name": "Аванс внесен", "do": "клиент перемещается в стадию Внесен аванс, предлагается задача Сделка"}]',
                        0
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        14,
                        'buyer',
                        'Подготовка к сделке',
                        2,
                        0,
                        '[{"id": 1, "sub_st_name": "Контроль выполнения собственником обязательств по предварительному договору: документы/квартира", "do": "Проверил"}, {"id": 2, "sub_st_name": "Заказать ячейку/открытие аккредитивного счета", "do": "Заказал"}, {"id": 3, "sub_st_name": "Передать документы нотариусу или юристу компании для подготовки договора купли-продажи", "do": "Передал"}, {"id": 4, "sub_st_name": "Получить необходимые согласования для проведения сделки: одобрение ипотеки, распоряжение органов опеки, нотариальные согласия супругов", "do": "Получил"}, {"id": 5, "sub_st_name": "Направить сторонам сделки договор купли-продажи на согласование", "do": "Направил"}, {"id": 6, "sub_st_name": "Подтвердить письменно  место, время, список необходимых документов для сделки, а также обозначить суммы расходов по сделке участникам", "do": "Подтвердил"}, {"id": 7, "sub_st_name": "Контрольный звонок участникам сделки: время, место, документы", "do": "Сделал"}, {"id": 8, "sub_st_name": "Бумага, ручки, форма расписки, вода в бутылках, стаканчики, шоколад", "do": "Взял"}, {"id": 9, "sub_st_name": "Акты выполненных работ с клиентом, приходный кассовый ордер, гарантийные обязательства", "do": "Взял"}, {"id": 10, "sub_st_name": "Предупредить бухгалтерию о дате, времени и порядке проведения расчетов по сделке, сумме", "do": "Предупредил"}]',
                        1
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        15,
                        'buyer',
                        'Сделка',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "Перенос", "do": "клиент остается в текущей стадии, предлагается задача Сделка"}, {"id": 2, "sub_st_name": "Отказ от сотрудничества", "do": "клиент перемещается в общую базу"}, {"id": 3, "sub_st_name": "Документы поданы", "do": "пользователю предлагается указать из подходящих по параметрам клиентов продавцов того по которому завершена сделка. Клиент-покупатель перемещается в стадию Сделка завершена, клиент-продавец перемещается в стадию Объект продан, новая задача не предлагается."}]',
                        0
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        16,
                        'seller',
                        'Реклама',
                        0,
                        0,
                        '[{"id": 1, "sub_st_name": "Проверить рекламу по объекту", "do": "Проверил"}, {"id": 2, "sub_st_name": "Презентация объекта в корпоративном чате и  партнерам-агентам", "do": "Презентовал"}, {"id": 3, "sub_st_name": "Построить БАТАРЕЮ  ПРОДАЖ по данному объекту", "do": "Построил"}, {"id": 4, "sub_st_name": "Прозвонить всю БАТАРЕЮ ПРОДАЖ", "do": "Прозвонил"}, {"id": 5, "sub_st_name": "Расклейка объявлений ПРОДАЕТСЯ", "do": "Расклеил"}]',
                        1
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        17,
                        'seller',
                        'Не назначено',
                        0,
                        0,
                        '[]',
                        0
                    );

INSERT INTO stadies (
                        id,
                        to_role,
                        name,
                        time_before,
                        time_past,
                        details,
                        steps
                    )
                    VALUES (
                        18,
                        'buyer',
                        'Сделка завершена',
                        0,
                        0,
                        '[]',
                        0
                    );


-- Таблица: task
DROP TABLE IF EXISTS task;

CREATE TABLE task (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    creator_id  INTEGER       NOT NULL,
    name        VARCHAR (255) NOT NULL,
    task_text   TEXT          NOT NULL,
    description TEXT          NOT NULL,
    date_create DATE          NOT NULL,
    date_start  DATETIME      NOT NULL,
    date_end    DATETIME      NOT NULL,
    info        TEXT          NOT NULL,
    status      INTEGER       NOT NULL
);


-- Таблица: tempconsumers
DROP TABLE IF EXISTS tempconsumers;

CREATE TABLE tempconsumers (
    id          INTEGER NOT NULL
                        PRIMARY KEY,
    consumer_id INTEGER NOT NULL,
    agent_id    INTEGER NOT NULL
);


-- Таблица: town
DROP TABLE IF EXISTS town;

CREATE TABLE town (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    date_create DATETIME      NOT NULL,
    name        VARCHAR (255) NOT NULL,
    description TEXT          NOT NULL,
    info        TEXT          NOT NULL,
    status      INTEGER       NOT NULL
);

INSERT INTO town (
                     id,
                     date_create,
                     name,
                     description,
                     info,
                     status
                 )
                 VALUES (
                     1,
                     '2019-05-02 12:30:06',
                     'Троицк',
                     '',
                     '{}',
                     1
                 );

INSERT INTO town (
                     id,
                     date_create,
                     name,
                     description,
                     info,
                     status
                 )
                 VALUES (
                     2,
                     '2019-05-02 12:30:24',
                     'Чехов',
                     '',
                     '{}',
                     1
                 );


-- Таблица: towndistricts
DROP TABLE IF EXISTS towndistricts;

CREATE TABLE towndistricts (
    id          INTEGER NOT NULL
                        PRIMARY KEY,
    town_id     INTEGER NOT NULL,
    district_id INTEGER NOT NULL
);

INSERT INTO towndistricts (
                              id,
                              town_id,
                              district_id
                          )
                          VALUES (
                              1,
                              1,
                              1
                          );

INSERT INTO towndistricts (
                              id,
                              town_id,
                              district_id
                          )
                          VALUES (
                              2,
                              1,
                              2
                          );

INSERT INTO towndistricts (
                              id,
                              town_id,
                              district_id
                          )
                          VALUES (
                              4,
                              2,
                              4
                          );

INSERT INTO towndistricts (
                              id,
                              town_id,
                              district_id
                          )
                          VALUES (
                              5,
                              2,
                              5
                          );

INSERT INTO towndistricts (
                              id,
                              town_id,
                              district_id
                          )
                          VALUES (
                              6,
                              2,
                              6
                          );

INSERT INTO towndistricts (
                              id,
                              town_id,
                              district_id
                          )
                          VALUES (
                              7,
                              2,
                              7
                          );

INSERT INTO towndistricts (
                              id,
                              town_id,
                              district_id
                          )
                          VALUES (
                              8,
                              2,
                              8
                          );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
