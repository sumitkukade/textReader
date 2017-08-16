/*
keySetting - timing Integer,delay Integer;
keyBinding - productId,keySequnce;
priceBinding - poductId,date,price;
products - productId,unit,price;
orders - orderNo,custName,date.actualAmount,discount,finalAmount;
orderDetails - orderNo,productId,quantity,price,totalAmount
responeses - orderNo,date,orderList;
*/

DROP DATABASE IF EXISTS productOrder;

CREATE DATABASE productOrder;

use productOrder


DROP TABLE IF EXISTS customerDetails;
DROP TABLE IF EXISTS maybeorderDetails;
DROP TABLE IF EXISTS responeses;
DROP TABLE IF EXISTS orderDetails;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS priceBinding;
DROP TABLE IF EXISTS products;

create table customerDetails
(
  custId Integer Not Null primary key,
  custName varchar(20),
  custAddr varchar(20)
);

create table products
(
  productId varchar(20) Not Null primary key,
  unit integer Not Null,
  price double precision Not Null
);

create table priceBinding
(
  productId varchar(20) Not Null,
  productDate timestamp Not Null,
  price double precision Not Null,
  Constraint pk_priceBinding primary key (productId,productDate),
  Foreign Key (productId) References products(productId)
  ON DELETE RESTRICT ON UPDATE CASCADE
);

create table orders
(
  orderNo Integer Not Null primary key Auto_increment,
  custName varchar(20) Not Null,
  orderDate timestamp Not Null,
  actualAmount double precision default 0,
  discount double precision default 0,
  finalAmount double precision default 0
);

create table orderDetails
(
  orderNo Integer Not Null,
  productId varchar(20) Not Null,
  quantity Integer Not Null,
  price double precision Not Null,
  totalAmount double precision Not Null,
  Constraint pk_orderDetails primary key (orderNo,productId),
  Foreign Key (orderNo) References orders(orderNo)
  ON DELETE RESTRICT ON UPDATE CASCADE
);

create table maybeorderDetails
(
  orderNo Integer Not Null,
  productId varchar(20) Not Null,
  quantity Integer Not Null,
  price double precision default 0,
  totalAmount double precision default 0,
  Constraint pk_maybeorderDetails primary key (orderNo,productId),
  Foreign Key (orderNo) References orders(orderNo)
  ON DELETE RESTRICT ON UPDATE CASCADE
);

create table responeses
(
  orderNo Integer Not NulL,
  orderDate timestamp Not Null,
  orderList varchar(100) Not Null,
  finalAmount double precision,
  Foreign Key (orderNo) References orders(orderNo)
  ON DELETE RESTRICT ON UPDATE CASCADE
);

create table orderDiscount
(
  amount double precision Not Null primary key,
  discount double precision Not Null
);

create table temp
(
  u double precision
);


delimiter |



create trigger trigger_InsertInorder after insert on customerDetails
FOR EACH ROW
BEGIN
insert into orders(custName,orderDate) values(new.custName,now());
END;

create trigger trigger_updateOnorderDetails after insert on maybeorderDetails
FOR EACH ROW
BEGIN
  insert into orderDetails(orderNo,productId,quantity,price,totalAmount) values(new.orderNo,new.productId,new.quantity,(select price from products where productId=new.productId),(select price*new.quantity from products where productId=new.productId));
END;

create trigger trigger_updateorder after insert on orderDetails
FOR EACH ROW
BEGIN
  update orders set actualAmount = actualAmount+(select price*new.quantity from products where productId=new.productId);
  update orders set discount = (select discount from orderDiscount where amount<actualAmount order by discount desc limit 1);
  update orders set finalAmount = actualAmount-actualAmount*discount/100;
END;

create trigger insertIntoResponses after update on orders
FOR EACH ROW
  BEGIN
    set @isExistsOrderNo = (select NEW.orderNo in (select orderNo from responeses));
    if(@isExistsOrderNo = 0) then
    insert into responeses(orderNo,orderDate,orderList,finalAmount) values (new.orderNo,(select orderDate from orders where orderNo = new.orderNo),(select group_concat(productId," - ",quantity," - ",price,"\n") as orderList from orderDetails group by new.orderNo),new.finalAmount);
  else
    delete from responeses where orderNo=New.orderNo;
    insert into responeses(orderNo,orderDate,orderList,finalAmount) values (new.orderNo,(select orderDate from orders where orderNo = new.orderNo),(select group_concat(productId," - ",quantity," - ",price*quantity,"\n") as orderList from orderDetails group by new.orderNo),new.finalAmount);
    end if;
    END;

  |

delimiter ;

insert into customerDetails values(1,"shaan","abshbkbkd fjdsbj");


insert into products(productId,unit,price) values("abc",1,100);
insert into products(productId,unit,price) values("xyz",2,200);
insert into products(productId,unit,price) values("pqr",8,300);
insert into products(productId,unit,price) values("def",9,500);
insert into products(productId,unit,price) values("wxy",1,200);

insert into orderDiscount(amount,discount) values(500,10);
insert into orderDiscount(amount,discount) values(550,15);
insert into orderDiscount(amount,discount) values(1000,20);

insert into maybeorderDetails(orderNo,productId,quantity) values(1,"abc",2);
insert into maybeorderDetails(orderNo,productId,quantity) values(1,"xyz",3);
insert into maybeorderDetails(orderNo,productId,quantity) values(1,"pqr",1);

insert into priceBinding(productId,productDate,price) values("abc","2017-01-02 11:22:01",80);
insert into priceBinding(productId,productDate,price) values("xyz","2014-03-02 12:56:01",100);
insert into priceBinding(productId,productDate,price) values("pqr","2013-08-09 01:22:01",100);
insert into priceBinding(productId,productDate,price) values("abc","2013-08-02 04:22:01",30);

select * from orders;
select * from responeses;


