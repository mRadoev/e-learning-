-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema e-learning
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `e-learning` DEFAULT CHARACTER SET latin1 ;
USE `e-learning` ;

-- -----------------------------------------------------
-- Table `e-learning`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `role` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `password` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `id_UNIQUE` (`user_id` ASC) ,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `e-learning`.`teachers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`teachers` (
  `teacher_id` INT(11) NOT NULL,
  `linkedin` VARCHAR(255) NULL DEFAULT NULL,
  `phone_number` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`teacher_id`),
  INDEX `user_id` (`teacher_id` ASC) ,
  CONSTRAINT `teachers_ibfk_1`
    FOREIGN KEY (`teacher_id`)
    REFERENCES `e-learning`.`users` (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `e-learning`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`courses` (
  `course_id` INT(11) NOT NULL AUTO_INCREMENT,
  `owner_id` INT(11) NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `description` TEXT NOT NULL,
  `objectives` VARCHAR(45) NOT NULL,
  `tags` TEXT NOT NULL,
  `status` TINYINT(4) NOT NULL,
  `owner_name` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) ,
  UNIQUE INDEX `course_id_UNIQUE` (`course_id` ASC) ,
  INDEX `fk_courses_teachers1_idx` (`owner_id` ASC) ,
  CONSTRAINT `fk_courses_teachers1`
    FOREIGN KEY (`owner_id`)
    REFERENCES `e-learning`.`teachers` (`teacher_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `e-learning`.`emails`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`emails` (
  `email_id` INT(11) NOT NULL AUTO_INCREMENT,
  `sender_id` INT(11) NOT NULL,
  `recipient_id` INT(11) NOT NULL,
  `course_id` INT(11) NOT NULL,
  `response` TINYINT(4) NULL DEFAULT NULL,
  PRIMARY KEY (`email_id`),
  UNIQUE INDEX `email_id_UNIQUE` (`email_id` ASC) ,
  INDEX `fk_emails_users1_idx` (`sender_id` ASC) ,
  INDEX `fk_emails_users2_idx` (`recipient_id` ASC) ,
  INDEX `fk_emails_courses1_idx` (`course_id` ASC) ,
  CONSTRAINT `fk_emails_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `e-learning`.`courses` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_emails_users1`
    FOREIGN KEY (`sender_id`)
    REFERENCES `e-learning`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_emails_users2`
    FOREIGN KEY (`recipient_id`)
    REFERENCES `e-learning`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `e-learning`.`sections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`sections` (
  `section_id` INT(11) NOT NULL AUTO_INCREMENT,
  `course_id` INT(11) NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `content` TEXT NOT NULL,
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
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `e-learning`.`students`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`students` (
  `student_id` INT(11) NOT NULL,
  `photo` BLOB NULL DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  INDEX `user_id` (`student_id` ASC) ,
  CONSTRAINT `students_ibfk_1`
    FOREIGN KEY (`student_id`)
    REFERENCES `e-learning`.`users` (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `e-learning`.`students_has_courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`students_has_courses` (
  `course_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `subscription_status` TINYINT(4) NOT NULL,
  `enrollment_date` DATETIME NOT NULL,
  `unenrollment_date` DATETIME NULL,
  `student_rating` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`course_id`, `user_id`),
  INDEX `fk_courses_has_students_students1_idx` (`user_id` ASC) ,
  INDEX `fk_courses_has_students_courses1_idx` (`course_id` ASC) ,
  CONSTRAINT `fk_courses_has_students_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `e-learning`.`courses` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_courses_has_students_students1`
    FOREIGN KEY (`user_id`)
    REFERENCES `e-learning`.`students` (`student_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
