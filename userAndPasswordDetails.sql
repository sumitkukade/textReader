DROP TABLE IF EXISTS userPassword;
/*--------------------------------------------------------------*/
/*this table have user and password record */

CREATE TABLE IF NOT EXISTS userPassword (
   userId varchar(15) NOT NULL,
   password text NOT NULL,
   Constraint pk_userIdDomain Primary Key(userId),
   Foreign Key (userId) References userIdDomain(userId)
   ON DELETE RESTRICT ON UPDATE CASCADE
);

