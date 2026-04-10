CREATE DATABASE `trading_sim`;

USE trading_sim;

CREATE TABLE `players` (
    `player_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `player_name` VARCHAR(64) NOT NULL,
    `balance` DECIMAL(10, 2) NOT NULL DEFAULT 10000.00,
    `is_bot` BOOLEAN NOT NULL DEFAULT FALSE,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `orders` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `quantity` INT NOT NULL,
    `value` DECIMAL(10, 2) NOT NULL,
    `price` DECIMAL(10, 2) NOT NULL,
    `type` ENUM('BUY', 'SELL') NOT NULL,
    `ticker` VARCHAR(10) NOT NULL,
    `player_id` INT NOT NULL,
    FOREIGN KEY (`player_id`) REFERENCES `players`(`player_id`)
);

CREATE TABLE `portfolio` (
    `ticker` VARCHAR(10) NOT NULL,
    `quantity` INT NOT NULL DEFAULT 0,
    `player_id` INT NOT NULL,
    PRIMARY KEY (`ticker`, `player_id`),
    FOREIGN KEY (`player_id`) REFERENCES `players`(`player_id`)
);