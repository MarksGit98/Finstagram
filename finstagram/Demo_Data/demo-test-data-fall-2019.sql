SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

INSERT INTO `Friendgroup` (`groupOwner`, `groupName`, `description`) VALUES('C', 'best friends', 'Cathy''s best friends');
INSERT INTO `Friendgroup` (`groupOwner`, `groupName`, `description`) VALUES('D', 'best friends', 'Dave''s best friends');

INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES(1, '2019-12-10 00:00:00', 'photo1B.jpg', 1, 'photo 1', 'B');
INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES(2, '2019-12-11 00:00:00', 'photo2C.jpg', 1, 'photo 2', 'C');
INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES(3, '2019-12-12 00:00:00', 'photo3D.jpg', 1, 'photo 3', 'D');
INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES(4, '2019-12-13 00:00:00', 'photo4D.jpg', 1, NULL, 'D');
INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES(5, '2019-12-14 00:00:00', 'photo5E.jpg', 0, 'photo 5', 'E');

INSERT INTO `SharedWith` (`groupOwner`, `groupName`, `photoID`) VALUES('C', 'best friends', 2); 
INSERT INTO `SharedWith` (`groupOwner`, `groupName`, `photoID`) VALUES('D', 'best friends', 3);

INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES('A', 'C', 'best friends');

INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES('A', 'B', 1);
INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES('A', 'C', 0);
INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES('A', 'D', 0);
INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES('A', 'E', 1);
INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES('B', 'A', 1);
INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES('B', 'D', 1);
INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES('B', 'E', 1);
INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES('C', 'D', 1);
INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES('E', 'A', 1);

INSERT INTO `Likes` (`username`, `photoID`, `liketime`, `rating`) VALUES('D', 1, '2019-12-11 00:00:00', 5);
INSERT INTO `Likes` (`username`, `photoID`, `liketime`, `rating`) VALUES('D', 2, '2019-12-11 00:00:00', 5);
INSERT INTO `Likes` (`username`, `photoID`, `liketime`, `rating`) VALUES('E', 1, '2019-12-11 00:00:00', 3);

INSERT INTO `Tagged` (`username`, `photoID`, `tagstatus`) VALUES('A', 1, 0);
INSERT INTO `Tagged` (`username`, `photoID`, `tagstatus`) VALUES('D', 1, 1);
INSERT INTO `Tagged` (`username`, `photoID`, `tagstatus`) VALUES('D', 2, 1);
INSERT INTO `Tagged` (`username`, `photoID`, `tagstatus`) VALUES('E', 1, 1);