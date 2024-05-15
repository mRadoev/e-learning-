-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema E-learning
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema E-learning
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `E-learning` DEFAULT CHARACTER SET utf8 ;
USE `E-learning` ;

-- -----------------------------------------------------
-- Table `E-learning`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `E-learning`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `role` VARCHAR(45) NOT NULL DEFAULT 'guest',
  `e-mail` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `photo` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `E-learning`.`courses_has_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `E-learning`.`courses_has_users` (
  `user_id` INT NOT NULL,
  `course_id` INT NOT NULL,
  `student_rating` VARCHAR(45) NOT NULL DEFAULT 'None',
  `has_control` VARCHAR(45) NULL,
  `has_access` VARCHAR(45) NULL,
  PRIMARY KEY (`user_id`, `course_id`, `student_rating`),
  INDEX `fk_courses_has_users_users2_idx` (`user_id` ASC) ,
  INDEX `fk_courses_has_users_courses1_idx` (`course_id` ASC) ,
  CONSTRAINT `fk_courses_has_users_users2`
    FOREIGN KEY (`user_id`)
    REFERENCES `E-learning`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_courses_has_users_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `E-learning`.`courses` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `E-learning`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `E-learning`.`courses` (
  `course_id` INT NOT NULL AUTO_INCREMENT,
  `title` INT NOT NULL,
  `description` TEXT NOT NULL,
  `objectives` VARCHAR(45) NOT NULL,
  `owner(teacher)` VARCHAR(45) NOT NULL,
  `tags` VARCHAR(45) NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  `student_rating` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`course_id`, `student_rating`),
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) ,
  INDEX `fk_courses_courses_has_users1_idx` (`student_rating` ASC) ,
  CONSTRAINT `fk_courses_courses_has_users1`
    FOREIGN KEY (`student_rating`)
    REFERENCES `E-learning`.`courses_has_users` (`student_rating`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `E-learning`.`sections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `E-learning`.`sections` (
  `section_id` INT NOT NULL AUTO_INCREMENT,
  `course_id` INT NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `content` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  `link` VARCHAR(45) NULL,
  PRIMARY KEY (`section_id`),
  INDEX `fk_section_courses1_idx` (`course_id` ASC) ,
  CONSTRAINT `fk_section_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `E-learning`.`courses` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
