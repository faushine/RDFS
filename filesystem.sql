USE rdfs;

DROP TABLE Directory;

DROP TABLE File;

CREATE TABLE `Directory` (
  `dirId` varchar(50) NOT NULL,
  `dirPath` varchar(100) DEFAULT NULL,
  `dirName` VARCHAR(20),
  `dirSub` text,
  `permission` varchar(15) DEFAULT NULL,
  `dirNode` INT,
  `dirOwner` varchar(20) DEFAULT NULL,
  `groupOwner` varchar(20) DEFAULT NULL,
  `dirSize` INT,
  `lastModified` VARCHAR(20),
  PRIMARY KEY (`dirId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `File` (
  `fId` varchar(100) NOT NULL,
  `fname` varchar(30) DEFAULT NULL,
  `content` longblob,
  `permission` varchar(15) DEFAULT NULL,
  `fileNode` INT,
  `fileOwner` varchar(20) DEFAULT NULL,
  `groupOwner` varchar(20) DEFAULT NULL,
  `fileSize` INT,
  `fileType` varchar(10) DEFAULT NULL,
   `lastModified` VARCHAR(20),
  PRIMARY KEY (`fId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



