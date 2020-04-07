# ShopBot
Selenium Python Webdriver, that searchs and buys products from Supremenewyork.com during drop time at 11:00 AM EST.

## Getting Started
pip install -r requirements.txt

## Deployment

Edit src/customer.json file to find exactly what items you want to search. Customer.json allows the following

### 1.) Items

Clothing article name
  * jackets
  * shirts
  * pants
  * sweatshirts
  * sweaters
  * hats
  * bags
  * shoes
  * skate
  * t-shirts
  * accessories
  
Fields
  * name : [Any name without specal characters inside]
  * color : ['Red','Gold','Pink'..etc]
  * size : ['S','M','L','XL']

### 2.) Payment

Payment Information
  * name 
  * email
  * phone
  * address
  * apt_num
  * zip
  * town
  * card
  * cvv
  * state
  * country
  * card_expiration_month
  * card_expirtaion_year 

 === See customer.json for template example === 
  
  
