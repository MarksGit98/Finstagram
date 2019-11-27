CREATE TABLE Person(
    username VARCHAR(20), 
    password CHAR(64), 
    fname VARCHAR(20),
    lname VARCHAR(20),
    PRIMARY KEY (username)
);

CREATE TABLE Photo(
    photoID int NOT NULL AUTO_INCREMENT,
    timestamp Timestamp,
    filePath VARCHAR(2048),
    PRIMARY KEY (photoID)
);

SELECT DISTINCT photoID
FROM Photo AS P JOIN Follow AS F ON
P.photoPoster = F.username_followed LEFT JOIN SharedWith AS S
ON S.photoID = P.photoID LEFT JOIN BelongTo AS B ON S.groupName = B.groupName AND S.groupOwner = B.owner_username
WHERE (F.username_follower = 'TestUser' AND F.followstatus = 1 AND
P.allFollowers = 1) OR B.member_username = 'TestUser'