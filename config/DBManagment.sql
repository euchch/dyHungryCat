CREATE TABLE hcData (
    foodName VARCHAR(20) CHARACTER SET utf8,
    updateTime DATETIME NOT NULL PRIMARY KEY,
    notificationSent ENUM('false', 'true') NOT NULL DEFAULT 'false',
    lastModified DATETIME,
    notificationSentTimeStamp DATETIME
);