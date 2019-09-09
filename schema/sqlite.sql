CREATE TABLE IF NOT EXISTS `Campus` (
    `id` INTEGER NOT NULL,
    `name` VARCHAR(64) NOT NULL,
    
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Building` (
    `id` INTEGER NOT NULL,
    `name` VARCHAR(64) NOT NULL,
    `floor_count` INTEGER NOT NULL DEFAULT 1,
    `campus` INTEGER NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`campus`) REFERENCES `Campus`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Room` (
    `id` INTEGER NOT NULL,
    `identifier` VARCHAR(16) NOT NULL,
    `building_floor` INTEGER NOT NULL DEFAULT 1,
    `building` INTEGER NOT NULL,
    `capacity` INTEGER NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`building`) REFERENCES `Building`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Student` (
    `id` INTEGER NOT NULL,
    `first_name` VARCHAR(64) NOT NULL,
    `last_name` VARCHAR(64) NOT NULL,
    `email` VARCHAR(128) NOT NULL,
    `mobile` VARCHAR(32) NULL,
    `salt` CHAR(16) NOT NULL,
    `password` CHAR(64),

    PRIMARY KEY (`id`),
    UNIQUE (`email`)
);

CREATE TABLE IF NOT EXISTS `Teacher` (
    `id` INTEGER NOT NULL,
    `first_name` VARCHAR(64) NOT NULL,
    `last_name` VARCHAR(64) NOT NULL,
    `email` VARCHAR(128) NOT NULL,
    `mobile` VARCHAR(32) NULL,
    `salt` CHAR(16) NOT NULL,
    `password` CHAR(64),

    PRIMARY KEY (`id`),
    UNIQUE (`email`)
);

CREATE TABLE IF NOT EXISTS `StaffRole` (
    `id` INTEGER NOT NULL,
    `name` VARCHAR(64) NOT NULL,
    `display_name` VARCHAR(64) NOT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Staff` (
    `id` INTEGER NOT NULL,
    `first_name` VARCHAR(64) NOT NULL,
    `last_name` VARCHAR(64) NOT NULL,
    `email` VARCHAR(128) NOT NULL,
    `mobile` VARCHAR(32) NULL,
    `salt` CHAR(16) NOT NULL,
    `password` CHAR(64),
    `role` INTEGER NOT NULL,

    PRIMARY KEY (`id`),
    UNIQUE (`email`),
    FOREIGN KEY (`role`) REFERENCES `StaffRole`(`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS `Module` (
    `id` INTEGER NOT NULL,
    `name` VARCHAR(128) NOT NULL,
    `leader` INTEGER NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`leader`) REFERENCES `Teacher`(`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS `StudentModule` (
    `id` INTEGER NOT NULL,
    `module` INTEGER NOT NULL,
    `student` INTEGER NOT NULL,
    `enrolment_date` INTEGER NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`module`) REFERENCES `Module`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (`student`) REFERENCES `Student`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `ModuleSessionType` (
    `id` INTEGER NOT NULL,
    `name` VARCHAR(64) NOT NULL,
    `display_name` VARCHAR(64) NOT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `ModuleSession` (
    `id` INTEGER NOT NULL,
    `module` INTEGER NOT NULL,
    `staff` INTEGER NOT NULL,
    `type` INTEGER NOT NULL,

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
);

CREATE TABLE IF NOT EXISTS `RoomBooking` (
    `id` INTEGER NOT NULL,
    `room` INTEGER NOT NULL,
    `time_from` INTEGER NOT NULL,
    `time_to` INTEGER NOT NULL,
    `module_session` INTEGER NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`room`) REFERENCES `Room`(`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (`module_session`) REFERENCES `ModuleSession`(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `ApiSession` (
    `id` INTEGER NOT NULL,
    `token` VARCHAR(64) NOT NULL,
    `signature` VARCHAR(64) NOT NULL,
    `user_id` INT,
    `user_type` VARCHAR(16), -- either "teacher" or "student", field bigger for future purposes
    `expires` INTEGER NOT NULL,

    PRIMARY KEY (`id`),
    UNIQUE (`token`)
);

CREATE TABLE IF NOT EXISTS `PasswordReset` (
    `id` INTEGER NOT NULL,
    `token` VARCHAR(64) NOT NULL,
    `user_id` INTEGER NOT NULL,
    `user_type` VARCHAR(16) NOT NULL, -- one of: teacher/student/staff
    `expires` INTEGER NOT NULL,

    PRIMARY KEY(`id`),
    UNIQUE(`token`)
);

CREATE TABLE IF NOT EXISTS `Term` (
    `id` INTEGER NOT NULL,
    `start_date` INTEGER NOT NULL,
    `end_date` INTEGER NOT NULL,
    `term` INTEGER NOT NULL,

    PRIMARY KEY(`id`)
);

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

INSERT INTO `Staff` (`first_name`, `last_name`, `email`, `mobile`, `salt`, `password`, `role`) VALUES ('Admin', 'Admin', 'admin@a4scheduler.xyz', '07471290471', 'c4d99330bde68c51', '01a41c0b6042bec9f1d841e5f46132e70e0a4471dedb2f21ed4bea6266807a4d', 1);