CREATE TABLE `Datasets Table` (
    `DatasetID` INT PRIMARY KEY,
    `Name` VARCHAR(255),
    `Description` TEXT,
    `Type` VARCHAR(100),
    `CreationDate` DATE
);

CREATE TABLE `Images Table` (
    `ImageID` INT PRIMARY KEY,
    `DatasetID` INT,
    `FilePath` TEXT,
    `Label` VARCHAR(255),
    `Split` VARCHAR(50),
    FOREIGN KEY (`DatasetID`) REFERENCES `Datasets Table`(`DatasetID`)
);

CREATE TABLE `Annotations Table` (
    `AnnotationID` INT PRIMARY KEY,
    `ImageID` INT,
    `ObjectClass` VARCHAR(100),
    `BoundingBox` VARCHAR(100), 
    FOREIGN KEY (`ImageID`) REFERENCES `Images Table`(`ImageID`)
);

CREATE TABLE `Models Table` (
    `ModelID` INT PRIMARY KEY,
    `Name` VARCHAR(255),
    `Architecture` VARCHAR(100),
    `CreationDate` DATE,
    `TrainingDatasetID` INT,
    FOREIGN KEY (`TrainingDatasetID`) REFERENCES `Datasets Table`(`DatasetID`)
);

CREATE TABLE `Training Sessions Table` (
    `SessionID` INT PRIMARY KEY,
    `ModelID` INT,
    `StartDate` DATETIME,
    `EndDate` DATETIME,
    `Status` VARCHAR(50),
    `Accuracy` FLOAT,
    `Loss` FLOAT,
    FOREIGN KEY (`ModelID`) REFERENCES `Models Table`(`ModelID`)
);

CREATE TABLE `Inferences Table` (
    `InferenceID` INT PRIMARY KEY,
    `ModelID` INT,
    `InputData` TEXT,
    `Result` TEXT,
    `InferenceDate` DATETIME,
    FOREIGN KEY (`ModelID`) REFERENCES `Models Table`(`ModelID`)
);
