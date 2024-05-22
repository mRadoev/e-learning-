-- --Courses examples for testing
INSERT INTO `e-learning`.`courses` (`title`,`description`,`objectives`,`owner`,`tags`,`status`) VALUES ('Javascript level 1','Learn the basics of java','Learn java',2, 'java, javascript, level 1',0);
INSERT INTO `e-learning`.`courses` (`title`,`description`,`objectives`,`owner`,`tags`,`status`) VALUES ('Python Programming', 'Learn Python programming language', 'Master Python basics and advanced concepts', 1, 'python, programming, beginner', 0);
INSERT INTO `e-learning`.`courses` (`title`,`description`,`objectives`,`owner`,`tags`,`status`) VALUES ('Web Development Fundamentals', 'Introduction to web development technologies', 'Understand HTML, CSS, and JavaScript basics', 4, 'web development, html, css, javascript', 0);
INSERT INTO `e-learning`.`courses` (`title`,`description`,`objectives`,`owner`,`tags`,`status`) VALUES ('Literature ', 'First steps in the world of literature', 'Get to know famous authors and their work', 4, 'literature, authors, books', 0);

-- --Users examples for testing
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('student','example1@asd.com','Goro','Boro', '1234');
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('teacher','example2@asd.com','Ara','Mara', '1234');
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('student', 'example3@asd.com', 'Georgi', 'Georgiev', 'password123');
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('student', 'example5@asd.com', 'Ico', 'Xa', 'password123');
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('student', 'example6@asd.com', 'Tedo', 'Za', 'password123');
INSERT INTO `e-learning`.`users` (`role`,`email`,`first_name`,`last_name`,`password`) VALUES ('teacher', 'example4@asd.com', 'Anton', 'Antonov', 'password123');

-- --Sections examples for testing
INSERT INTO `e-learning`.`sections` (`course_id`,`title`,`content`,`description`) VALUES (5,'Java 1','New content','The first java example');
INSERT INTO `e-learning`.`sections` (`course_id`,`title`,`content`,`description`) VALUES (2, 'HTML Basics', 'Example content', 'Introduction to HTML markup language');
INSERT INTO `e-learning`.`sections` (`course_id`,`title`,`content`,`description`) VALUES (3, 'CSS Styling', 'Example content', 'Learn how to style elements using CSS');
INSERT INTO `e-learning`.`sections` (`course_id`,`title`,`content`,`description`) VALUES (4, 'William Shakespeare', 'Example content', 'Introduction to the ideas of one of the most famous authors of moder times');