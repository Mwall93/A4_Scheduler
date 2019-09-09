CREATE TABLE IF NOT EXISTS `Campus` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(64) NOT NULL,
    
    PRIMARY KEY (`id`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `Building` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(64) NOT NULL,
    `floor_count` INT NOT NULL DEFAULT 1,
    `campus` INT NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`campus`) REFERENCES `Campus`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `Room` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `identifier` VARCHAR(16) NOT NULL,
    `building_floor` INT NOT NULL DEFAULT 1,
    `building` INT NOT NULL,
    `capacity` INT NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`building`) REFERENCES `Building`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `Student` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `first_name` VARCHAR(64) NOT NULL,
    `last_name` VARCHAR(64) NOT NULL,
    `email` VARCHAR(128) NOT NULL,
    `mobile` VARCHAR(32) NULL,
    `salt` CHAR(16) NOT NULL,
    `password` CHAR(64),

    PRIMARY KEY (`id`),
    UNIQUE (`email`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `Teacher` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `first_name` VARCHAR(64) NOT NULL,
    `last_name` VARCHAR(64) NOT NULL,
    `email` VARCHAR(128) NOT NULL,
    `mobile` VARCHAR(32) NULL,
    `salt` CHAR(16) NOT NULL,
    `password` CHAR(64),

    PRIMARY KEY (`id`),
    UNIQUE (`email`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `StaffRole` (
    `id` INT NOT NULL,
    `name` VARCHAR(64) NOT NULL,
    `display_name` VARCHAR(64) NOT NULL,

    PRIMARY KEY (`id`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `Staff` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `first_name` VARCHAR(64) NOT NULL,
    `last_name` VARCHAR(64) NOT NULL,
    `email` VARCHAR(128) NOT NULL,
    `mobile` VARCHAR(32) NULL,
    `salt` CHAR(16) NOT NULL,
    `password` CHAR(64),
    `role` INT NOT NULL,

    PRIMARY KEY (`id`),
    UNIQUE (`email`),
    FOREIGN KEY (`role`) REFERENCES `StaffRole`(`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `Module` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(128) NOT NULL,
    `leader` INT NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`leader`) REFERENCES `Teacher`(`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `StudentModule` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `module` INT NOT NULL,
    `student` INT NOT NULL,
    `enrolment_date` INT NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`module`) REFERENCES `Module`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (`student`) REFERENCES `Student`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `ModuleSessionType` (
    `id` INT NOT NULL,
    `name` VARCHAR(64) NOT NULL,
    `display_name` VARCHAR(64) NOT NULL,

    PRIMARY KEY (`id`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `ModuleSession` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `module` INT NOT NULL,
    `staff` INT NOT NULL,
    `type` INT NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`module`) REFERENCES `Module`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (`staff`) REFERENCES `Teacher`(`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (`type`) REFERENCES `ModuleSessionType`(`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `RoomBooking` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `room` INT NOT NULL,
    `time_from` INT NOT NULL,
    `time_to` INT NOT NULL,
    `module_session` INT NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`room`) REFERENCES `Room`(`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (`module_session`) REFERENCES `ModuleSession`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `ApiSession` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `token` VARCHAR(64) NOT NULL,
    `signature` VARCHAR(64) NOT NULL,
    `user_id` INT,
    `user_type` VARCHAR(16), -- either "teacher" or "student", field bigger for future purposes
    `expires` INT NOT NULL,

    PRIMARY KEY (`id`),
    UNIQUE (`token`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `PasswordReset` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `token` VARCHAR(64) NOT NULL,
    `user_id` INT NOT NULL,
    `user_type` VARCHAR(16) NOT NULL, -- one of: teacher/student/staff
    `expires` INT NOT NULL,

    PRIMARY KEY(`id`),
    UNIQUE(`token`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `Term` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `start_date` INT NOT NULL,
    `end_date` INT NOT NULL,
    `term` INT NOT NULL,

    PRIMARY KEY(`id`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

-- Insert possible staff roles (these reflect staff roles in the system)
INSERT INTO `StaffRole` (`id`, `name`, `display_name`) VALUES (1, 'admin', 'System Administrator');
INSERT INTO `StaffRole` (`id`, `name`, `display_name`) VALUES (2, 'building_admin', 'Building Administrator');
INSERT INTO `StaffRole` (`id`, `name`, `display_name`) VALUES (3, 'scheduling_admin', 'Scheduling Administrator');
INSERT INTO `StaffRole` (`id`, `name`, `display_name`) VALUES (4, 'fire_officer', 'Fire Officer');

-- Insert possible module session types (these reflect session types in the system)
INSERT INTO `ModuleSessionType` (`id`, `name`, `display_name`) VALUES (1, 'lecture', 'Lecture');
INSERT INTO `ModuleSessionType` (`id`, `name`, `display_name`) VALUES (2, 'seminar', 'Seminar');
INSERT INTO `ModuleSessionType` (`id`, `name`, `display_name`) VALUES (3, 'lab', 'Lab');
INSERT INTO `ModuleSessionType` (`id`, `name`, `display_name`) VALUES (4, 'workshop', 'Workshop');
INSERT INTO `ModuleSessionType` (`id`, `name`, `display_name`) VALUES (5, 'tutorials', 'Personal & Academic Tutorials');

INSERT INTO `Term` (`start_date`, `end_date`, `term`) VALUES (1538352000, 1544745600, 1);

-- SQL Change Statements (for modifying existing databases)

DROP TABLE IF EXISTS `Term`;
DROP TABLE IF EXISTS `RoomBooking`;
DROP TABLE IF EXISTS `StudentModule`;

CREATE TABLE IF NOT EXISTS `Term` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `start_date` INT NOT NULL,
    `end_date` INT NOT NULL,
    `term` INT NOT NULL,

    PRIMARY KEY(`id`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `RoomBooking` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `room` INT NOT NULL,
    `time_from` INT NOT NULL,
    `time_to` INT NOT NULL,
    `module_session` INT NULL, --FIXME: (CRITICAL) CHANGE THIS FROM NOT NULL TO NULL IN ALL DATABASES

    PRIMARY KEY (`id`),
    FOREIGN KEY (`room`) REFERENCES `Room`(`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (`module_session`) REFERENCES `ModuleSession`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB CHARACTER SET=utf8mb4;

CREATE TABLE IF NOT EXISTS `StudentModule` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `module` INT NOT NULL,
    `student` INT NOT NULL,
    `enrolment_date` INT NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`module`) REFERENCES `Module`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (`student`) REFERENCES `Student`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB CHARACTER SET=utf8mb4;


ALTER TABLE `RoomBooking` MODIFY `module_session` INT;
ALTER TABLE `Room` ADD `capacity` INT NOT NULL DEFAULT 15;
ALTER TABLE `Room` MODIFY `capacity` INT NOT NULL;

ALTER TABLE `ApiSession` ADD `expires` INT NOT NULL AFTER `user_type`;