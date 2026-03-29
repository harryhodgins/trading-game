CREATE DATABASE `trading_sim`;

USE trading_sim;

CREATE TABLE `orders` (
    `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `timestamp` DATETIME(6) NOT NULL,
    `quantity` int(11) NOT NULL,
    `price` DECIMAL(10,2) NOT NULL,
    `type` VARCHAR(10) NOT NULL
);

CREATE TABLE `portfolio` (
    `ticker` VARCHAR(4) NOT NULL,
    `quantity` int(11)
);