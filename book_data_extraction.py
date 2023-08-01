from bs4 import BeautifulSoup
import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}
data_frames_list=[]
data=[]
product_name=[]
product_prize=[]
product_author=[]
product_formate=[]
image_link=[]
star=[]
category=[]
url1= "https://www.awesomebooks.com/books/category/303/fiction?page="
url2= "https://www.awesomebooks.com/books/category/8211/crime--thriller?page="
url3= "https://www.awesomebooks.com/books/category/8214/sci-fi-fantasy--horror?page="
url=[url1, url2, url3]
category_name = ["Fiction", "Crime/Thrill/", "Science/Horror"]
for k in range(3):
    for i in range (1,500):
        URL = f'{url[k]}{i}'
        response = requests.get(url=URL, headers=headers)
        soup  =BeautifulSoup(response.text, "html.parser")
        div_css= soup.select("li.col-6 div.product-item__inner")
        data_frame = pd.DataFrame()
        for j , tag in enumerate(div_css):
            name=tag.select_one("li.col-6 a.font-weight-bold").text.strip()
            prize=tag.select_one("li.col-6 div.product-price span").text.strip()
            author_elem = tag.select_one("li.col-6 h5.mb-1.book_author a")
            author = author_elem.text.strip() if author_elem else "Unknown Author"
            formate = tag.select_one("li.col-6 span.text-gray-6").text.strip()
            image = tag.select_one('li.col-6 img[src]')['src'].strip()
            rating_star=len(tag.select(".fa-star,.fa-star-half"))
            rating=rating_star/2
            product_name.append(name)
            product_author.append(author)
            product_formate.append(formate)
            product_prize.append(prize)
            image_link.append(image)
            star.append(rating)
            category.append(category_name[k])
        # print(star)
zipped = list(zip(product_name, product_author, product_formate, product_prize, star, category, image_link))
df = pd.DataFrame(zipped, columns=['Product_Name', 'Product_Author', 'Product_Formate', 'Product_Prize', 'Product_Star_Rating', 'Product_Category', 'Product_Image_Link'])

print(df)
#Data Frame convert into CSV file
df.to_csv("Book.csv")