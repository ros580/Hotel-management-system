CREATE DATABASE hotel_db;
USE hotel_db;

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(15),
    address TEXT,
    check_in DATE,
    check_out DATE,
    room_no INT
);

CREATE TABLE rooms (
    room_no INT PRIMARY KEY,
    type VARCHAR(20),
    price DECIMAL(10,2),
    status VARCHAR(10) DEFAULT 'available'
);

-- Sample rooms
INSERT INTO rooms (room_no, type, price) VALUES 
(101, 'Single', 1000.00),
(102, 'Double', 1800.00),
(103, 'Suite', 3000.00);
