--
-- ���� ������������ � ������� SQLiteStudio v3.2.1 � �� ��� 17 08:25:51 2019
--
-- �������������� ��������� ������: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: admin
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


-- �������: adminconsumerstata
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


-- �������: agentconsumertask
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


-- �������: clientssteps
DROP TABLE IF EXISTS clientssteps;

CREATE TABLE clientssteps (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    role        VARCHAR (255) NOT NULL,
    consumer_id INTEGER       NOT NULL,
    agent_id    INTEGER       NOT NULL,
    step_name   VARCHAR (255) NOT NULL
);


-- �������: clientsstepshistory
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


-- �������: consumer
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


-- �������: consumergroup
DROP TABLE IF EXISTS consumergroup;

CREATE TABLE consumergroup (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    name        VARCHAR (255) NOT NULL,
    description TEXT          NOT NULL,
    info        TEXT          NOT NULL,
    status      INTEGER       NOT NULL
);


-- �������: consumerstatuses
DROP TABLE IF EXISTS consumerstatuses;

CREATE TABLE consumerstatuses (
    id            INTEGER       NOT NULL
                                PRIMARY KEY,
    name          VARCHAR (255) NOT NULL,
    status_number INTEGER       NOT NULL,
    info          TEXT          NOT NULL
);


-- �������: district
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
                         '�����',
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
                         '����������',
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
                         '����� �������',
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
                         '��������',
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
                         '�����',
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
                         '��������� �����',
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
                         '����������',
                         ' ',
                         '{}',
                         1
                     );


-- �������: group
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


-- �������: manager
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


-- �������: managercheknote
DROP TABLE IF EXISTS managercheknote;

CREATE TABLE managercheknote (
    id      INTEGER NOT NULL
                    PRIMARY KEY,
    user_id INTEGER NOT NULL,
    note_id INTEGER NOT NULL,
    status  INTEGER NOT NULL
);


-- �������: managergroup
DROP TABLE IF EXISTS managergroup;

CREATE TABLE managergroup (
    id       INTEGER NOT NULL
                     PRIMARY KEY,
    user_id  INTEGER NOT NULL,
    group_id INTEGER NOT NULL
);


-- �������: managerstadies
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


-- �������: managertask
DROP TABLE IF EXISTS managertask;

CREATE TABLE managertask (
    id      INTEGER NOT NULL
                    PRIMARY KEY,
    user_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL
);


-- �������: note
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


-- �������: notegroup
DROP TABLE IF EXISTS notegroup;

CREATE TABLE notegroup (
    id          INTEGER       NOT NULL
                              PRIMARY KEY,
    name        VARCHAR (255) NOT NULL,
    description TEXT          NOT NULL,
    info        TEXT          NOT NULL
);


-- �������: prices
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


-- �������: report
DROP TABLE IF EXISTS report;

CREATE TABLE report (
    id          INTEGER NOT NULL
                        PRIMARY KEY,
    manager_id  INTEGER NOT NULL,
    report_text TEXT    NOT NULL,
    status      INTEGER NOT NULL,
    send        INTEGER NOT NULL
);


-- �������: stadies
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
                        '���������� �� �������',
                        2,
                        0,
                        '[{"id": 1, "sub_st_name": "����� ������� � ������������", "do": "����"}, {"id": 2, "sub_st_name": "����� ������ ����� �� ����������� ��������", "do": "����"}, {"id": 3, "sub_st_name": "������", "do": "����"}, {"id": 4, "sub_st_name": "������ �21", "do": "����"}, {"id": 5, "sub_st_name": "�������", "do": "����"}, {"id": 6, "sub_st_name": "�������", "do": "����"}, {"id": 7, "sub_st_name": "��������������� �����", "do": "����"}, {"id": 8, "sub_st_name": "�����", "do": "����"}, {"id": 9, "sub_st_name": "�������/�����/������/�������/����� ��� �����/����� ��� ������/������� ��������", "do": "����"}]',
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
                        '�������',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "����� �� ��������������", "do": "������ ������������ � ����� ����"}, {"id": 2, "sub_st_name": "�������� �������", "do": "������ ������������ � ������ �������� �������, ������������ ������ ������������� ����������"}, {"id": 3, "sub_st_name": "����� ���������", "do": "������ ������������ � ������ ��������� �������, ������������ ������ ����������"}, {"id": 4, "sub_st_name": "�������", "do": "������ �������� � ������� ������, ������������ ������ �������"}]',
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
                        '���������� � ����������',
                        2,
                        0,
                        '[{"id": 1, "sub_st_name": "����� ������� � ������������", "do": "����"}, {"id": 2, "sub_st_name": "����� ������ ����� �� ����������� ��������", "do": "����"}, {"id": 3, "sub_st_name": "������", "do": "����"}, {"id": 4, "sub_st_name": "������ �21", "do": "����"}, {"id": 5, "sub_st_name": "�������", "do": "����"}, {"id": 6, "sub_st_name": "�������", "do": "����"}, {"id": 7, "sub_st_name": "��������������� �����", "do": "����"}, {"id": 8, "sub_st_name": "�����", "do": "����"}, {"id": 9, "sub_st_name": "�������/�����/������/�������/����� ��� �����/����� ��� ������/������� ��������", "do": "����"}]',
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
                        '����������',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "�������", "do": "������ �������� � ������� ������, ������������ ������ ����������"}, {"id": 2, "sub_st_name": "����� �� ��������������", "do": "������ ������������ � ����� ����"}, {"id": 3, "sub_st_name": "�������� �������", "do": "������ ������������ � ������ �������� �������, ������������ ������ ������������� ���������� � ������������������ ��������"}]',
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
                        '������������� ����������',
                        0,
                        0,
                        '[{"id": 1, "sub_st_name": "������ ���������� �� �������� � ��������", "do": "����"}, {"id": 2, "sub_st_name": "������� ���� ����� ���������� �� ������� ����-���������", "do": "�������"}, {"id": 3, "sub_st_name": "������� ���������� �� ������� ��� ��� �������� � ��������� ����", "do": "�������"}]',
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
                        '������������� ����������',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "�������", "do": "������ �������� � ������� ������, ������������ ������ ������������� ����������"}, {"id": 2, "sub_st_name": "����� �� ��������������", "do": "������ ������������ � ����� ����"}, {"id": 3, "sub_st_name": "���������", "do": "������ �������� � ������� ������, ������������ ������ ������ �������"}]',
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
                        '������ �������',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "�������", "do": "������ �������� � ������� ������, ������������ ������ ������ �������"}, {"id": 2, "sub_st_name": "����� �� ��������������", "do": "������ ������������ � ����� ����"}, {"id": 3, "sub_st_name": "���������", "do": "������ �������� � ������� ������, ��������� ������ �� ������������"}]',
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
                        '����������� �� ������',
                        0,
                        168,
                        '[{"id": 1, "sub_st_name": "�������", "do": "������ �������� � ������� ������, ������������ ������ �����"}, {"id": 2, "sub_st_name": "����� �� ��������������", "do": "������ ������������ � ����� ����"}, {"id": 3, "sub_st_name": "���������", "do": "������ �������� � ������� ������, ��������� ������ �� ������������"}]',
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
                        '������������� ����',
                        0,
                        336,
                        '[{"id": 1, "sub_st_name": "�������", "do": "������ �������� � ������� ������, ������������ ������ ������������� ����"}, {"id": 2, "sub_st_name": "����� �� ��������������", "do": "������ ������������ � ����� ����"}, {"id": 3, "sub_st_name": "���������", "do": "������ �������� � ������� ������, ��������� ������ �� ������������"}]',
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
                        '���������� � ������',
                        2,
                        0,
                        '[{"id": 1, "sub_st_name": "����������� ������ ���������� ������", "do": "������"}, {"id": 2, "sub_st_name": "��������� �������� �����ƻ", "do": "��������"}, {"id": 3, "sub_st_name": "������", "do": "����"}, {"id": 4, "sub_st_name": "�������/�����/������/�������/����� ��� �����/����� ��� ������/������� ��������", "do": "����"}, {"id": 5, "sub_st_name": "������ �21", "do": "����"}, {"id": 6, "sub_st_name": "�������", "do": "����"}, {"id": 7, "sub_st_name": "�����", "do": "����"}, {"id": 8, "sub_st_name": "������� � ���� ������� �������", "do": "����"}]',
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
                        '�����',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "�������", "do": "������ �������� � ������� ������, ������������ ������ �����"}, {"id": 2, "sub_st_name": "����� �� ��������������", "do": "������ ������������ � ����� ����"}, {"id": 3, "sub_st_name": "������ ��������", "do": "������ ������������ � ������ ������� ��������, ������������ ������ �����"}, {"id": 4, "sub_st_name": "�������� �������", "do": "������ ����������� � ������ �������� �����, ��� ������������� �������� ������� �� ������, ������������ ������ �����. � ���������� ��� ���������� ������ ����� ��� �������� � ���������� ������� �� ������ ������� �������� ������� �� ������������"}]',
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
                        '���������� � ������',
                        2,
                        0,
                        '[{"id": 1, "sub_st_name": "��������� � �������� ������������� ���������", "do": "�������"}, {"id": 2, "sub_st_name": "���������� ������ ����������� ������������ (����� ��� �������)", "do": "���������"}, {"id": 3, "sub_st_name": "���������� ���������� � ����", "do": "���������"}, {"id": 4, "sub_st_name": "������������ �������������� �� ������������� ������", "do": "�����������"}, {"id": 5, "sub_st_name": "������� ����� �������� ���������� (����, ��������, �������� ���������)", "do": "������"}, {"id": 6, "sub_st_name": "����������� ������ �������� ������", "do": "����������"}, {"id": 7, "sub_st_name": "����������� ��������� �������� (������� � ��������� �� ������)", "do": "����������"}, {"id": 8, "sub_st_name": "�������� ��� ��������� ������ ��� ���������� �������� ������ � ��������� ���� ������� ������", "do": "�������"}, {"id": 9, "sub_st_name": "����� ������", "do": "�������"}, {"id": 10, "sub_st_name": "���������� ������ �� ������� (���������� ������� ����) - �������, �����, �����������", "do": "����������"}]',
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
                        '�����',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "�������", "do": "������ �������� � ������� ������, ������������ ������ ������"}, {"id": 2, "sub_st_name": "����� �� ��������������", "do": "������ ������������ � ����� ����"}, {"id": 3, "sub_st_name": "����� ������", "do": "������ ������������ � ������ ������ �����, ������������ ������ ������"}]',
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
                        '���������� � ������',
                        2,
                        0,
                        '[{"id": 1, "sub_st_name": "�������� ���������� ������������� ������������ �� ���������������� ��������: ���������/��������", "do": "��������"}, {"id": 2, "sub_st_name": "�������� ������/�������� �������������� �����", "do": "�������"}, {"id": 3, "sub_st_name": "�������� ��������� ��������� ��� ������ �������� ��� ���������� �������� �����-�������", "do": "�������"}, {"id": 4, "sub_st_name": "�������� ����������� ������������ ��� ���������� ������: ��������� �������, ������������ ������� �����, ������������ �������� ��������", "do": "�������"}, {"id": 5, "sub_st_name": "��������� �������� ������ ������� �����-������� �� ������������", "do": "��������"}, {"id": 6, "sub_st_name": "����������� ���������  �����, �����, ������ ����������� ���������� ��� ������, � ����� ���������� ����� �������� �� ������ ����������", "do": "����������"}, {"id": 7, "sub_st_name": "����������� ������ ���������� ������: �����, �����, ���������", "do": "������"}, {"id": 8, "sub_st_name": "������, �����, ����� ��������, ���� � ��������, ����������, �������", "do": "����"}, {"id": 9, "sub_st_name": "���� ����������� ����� � ��������, ��������� �������� �����, ����������� �������������", "do": "����"}, {"id": 10, "sub_st_name": "������������ ����������� � ����, ������� � ������� ���������� �������� �� ������, �����", "do": "�����������"}]',
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
                        '������',
                        0,
                        1,
                        '[{"id": 1, "sub_st_name": "�������", "do": "������ �������� � ������� ������, ������������ ������ ������"}, {"id": 2, "sub_st_name": "����� �� ��������������", "do": "������ ������������ � ����� ����"}, {"id": 3, "sub_st_name": "��������� ������", "do": "������������ ������������ ������� �� ���������� �� ���������� �������� ��������� ���� �� �������� ��������� ������. ������-���������� ������������ � ������ ������ ���������, ������-�������� ������������ � ������ ������ ������, ����� ������ �� ������������."}]',
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
                        '�������',
                        0,
                        0,
                        '[{"id": 1, "sub_st_name": "��������� ������� �� �������", "do": "��������"}, {"id": 2, "sub_st_name": "����������� ������� � ������������� ���� �  ���������-�������", "do": "�����������"}, {"id": 3, "sub_st_name": "��������� �������  ������ �� ������� �������", "do": "��������"}, {"id": 4, "sub_st_name": "���������� ��� ������� ������", "do": "���������"}, {"id": 5, "sub_st_name": "��������� ���������� ���������", "do": "��������"}]',
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
                        '�� ���������',
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
                        '������ ���������',
                        0,
                        0,
                        '[]',
                        0
                    );


-- �������: task
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


-- �������: tempconsumers
DROP TABLE IF EXISTS tempconsumers;

CREATE TABLE tempconsumers (
    id          INTEGER NOT NULL
                        PRIMARY KEY,
    consumer_id INTEGER NOT NULL,
    agent_id    INTEGER NOT NULL
);


-- �������: town
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
                     '������',
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
                     '�����',
                     '',
                     '{}',
                     1
                 );


-- �������: towndistricts
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
