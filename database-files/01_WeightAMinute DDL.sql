DROP DATABASE IF EXISTS weightaminute;
CREATE DATABASE weightaminute;
USE weightaminute;

CREATE TABLE Users
(
    userId    int AUTO_INCREMENT PRIMARY KEY,
    DOB       date         NOT NULL,
    gender    varchar(10)  NOT NULL,
    email     varchar(255) NOT NULL,
    firstName varchar(100) NOT NULL,
    lastName  varchar(100) NOT NULL,
    adminId   int,
    CONSTRAINT fk_adminId_users_users
        FOREIGN KEY (adminId) REFERENCES Users (userId)
            ON DELETE SET NULL
            ON UPDATE CASCADE
);

CREATE TABLE FAQs
(
    faqId       int AUTO_INCREMENT PRIMARY KEY,
    question    text NOT NULL,
    answer      text NOT NULL,
    dateUpdated datetime DEFAULT CURRENT_TIMESTAMP,
    createdById int,
    CONSTRAINT fk_createdById_faqs_users
        FOREIGN KEY (createdById) REFERENCES Users (userId)
            ON DELETE SET NULL
            ON UPDATE CASCADE
);

CREATE TABLE Trainers
(
    trainerId int AUTO_INCREMENT PRIMARY KEY,
    userId    int          NOT NULL,
    type      varchar(100) NOT NULL,
    YOE       int          NOT NULL,
    CONSTRAINT fk_userId_trainers_users
        FOREIGN KEY (userId) REFERENCES Users (userId)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE UsersTrainedBy
(
    userId    int,
    trainerId int,
    PRIMARY KEY (userId, trainerId),
    CONSTRAINT fk_UsersTrainedBy_userId
        FOREIGN KEY (userId) REFERENCES Users (userId)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_UsersTrainedBy_trainerId
        FOREIGN KEY (trainerId) REFERENCES Trainers (trainerId)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE BlogPosts
(
    postId   int AUTO_INCREMENT PRIMARY KEY,
    content  longtext     NOT NULL,
    title    varchar(255) NOT NULL,
    authorId int          NOT NULL,
    CONSTRAINT fk_authorId_blogposts_trainers
        FOREIGN KEY (authorId) REFERENCES Trainers (trainerId)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE GymRequests
(
    userId      int,
    requestId   int,
    gymDetails  text NOT NULL,
    requestDate datetime DEFAULT CURRENT_TIMESTAMP,
    reviewId    int,
    PRIMARY KEY (userId, requestId),
    CONSTRAINT fk_reviewId_gymrequests_users
        FOREIGN KEY (reviewId) REFERENCES Users (userId)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
    CONSTRAINT fk_userId_gymrequests_users
        FOREIGN KEY (userId) REFERENCES Users (userId)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE Workouts
(
    workoutId    int AUTO_INCREMENT PRIMARY KEY,
    name         varchar(255) NOT NULL,
    time         time,
    timesPerWeek int          NOT NULL,
    createdById  int,
    CONSTRAINT fk_createdById_workouts_trainers
        FOREIGN KEY (createdById) REFERENCES Trainers (trainerId)
            ON DELETE SET NULL
            ON UPDATE CASCADE
);

CREATE TABLE CompletedWorkouts
(
    workoutId   int,
    userId      int,
    completedAt datetime DEFAULT CURRENT_TIMESTAMP,
    notes       longtext,
    PRIMARY KEY (userId, workoutId),
    CONSTRAINT fk_CompletedWorkouts_userId
        FOREIGN KEY (userId) REFERENCES Users (userId)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_CompletedWorkouts_workoutId
        FOREIGN KEY (workoutId) REFERENCES Workouts (workoutId)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE TargetMuscles
(
    muscleGroup varchar(100) NOT NULL,
    workoutId   int,
    PRIMARY KEY (muscleGroup, workoutId),
    CONSTRAINT fk_workoutId_targetmuscles_workouts
        FOREIGN KEY (workoutId) REFERENCES Workouts (workoutId)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE Gyms
(
    gymId        int AUTO_INCREMENT PRIMARY KEY,
    name         varchar(255) NOT NULL,
    location     varchar(255) NOT NULL,
    type         varchar(100) NOT NULL,
    monthlyPrice int          NOT NULL,
    ownerId      int,
    adminId      int,
    CONSTRAINT fk_ownerId_gyms_users
        FOREIGN KEY (ownerId) REFERENCES Users (userId)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
    CONSTRAINT fk_adminId_gyms_users
        FOREIGN KEY (adminId) REFERENCES Users (userId)
            ON DELETE SET NULL
            ON UPDATE CASCADE
);

CREATE TABLE Memberships
(
    subscriptionId int AUTO_INCREMENT PRIMARY KEY,
    userId         int         NOT NULL,
    gymId          int         NOT NULL,
    tier           varchar(50) NOT NULL,
    monthlyFee     int         NOT NULL,
    length         int         NOT NULL,
    CONSTRAINT fk_userId_memberships_users
        FOREIGN KEY (userId) REFERENCES Users (userId)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_gymId_memberships_gyms
        FOREIGN KEY (gymId) REFERENCES Gyms (gymId)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE Records
(
    userId int,
    name   varchar(255) NOT NULL,
    type   varchar(100) NOT NULL,
    weight int          NOT NULL,
    reps   int          NOT NULL,
    gymId  int          NOT NULL,
    PRIMARY KEY (userId, name),
    CONSTRAINT fk_userId_records_users
        FOREIGN KEY (userId) REFERENCES Users (userId)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_gymId_records_gyms
        FOREIGN KEY (gymId) REFERENCES Gyms (gymId)
            ON DELETE RESTRICT
            ON UPDATE CASCADE
);

CREATE TABLE Equipment
(
    equipmentId int AUTO_INCREMENT PRIMARY KEY,
    name        varchar(255) NOT NULL,
    minWeight   int,
    maxWeight   int,
    brand       varchar(100),
    description text         NOT NULL
);

CREATE TABLE Exercises
(
    exerciseId int AUTO_INCREMENT PRIMARY KEY,
    name       varchar(255) NOT NULL,
    weight     int
);

CREATE TABLE ExerciseEquipment
(
    equipmentId int,
    exerciseId  int,
    PRIMARY KEY (equipmentId, exerciseId),
    CONSTRAINT fk_equipmentId_exerciseequipment_equipment
        FOREIGN KEY (equipmentId) REFERENCES Equipment (equipmentId)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_exerciseId_exerciseequipment_exercises
        FOREIGN KEY (exerciseId) REFERENCES Exercises (exerciseId)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE WorkoutExercises
(
    exerciseId int NOT NULL,
    workoutId  int NOT NULL,
    reps       int,
    sets       int,
    PRIMARY KEY (exerciseId, workoutId),
    CONSTRAINT fk_exerciseId_workoutexercises_exercises
        FOREIGN KEY (exerciseId) REFERENCES Exercises (exerciseId)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_workoutId_workoutexercises_workouts
        FOREIGN KEY (workoutId) REFERENCES Workouts (workoutId)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE GymEquipment
(
    gymId       int,
    equipmentId int,
    PRIMARY KEY (gymId, equipmentId),
    CONSTRAINT fk_gymId_gymequipment_gyms
        FOREIGN KEY (gymId) REFERENCES Gyms (gymId)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_equipmentId_gymequipment_equipment
        FOREIGN KEY (equipmentId) REFERENCES Equipment (equipmentId)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);
