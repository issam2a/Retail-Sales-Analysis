-- (Inspecting the data ) sample rows from sales table 

	select * from sales limit 10 ;


-- Basic Exploration:
	-- Count total records (transactions)
		select count(*) as total_transactions from sales ;
    
    -- Count distinct customers
		select  count(distinct CustomerID) as Customers_count from sales ;
    
    -- Count distinct products
		select count(distinct ProductID) as Products_count from sales ;
    
    -- Total sales and profit
		select sum(sales) as total_revenue  , sum(profit) as total_profit  
		from sales ;
    -- Profit Margin 
		select  round((sum(Profit) / sum(Sales) ) *100 ,2) as Profit_margin from sales ;
        
        -- Average Order Value (AOV) Total Sales / Number of Orders
			select round(sum(sales) / count(distinct OrderID) , 2 ) as AOV from sales;
            
	select  count(ShipMode)  , ShipMode 
    from sales
    group by ShipMode
    order by count(ShipMode);
    
    -- One quiry Basic Exploration:
		select count(*) as total_transactions ,
			count(distinct CustomerID) as Customers_count,
            count(distinct ProductID) as Products_count,
            sum(sales) as total_revenue  ,
            sum(profit) as total_profit  
		from sales ;
    
-- Customer Analysis
	-- Top 10 customers by sales
		select CustomerName , sum(sales) as total_sales,
        rank() over(order by sum(sales) desc )  as sales_Rank 
		from sales 
		group by CustomerName 
		order by sales_Rank 
		limit 10;
    
    -- Customers by profit contribution
		select CustomerName , sum(Profit) as Profit_contribution
		from sales 
		group by CustomerName 
		order by Profit_contribution desc
		limit 10;
    -- Sales per Customer
		select round( sum(sales) / count(distinct CustomerID) , 2) from sales ;
        
	-- Repeat Customers → customers with more than 1 order
		select  distinct CustomerName , count(OrderID) from sales 
        group by CustomerName 
        having count(OrderID) > 1 
        order by count(OrderID) desc;
	-- the percentage of customers with more that 1 order 
		SELECT 
    (COUNT(*) / (SELECT COUNT(DISTINCT CustomerName) FROM sales)) * 100 AS repeated_customers_percentage
FROM (
    SELECT CustomerName
    FROM sales
    GROUP BY CustomerName
    HAVING COUNT(OrderID) > 1
) AS repeated_customers;

-- Product Analysis
	-- Best-selling products (by  items soled)
		select ProductName , count(Quantity) as items_soled
        from sales 
        group by ProductName
        order by items_soled desc
        limit 10 ;
    -- Best-selling products (by sales revenue)
    
		select ProductName , sum(sales) as product_total_sales
		from sales 
		group by ProductName
		order by product_total_sales desc
		;
    -- Most profitable sub-categories
		select SubCategory , sum(Profit) as subcategory_profit 
		from sales 
		group by SubCategory 
		order by subcategory_profit desc
		;
    
    -- Products with negative profit (loss-makers)
   
		select ProductName , sum(Profit) as total_loss 
        from sales 
        group by ProductName
        having total_loss <0 
		order by total_loss asc
        ;
	-- Low Margin Products → products where Profit Margin < 20%
		select
			ProductName,
            Category,
            SubCategory,
			sum(sales) as total_sales ,
			sum(Profit) as total_profit ,
            round(sum(Profit) / sum(sales) ,2 ) * 100  as profit_margin 
            from sales 
            group by ProductName ,Category,SubCategory
            having profit_margin  > 20 
            order by profit_margin desc;
            
-- Regional & Segment Analysis
	-- Sales by region 
		select Region , sum(sales) as sales_by_region 
        from sales 
        group by Region 
        order by sales_by_region desc
        ;
        
	-- Sales by segment
		select segment , sum(sales) as segment_sales 
        from sales 
        group by segment 
        order by segment_sales desc 
        ;
        
	-- Sales by state (Top 10) 
		select state , sum(sales) as total_state_sales 
        from sales 
        group by state 
        order by total_state_sales desc 
        limit 10 ;
        
-- Time Analysis
	-- Sales by year
		select  year(OrderDate) as Order_year ,sum(sales) as sales_by_year
        from sales 
        group by  year(OrderDate)
        order by sales_by_year desc
        ;
        
	-- Sales by month 
		select month , sales_by_month , rank() over(order by sales_by_month desc) as sales_rank 
        from (
			select month(OrderDate) as month  , sum(sales) as sales_by_month
			from sales 
			group by month(OrderDate)  
			
            ) as monthly_sales
            order by sales_rank
        ;
        
     -- sales by year and month 
			select month , year ,total_sales , rank() over(order by total_sales desc) as sales_rank 
            from (
 			select month(OrderDate) as month ,
			year(OrderDate) as year ,
			sum(sales) as total_sales 
			from sales 
			group by  year(OrderDate), month(OrderDate) 
			order by  year(OrderDate) , month(OrderDate) 
            ) as yearly_sales 
            order by sales_rank;

        
	-- Seasonality Analysis quarters with peak sales
			select month , year ,quarter , total_sales , rank() over(order by total_sales desc ) as sales_rank 
        
			from (
 			select month(OrderDate) as month , quarter(OrderDate) as quarter ,
			year(OrderDate) as year ,
			sum(sales) as total_sales 
			from sales 
			group by  year(OrderDate), month(OrderDate) , quarter(OrderDate)
			order by  year(OrderDate) , month(OrderDate) , quarter(OrderDate)
            ) as yearly_sales 
            order by sales_rank;
-- Shipping analysis 
	-- Orders by Ship Mode distribution of shipping methods
		select ShipMode , count(OrderID) as Orders_count 
        from sales 
        group by ShipMode 
        order by orders_count desc ;
        
        -- percentage distribution 
			
			select ShipMode ,
            count(OrderID) as Orders_count ,
            (count(OrderId) / (select count(*) from sales ) *100) as Order_percentage
			from sales 
			group by ShipMode 
			order by orders_count desc;
		-- Average Shipping Time 
			select ShipMode , avg(datediff(ShipDate , OrderDate)) as avg_Shipment_days 
            from sales 
            group by ShipMode
            order by avg_Shipment_days ;
            
            
            
           select ShipMode , DATEDIFF(ShipDate, OrderDate) as days 
           from sales 
           where ShipMode like 'Same Day' and DATEDIFF(ShipDate, OrderDate) > 1;
           
            