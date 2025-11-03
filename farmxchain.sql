SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `farmers` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `farmers`;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `addagroproducts`;
DROP TABLE IF EXISTS `trig`;
DROP TABLE IF EXISTS `farming`;
DROP TABLE IF EXISTS `register`;
DROP TABLE IF EXISTS `test`;
DROP TABLE IF EXISTS `user`;
SET FOREIGN_KEY_CHECKS = 1;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


CREATE TABLE `register` (
  `rid` INT NOT NULL AUTO_INCREMENT,
  `farmername` VARCHAR(100) NOT NULL,
  `adharnumber` VARCHAR(50) DEFAULT NULL,
  `age` INT DEFAULT NULL,
  `gender` VARCHAR(20) DEFAULT NULL,
  `phonenumber` VARCHAR(30) DEFAULT NULL,
  `address` VARCHAR(255) DEFAULT NULL,
  `farming` VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (`rid`),
  UNIQUE KEY `uq_register_adharnumber` (`adharnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `farming` (
  `fid` INT NOT NULL AUTO_INCREMENT,
  `farmingtype` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`fid`),
  UNIQUE KEY `uq_farming_type` (`farmingtype`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `addagroproducts` (
  `pid` INT NOT NULL AUTO_INCREMENT,
  `productname` VARCHAR(150) NOT NULL,
  `productdesc` TEXT DEFAULT NULL,
  `price` INT NOT NULL, 
  `owner_id` INT DEFAULT NULL, 
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`pid`),
  KEY `fk_product_owner_idx` (`owner_id`),
  CONSTRAINT `fk_product_owner` FOREIGN KEY (`owner_id`) REFERENCES `register` (`rid`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `trig` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fid` INT NOT NULL, 
  `action` VARCHAR(200) NOT NULL,
  `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_trig_farmer_idx` (`fid`),
  CONSTRAINT `fk_trig_farmer` FOREIGN KEY (`fid`) REFERENCES `register` (`rid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `test` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(80) NOT NULL,
  `email` VARCHAR(120) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_user_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DELIMITER $$
CREATE TRIGGER `register_after_insert`
AFTER INSERT ON `register`
FOR EACH ROW
BEGIN
  INSERT INTO trig (fid, action, timestamp) VALUES (NEW.rid, 'Farmer Inserted', NOW());
END$$

CREATE TRIGGER `register_after_update`
AFTER UPDATE ON `register`
FOR EACH ROW
BEGIN
  INSERT INTO trig (fid, action, timestamp) VALUES (NEW.rid, 'Farmer Updated', NOW());
END$$

CREATE TRIGGER `register_before_delete`
BEFORE DELETE ON `register`
FOR EACH ROW
BEGIN
  INSERT INTO trig (fid, action, timestamp) VALUES (OLD.rid, 'Farmer Deleted', NOW());
END$$
DELIMITER ;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
