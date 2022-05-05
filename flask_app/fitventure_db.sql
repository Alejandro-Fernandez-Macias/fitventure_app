-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema fitventure_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `fitventure_db` ;

-- -----------------------------------------------------
-- Schema fitventure_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `fitventure_db` DEFAULT CHARACTER SET utf8 ;
USE `fitventure_db` ;

-- -----------------------------------------------------
-- Table `fitventure_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitventure_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL DEFAULT NULL,
  `last_name` VARCHAR(255) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `confirm_password` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `fitventure_db`.`workouts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitventure_db`.`workouts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `length` VARCHAR(25) NULL DEFAULT NULL,
  `type` VARCHAR(255) NULL DEFAULT NULL,
  `instructions` TEXT NULL DEFAULT NULL,
  `times_worked_out` INT NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_workouts_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_workouts_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `fitventure_db`.`users` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `fitventure_db`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitventure_db`.`likes` (
  `user_id` INT NOT NULL,
  `workout_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `workout_id`),
  INDEX `fk_users_has_workouts_workouts1_idx` (`workout_id` ASC) VISIBLE,
  INDEX `fk_users_has_workouts_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_workouts_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `fitventure_db`.`users` (`id`),
  CONSTRAINT `fk_users_has_workouts_workouts1`
    FOREIGN KEY (`workout_id`)
    REFERENCES `fitventure_db`.`workouts` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `fitventure_db`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fitventure_db`.`messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `sender_id` INT NULL DEFAULT NULL,
  `receiver_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `sender_id_idx` (`sender_id` ASC) VISIBLE,
  INDEX `receiver_id_idx` (`receiver_id` ASC) VISIBLE,
  CONSTRAINT `receiver_id`
    FOREIGN KEY (`receiver_id`)
    REFERENCES `fitventure_db`.`users` (`id`),
  CONSTRAINT `sender_id`
    FOREIGN KEY (`sender_id`)
    REFERENCES `fitventure_db`.`users` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
