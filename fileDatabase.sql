DROP TABLE IF EXISTS fileDomain;
DROP TABLE IF EXISTS fontSizeDomain;

CREATE TABLE IF NOT EXISTS fileDomain (
  filename text NOT NULL,
  filePath text NOT NULL,
  fileContent blob NOT NULL,
  Constraint pk_fileDomain Primary Key(filename,filePath)
);

CREATE TABLE IF NOT EXISTS fontSizeDomain (
  fontSize integer NOT NULL primary key
);

CREATE TABLE IF NOT EXISTS userDetailsDomain (
  userId text NOT NULL primary Key,
  name text NOT NULL,
)

insert into fileDomain(filename,filePath,fileContent) values("r.txt","/home/reshma/InternShip/textReader/r.txt",readfile("r.txt"));

insert into fontSizeDomain(fontSize) values(10),(15),(20),(25);





