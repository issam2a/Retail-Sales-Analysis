
-- checking for null values 

	select OrderID  from sales 
	where OrderID is null ;

	select RowID from sales 
	where RowID is null ;

	select CustomerID from sales where CustomerID is null ;

-- Checking the data type 
	select COLUMN_NAME , DATA_TYPE from information_schema.columns  where TABLE_NAME like 'sales';

-- Standardizing formats
	select OrderDate , ShipDate  from sales limit 10 ; 
	select str_to_date(OrderDate ,  '%Y-%m-%d' ) AS CleanOrderDate ,
    str_to_date(ShipDate ,  '%Y-%m-%d' ) AS CleanShipDate from sales ;
    
	update sales 
		set OrderDate = str_to_date(OrderDate , '%Y-%m-%d'),
			ShipDate = str_to_date(ShipDate ,  '%Y-%m-%d' ) ;
            
	select OrderDate , ShipDate  from sales limit 10 ;
    alter table sales modify OrderDate Date ;
    alter table sales modify ShipDate Date ;
    select data_type from information_schema.columns where table_name like 'sales' and column_name like '%Date%' ;
    
    
-- Checking the missing values 
	select count(*) - count('RowID') from sales ;

-- Remove dublicates 
	Delete t1 from sales t1 
	inner join sales t2
	where 
		t1.RowID > t2.RowID
    and 
		t1.OrderID = t2.OrderID
    and 
		t1.ProductID = t2.ProductID
    ;
    
    
-- Handle Nulls in postalcode 
	update sales 
	set PostalCode = 'Unknown'
	where PostalCode is null ; 

