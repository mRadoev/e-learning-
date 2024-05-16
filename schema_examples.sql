INSERT INTO `e-learning`.`courses` (`title`,`description`,`objectives`,`owner`,`tags`,`status`) VALUES ('Javascript level 1','Learn the basics of java','Learn java',2, 'java, javascript, level 1',0);

INSERT INTO `e-learning`.`users` (`role`,`e-mail`,`first_name`,`last_name`,`password`) VALUES ('student','example1@asd.com','Goro','Boro', '1234');
INSERT INTO `e-learning`.`users` (`role`,`e-mail`,`first_name`,`last_name`,`password`) VALUES ('teacher','example2@asd.com','Ara','Mara', '1234');

INSERT INTO `e-learning`.`sections` (`course_id`,`title`,`content`,`description`) VALUES (1,'Java 1','New content','The first java example');