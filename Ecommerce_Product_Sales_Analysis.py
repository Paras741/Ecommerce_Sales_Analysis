#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick


# In[2]:


df = pd.read_csv('ecommerce_product_dataset.csv')


# In[3]:


df['DateAdded'] = pd.to_datetime(df['DateAdded'])


# # Sales and Prizes Analysis

# Q1 : What is the relationship between the price of a product and its sales?

# In[4]:


# Compute correlation using numpy
correlation = df['Price'].corr(df['Sales'])
print("Correlation :", correlation)


# Ans: A correlation coefficient is very close to 0, indicating that there is almost no linear relationship between Price and
# Sales. This means that changes in one variable do not predict changes in the other variable.

# Q2: How do discounts impact the sales of products?

# In[5]:


df.head()


# In[6]:


df['Discount'].corr(df['Sales'])


# Ans: The correlation between discount and sales is weak, suggesting that discounts alone do not significantly impact sales.

# Q3: Analyze Discount Effectiveness by Discount Ranges?

# In[7]:


df.head()


# In[8]:


df['Discount'].unique()


# In[9]:


discount_bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
discount_labels = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%']
df['DiscountRange'] = pd.cut(df['Discount'], bins=discount_bins, labels=discount_labels)


# In[10]:


# Calculate average sales for each discount range
average_sales_by_discount = df.groupby('DiscountRange')['Sales'].mean().reset_index()


# In[11]:


average_sales_by_discount


# In[12]:


# visualizing
sns.barplot(data = average_sales_by_discount, x = 'DiscountRange', y = 'Sales')
plt.title('Average Sales by Discount Range')
plt.xlabel('Discount Range')
plt.ylabel('Average Sales')
plt.grid(True)
plt.show()


# Ans: As we can see above plot Providing 20-30% Discount increasing more sales volumne.

# Q4: Which price range has the highest sales volume?

# In[13]:


df.head()


# In[14]:


# Creating Price_range column
conditions = [
    
    (df['Price'] >= 10) & (df['Price'] < 50),
    (df['Price'] >= 50) & (df['Price'] < 100),
    (df['Price'] >= 100) & (df['Price'] < 150),
    (df['Price'] >= 150) & (df['Price'] < 200),
    (df['Price'] >= 200) & (df['Price'] < 250),
    (df['Price'] >= 250) & (df['Price'] < 300),
    (df['Price'] >= 300) & (df['Price'] < 350),
    (df['Price'] >= 350) & (df['Price'] < 400),
    (df['Price'] >= 400) & (df['Price'] < 450),
    (df['Price'] >= 450) & (df['Price'] < 500)
]
choices = ['10-50','50-100','100-150','150-200','200-250','250-300','300-350','350-400','400-450','450-500']
df['Price_range'] = np.select(conditions,choices, default = 'other')


# In[149]:


sales_by_price = df.groupby('Price_range')['Sales'].mean().sort_values(ascending = False).reset_index()


# In[152]:


plt.figure(figsize=(8,5))
sns.barplot(data = sales_by_price, x = 'Price_range', y = 'Sales')
plt.title('Average Sales by Price')
plt.xlabel('Price Range')
plt.ylabel('Sales')
plt.xticks(rotation = 45)
plt.grid(True)
plt.show()


# As we can see above plot prize range b/w 250 - 300 has the highest sales volume.

# # Category Performance Analysis

# Q5: Which product category generates the most revenue?

# In[16]:


df.head()


# In[17]:


df['Revenue'] = df['Price'] * df['Sales'] # adding revenue column


# In[18]:


top_category = df.groupby('Category')['Revenue'].sum().sort_values(ascending = False).reset_index().head(10)


# In[19]:


plt.figure(figsize = (8,7))
plt.bar(top_category['Category'], top_category['Revenue'], color='skyblue')
plt.xlabel('Category')
plt.ylabel('Total Revenue')
plt.title('Total Revenue by Product Category')
plt.xticks(rotation=76)
formatter = mtick.StrMethodFormatter('${x:,.0f}')
plt.gca().yaxis.set_major_formatter(formatter)


# Q5: How does the average rating vary across different product categories?

# In[20]:


avg_rating_by_category = df.groupby('Category')['Rating'].mean().reset_index().sort_values(by = 'Rating',ascending = False)


# In[21]:


plt.bar(avg_rating_by_category['Category'], avg_rating_by_category['Rating'])
plt.xlabel('Product Category')
plt.ylabel('Average Rating')
plt.title('Average Rating by Product Category')
plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility
plt.show()


# Q6: Which category has the highest average discount?

# In[22]:


df.head()


# In[23]:


df.groupby('Category')['Discount'].mean().sort_values(ascending = False).plot(kind = 'line')
plt.show()


# Ans: Makeup has the highest average discount around 27.65 %

# # Customer Reviews and Ratings

# Q7: is there a correlation between the number of reviews and the rating of a product?

# In[24]:


df.head()


# In[25]:


df['NumReviews'].corr(df['Rating'])


# Ans: It is very close to 0. Hence there is no correlation

# Q8: Do higher-rated products have significantly more sales?

# In[26]:


df.head()


# In[27]:


df['Rating'].corr(df['Sales'])


# Ans: It is very close to 0. Hence there is no linear correlation

# Q9: What is the distribution of ratings across all products?

# In[28]:


plt.hist(df['Rating'], bins=10, edgecolor='black')
plt.show()


# Ans: Products rated between 3.0 and 3.5 are often seen as average. They meet basic expectations but do not exceed them.
# Consistency: A high concentration of ratings in this range might indicate consistency in product quality, but not necessarily high quality.

# # Stock and Inventory Analysis

# Q10: Are there any products with high stock but low sales? What are the potential reasons?

# In[29]:


df.head()


# In[30]:


# dentify Products with High Stock and Low Sales
high_stock_threshold = df['StockQuantity'].quantile(0.75)  # Top 25% stock levels
low_sales_threshold = df['StockQuantity'].quantile(0.25)  # Bottom 25%

# Identify products with high stock but low sales
high_stock_low_sales = df[(df['StockQuantity'] > high_stock_threshold) & (df['Sales'] < low_sales_threshold)]
high_stock_low_sales.head()


# In[31]:


plt.figure(figsize=(10, 5))
plt.scatter(df['StockQuantity'], df['Sales'])
plt.axvline(high_stock_threshold, color='red', linestyle='--', label='High Stock Threshold')
plt.axhline(low_sales_threshold, color='blue', linestyle='--', label='Low Sales Threshold')
plt.xlabel('StockQuantity')
plt.ylabel('Sales')
plt.title('Stock vs. Sales')
plt.legend()
plt.show()


# Q11: What is the turnover rate for each product category?

# In[32]:


df.head()


# In[33]:


# Calculate turnover rate for each product category using stock
turnover_rate_by_category = df.groupby('Category').apply(lambda x: x['Sales'].sum() / x['StockQuantity'].mean())


# In[34]:


tr = turnover_rate_by_category.to_frame('Turn Over Rate').reset_index().sort_values(by='Turn Over Rate', ascending = False)


# In[35]:


sns.scatterplot(data = tr, x = 'Category', y = 'Turn Over Rate')
plt.xticks(rotation = 90)
plt.show()


# # Temporal Analysis

# Q12: How does the sales volume change over time? Are there any noticeable trends or seasonal patterns?

# In[36]:


df.head()


# In[37]:


df['year_month'] = df['DateAdded'].dt.strftime('%Y-%m')


# In[38]:


sales_over_time = df.groupby('year_month')['Sales'].sum().reset_index()


# In[39]:


plt.figure(figsize=(11, 6))
plt.plot(sales_over_time['year_month'], sales_over_time['Sales'], marker='o', linestyle='-')
plt.title('Sales Volume Over time')
plt.xlabel('Year_Month')
plt.ylabel('Sales Volume')
plt.grid(True)
plt.xticks(fontsize = 8)
plt.show()


# Q13: Are newer products selling better than older ones?

# In[ ]:


# step 1: Calculate the Age of Each Product


# In[40]:


from datetime import datetime


# In[54]:


current_date = datetime.now()


# In[55]:


current_date


# In[56]:


# Calculate the age of each product
df['ProductAgeDays'] = (current_date - df['DateAdded']).dt.days


# In[ ]:


# step 2: Analyze the Relationship Between Product Age and Sales


# In[63]:


age_sales_correlation = df[['ProductAgeDays', 'Sales']].corr().iloc[0, 1]
print(f'Correlation between Product Age and Sales: {age_sales_correlation}')


# Ans: there is no correlation

# # Discount Effectiveness

# Q14 : What is the average discount given across all products?

# In[64]:


df.head()


# In[73]:


print("Ans: Average discount across all products:", df['Discount'].mean() * 100)


#  # Revenue Analysis

# Q15: Which products generate the most revenue?

# In[95]:


top_5_products = df.groupby('ProductName')['Revenue'].sum().sort_values(ascending = False).reset_index().head(5)


# In[115]:


plt.pie(top_5_products['Revenue'], labels = top_5_products['ProductName'], autopct = '%.0f%%', shadow = True,colors = ['skyblue', 'lightyellow', 'lightgreen', 'orange','lightpink'])
plt.show()


# Q16: What is the total revenue generated by the top 10% of products?

# In[127]:


top_10_products = df.groupby('ProductName')['Revenue'].sum().sort_values(ascending = False).reset_index()


# In[132]:


top_10_percent = top_10_products.head(10)


# In[135]:


total_revenue_top_10_percent = top_10_percent['Revenue'].sum()


# In[136]:


total_revenue_top_10_percent


# Ans: 47118758.20999999 is the total revenue generated by the top 10% of products

# In[154]:


df.groupby('Price_range')['Sales'].mean().sort_values(ascending = False).reset_index()


# In[ ]:




