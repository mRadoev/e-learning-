-- --Courses examples for testing
TRUNCATE TABLE `e-learning`.`courses`;
INSERT INTO `e-learning`.`courses` (`title`,`description`,`objectives`,`owner`,`tags`,`status`) VALUES ('Javascript level 1','Learn the basics of java','Learn java',4, 'java, javascript, level 1',1);
INSERT INTO `e-learning`.`courses` (`title`,`description`,`objectives`,`owner`,`tags`,`status`) VALUES ('Python Programming', 'Learn Python programming language', 'Master Python basics and advanced concepts', 2, 'python, programming, beginner', 0);
INSERT INTO `e-learning`.`courses` (`title`,`description`,`objectives`,`owner`,`tags`,`status`) VALUES ('Web Development Fundamentals', 'Introduction to web development technologies', 'Understand HTML, CSS, and JavaScript basics', 2, 'web development, html, css, javascript', 0);
INSERT INTO `e-learning`.`courses` (`title`,`description`,`objectives`,`owner`,`tags`,`status`) VALUES ('Literature ', 'First steps in the world of literature', 'Get to know famous authors and their work', 4, 'literature, authors, books', 0);
INSERT INTO `e-learning`.`courses` (`title`,`description`,`objectives`,`owner`,`tags`,`status`) VALUES ('Supreme ', 'Everything', 'You cant ask for more', 7, 'everything, everywhere all at once', 1);

-- --Users examples for testing
TRUNCATE TABLE `e-learning`.`users`;
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('admin','example10@asd.com','admin','admin', 'admin');
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('teacher','example1@asd.com','Ara','Mara', '1234');
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('student','example2@asd.com','Goro','Boro', '1234');
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('teacher','example3@asd.com','Ara','Mara', '1234');
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('student', 'example4@asd.com', 'Georgi', 'Georgiev', 'password123');
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('student', 'example5@asd.com', 'Ico', 'Xa', 'password123');
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('teacher', 'example6@asd.com', 'Anton', 'Antonov', 'password123');
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('student', 'example7@asd.com', 'Tedo', 'Za', 'password123');


-- --Sections examples for testing
TRUNCATE TABLE `e-learning`.`sections`;
INSERT INTO `e-learning`.`sections` (`course_id`,`title`,`content`,`description`) VALUES (5,'Java 1','New content','The first java example');
INSERT INTO `e-learning`.`sections` (`course_id`,`title`,`content`,`description`) VALUES (2, 'HTML Basics', 'Example content', 'Introduction to HTML markup language');
INSERT INTO `e-learning`.`sections` (`course_id`,`title`,`content`,`description`) VALUES (3, 'CSS Styling', 'Example content', 'Learn how to style elements using CSS');
INSERT INTO `e-learning`.`sections` (`course_id`,`title`,`content`,`description`) VALUES (4, 'William Shakespeare', 'Example content', 'Introduction to the ideas of one of the most famous authors of moder times');
INSERT INTO `e-learning`.`sections` (`course_id`,`title`,`content`,`description`) VALUES (1, 'Test', 'test', 'Testing the test');