
CREATE TABLE building (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE floor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number VARCHAR(50) NOT NULL,
    building_id INTEGER,
    FOREIGN KEY (building_id) REFERENCES building(id)
);

CREATE TABLE room_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE room (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number VARCHAR(50) NOT NULL,
    room_category_id INTEGER NOT NULL,
    floor_id INTEGER,
    FOREIGN KEY (room_category_id) REFERENCES room_category(id),
    FOREIGN KEY (floor_id) REFERENCES floor(id)
);

CREATE TABLE projector (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    serial_number VARCHAR(100) NOT NULL
);

CREATE TABLE room_projector (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER,
    projector_id INTEGER,
    FOREIGN KEY (room_id) REFERENCES room(id),
    FOREIGN KEY (projector_id) REFERENCES projector(id)
);

CREATE TABLE person_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE person (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    person_type_id INTEGER NOT NULL,
    FOREIGN KEY (person_type_id) REFERENCES person_type(id)
);

CREATE TABLE keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    collection_date DATE,
    person_id INTEGER,
    room_id INTEGER NOT NULL,
    FOREIGN KEY (person_id) REFERENCES person(id),
    FOREIGN KEY (room_id) REFERENCES room(id)
);

CREATE INDEX idx_building_id ON floor(building_id);
CREATE INDEX idx_room_category_id ON room(room_category_id);
CREATE INDEX idx_floor_id ON room(floor_id);
CREATE INDEX idx_room_id ON room_projector(room_id);
CREATE INDEX idx_projector_id ON room_projector(projector_id);
CREATE INDEX idx_person_type_id ON person(person_type_id);
CREATE INDEX idx_person_id ON keys(person_id);
CREATE INDEX idx_room_id_keys ON keys(room_id);

INSERT INTO building (name) VALUES
('Building A'),
('Building B'),
('Building C'),
('Building D'),
('Building E');

INSERT INTO floor (number, building_id) VALUES
('1', 1),
('2', 1),
('1', 2),
('3', 3),
('2', 4);

INSERT INTO room_category (name) VALUES
('Sala wykładowa'),
('Laboratorium'),
('Pomieszczenie techniczne'),
('Aula');

INSERT INTO room (number, room_category_id, floor_id) VALUES
('101', 1, 1),
('102', 2, 2),
('201', 3, 3),
('301', 4, 4),
('401', 1, 5);

INSERT INTO projector (serial_number) VALUES
('SN12345'),
('SN12346'),
('SN12347'),
('SN12348'),
('SN12349');

INSERT INTO room_projector (room_id, projector_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

INSERT INTO person_type (name) VALUES
('Student'),
('Pracownik');

INSERT INTO person (first_name, last_name, person_type_id) VALUES
('Jan', 'Kowalski', 1),
('Anna', 'Nowak', 2),
('Piotr', 'Wójcik', 1),
('Katarzyna', 'Lewandowska', 2),
('Marek', 'Zieliński', 1);

INSERT INTO keys (collection_date, person_id, room_id) VALUES
('2025-03-10', 1, 1),
('2025-03-11', 2, 2),
('2025-03-12', 3, 3),
('2025-03-13', 4, 4),
('2025-03-14', 5, 5);
