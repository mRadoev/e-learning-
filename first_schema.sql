-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


-- -----------------------------------------------------
-- Schema e-learning
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `e-learning` DEFAULT CHARACTER SET utf8 ;
USE `e-learning` ;

-- -----------------------------------------------------
-- Table `e-learning`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`courses` (
  `course_id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `description` TEXT NOT NULL,
  `objectives` VARCHAR(45) NOT NULL,
  `owner` INT(11) NOT NULL,
  `tags` TEXT NOT NULL,
  `status` TINYINT(4) NOT NULL,
  `student_rating` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) ,
  UNIQUE INDEX `course_id_UNIQUE` (`course_id` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `e-learning`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `role` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `linkedin` VARCHAR(45) NULL DEFAULT 'None',
  `phone_number` VARCHAR(45) NULL DEFAULT 'None',
  `password` VARCHAR(45) NOT NULL,
  `photo` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `id_UNIQUE` (`user_id` ASC) ,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `e-learning`.`courses_has_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`courses_has_users` (
  `course_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `has_control` TINYINT(4) NULL DEFAULT NULL,
  `has_access` TINYINT(4) NULL DEFAULT NULL,
  `student_rating` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`course_id`, `user_id`),
  INDEX `fk_courses_has_users_users1_idx` (`user_id` ASC) ,
  INDEX `fk_courses_has_users_courses1_idx` (`course_id` ASC) ,
  CONSTRAINT `fk_courses_has_users_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `e-learning`.`courses` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_courses_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `e-learning`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `e-learning`.`sections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`sections` (
  `course_id` INT(11) NOT NULL,
  `section_id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `content` VARCHAR(45) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `link` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`section_id`),
  UNIQUE INDEX `section_id_UNIQUE` (`section_id` ASC) ,
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) ,
  INDEX `fk_section_courses1_idx` (`course_id` ASC) ,
  CONSTRAINT `fk_section_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `e-learning`.`courses` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
