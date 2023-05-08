import pandas as pd
import streamlit_pandas as sp
import json
import streamlit as st
from streamlit_lottie import st_lottie
import requests
from streamlit_option_menu import option_menu
from PIL import Image
import os
import io
import sqlite3



st.set_page_config(page_title="Marlo",layout="wide")
st.title(" Marlo Shopping👗")
with st.sidebar:
    select=option_menu(None, ["Home", "My Account","Admin", "Shopping","Contact",'Feedback'], 
        icons=['house','person','key','shop', 'person-lines-fill','chat-dots'], 
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "Purple", "font-size": "25px"}, 
            "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "pink"},})
image1=Image.open(r"C:\Users\Aswini Praba\Desktop\completedproject\colaninfoimage.jpeg")
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()
lottie_s=load_lottieurl(r"https://assets1.lottiefiles.com/private_files/lf30_x2lzmtdl.json")

if select=="Home":
    with st.container():
     image_column,text_column=st.columns((1,2))
     with image_column:
      st.image(image1)
      st.subheader("India, HeadQuarters")
      st.write("""
                  HQ: Unit-2, D 84, B Block, 4th Floor,
                  Murugesa Nayakar Building Greams Road,
                  Thousand Lights West, Thousand Lights,
                  CH – 600006 Phone: 044 42844666""")
     with text_column:
      st.write(
			"""Marlo by Colan Infotech is an online shopping website,
                        here you can shop online for latest apparel,Home decor,Fragrances,
                        Accessories,watches,Furnitures.We are providing express delivery for
                        all orders in India.
                                
                                """)
      st.write("""
                       Our site takes care of all your needs from electronics to babycare.
                       Shop from the comfort of your home while enjoying many other
                       things!Shop a range of your favorite brands with exclusive discounts and
                       offers only at Marlo Shopping!
    
			"""
		)
      st.title("Treat Yourself by Shopping in MARLO!!!!")

     st_lottie(
            lottie_s,
            speed=0.1,
            reverse=False,
            loop=True,
            quality="low",
            height=500,
            width=None,
            key=None
            )

class User:
    def __init__(self, conn):
        self.conn = conn

    def register(self):
        name = st.text_input("Enter Your Name:")
        gender = st.radio("Select your gender", ["Male", "Female", "Others"])
        age = st.slider("Enter Your age", 18, 150)
        mobile_no = st.text_input("Enter Your mobile Number:")
        email_id = st.text_input("Enter Your Email_id:")
        password = st.text_input("Enter your Password:", type="password")
        recovery_mail = st.text_input("Enter Recovery email_id:")
        submit = st.button("Submit")
        if submit:
            data = {
                "Name": name,
                "Gender": gender,
                "Age": age,
                "Mobile_Number": mobile_no,
                "Email_ID": email_id,
                "Password": password,
                "Recovery_Email": recovery_mail,
            }
            df = pd.DataFrame(data, index=[0])
            st.write(df)

            cursor = self.conn.cursor()
            create_sql = "CREATE TABLE IF NOT EXISTS user_details(Name VARCHAR(255),Gender VARCHAR(255),Age VARCHAR(255),Mobile_Number VARCHAR(255),Email_ID VARCHAR(255),Password VARCHAR(255),Recovery_Email VARCHAR(255))"
            cursor.execute(create_sql)

            for row in df.itertuples():
                insert_sql = "INSERT INTO user_details(Name,Gender,Age,Mobile_Number,Email_ID,Password,Recovery_Email) VALUES(?,?,?,?,?,?,?)"
                cursor.execute(
                    insert_sql,
                    (
                        row.Name,
                        row.Gender,
                        row.Age,
                        row.Mobile_Number,
                        row.Email_ID,
                        row.Password,
                        row.Recovery_Email,
                    ),
                )
                self.conn.commit()

            st.write("User registered successfully!")

    def login(self):
        email = st.text_input("Enter your email ID: ")
        password = st.text_input("Enter your password: ", type="password")
        done = st.button("Done")
        if done:
            cursor = self.conn.cursor()
            query = "SELECT * FROM user_details WHERE Email_ID=? AND Password=?"
            parameters = (email, password)
            cursor.execute(query, parameters)
            result = cursor.fetchone()

            if result:
                st.write("Login successful!")
                st.session_state.logged_in=True
                return result[0]
            else:
                st.write("Invalid email ID or password.")
                return None



if select == "My Account":
    conn=sqlite3.connect('marlo.db')
    user=User(conn)
    user_reg=st.selectbox("",["Register(New User)","Login(Already Registered)"],0)
    if user_reg=="Register(New User)":
        user.register()
    if user_reg=="Login(Already Registered)":
        user.login()



###############################################        
class catalogue:
    def __init__(self, conn):
        self.conn = conn

    def upload_product_details(self):
        name = st.text_input('Product Name')
        description = st.text_input('Product Description')
        price = st.number_input('Product Price')
        avail=st.radio("Select the availability", ["True", "False"])
        image = st.file_uploader('Product Image', type=['jpg', 'jpeg', 'png'])
        if image is not None:
            image_bytes = image.read()
        upload= st.button('Upload')
        if upload and name and description and price and avail:
            data_dict = {'Name': name, 'Description': description, 'Price': price,'Availability':avail, 'Image': image_bytes,}
            df1=pd.DataFrame(data_dict,index=[0])
            st.write(df1)
            cursor = self.conn.cursor()
            create_sql = "CREATE TABLE IF NOT EXISTS product_details_new(Name VARCHAR(255),Description VARCHAR(255),Price VARCHAR(255),Availability VARCHAR(255),Image blob)"
            cursor.execute(create_sql)
            for row in df1.itertuples():
                insert_sql = "INSERT INTO product_details_new(Name,Description,Price,Availability,Image) VALUES(?,?,?,?,?)"
                cursor.execute(
                    insert_sql,
                    (
                        row.Name,
                        row.Description,
                        row.Price,
                        row.Availability,
                        row.Image,
                    ),
                    )
                self.conn.commit()
            st.success('Product details are uploaded Successfully')
            
    def display_product_details(self):
        cursor = self.conn.cursor()
        select_sql = "SELECT Name, Description, Price,Availability, Image FROM product_details_new"
        cursor.execute(select_sql)
        data1 = cursor.fetchall()
        for row in data1:
            left_column,right_column=st.columns(2)
            with left_column:
                st.write('Product Name:', row[0])
                st.write('Product Description:', row[1])
                st.write('Product Price:', row[2])
                st.write('Product Availability:', row[3])
            with right_column:
                image = Image.open(io.BytesIO(row[4]))
                resize_image=image.resize((1000,1000))
                st.image(resize_image,width=250,caption=row[0])
    def delete_product_details(self):
        prod_name = st.text_input('Enter product name to delete')
        delete = st.button('Delete')
        if delete and prod_name:
            cursor = self.conn.cursor()
            delete_sql = "DELETE FROM product_details_new WHERE Name=?"
            cursor.execute(delete_sql, (prod_name,))
            self.conn.commit()
            st.success('Product details deleted Successfully')
        
if select == "Admin":
    conn=sqlite3.connect('marlo.db')
    cat=catalogue(conn)
    prod_reg=st.selectbox("",["Upload_prod_details","display_product_details","Delete_product_details"],0)
    if prod_reg=="Upload_prod_details":
        cat.upload_product_details()
    elif prod_reg=="display_product_details":
        cat.display_product_details()
    elif prod_reg=="Delete_product_details":
        cat.delete_product_details()
##################################
class shopping:
    def __init__(self, conn):
        self.conn = conn
    def show_product_details(self):
        cursor = self.conn.cursor()
        select_sql = """
        SELECT
            pd.Name,
            pd.Description,
            pd.Price,
            pd.Availability,
            pd.Image,
            AVG(pr.Rating) AS AvgRating
        FROM product_details_new pd
        LEFT JOIN product_reviews pr ON pd.Name = pr.product_name
        GROUP BY pd.Name, pd.Description, pd.Price, pd.Availability, pd.Image
        ORDER BY AvgRating DESC
        """
        cursor.execute(select_sql)
        data1 = cursor.fetchall()

        for row in data1:
            left_column,right_column=st.columns(2)
            with left_column:
                st.write('Product Name:', row[0])
                st.write('Product Description:', row[1])
                st.write('Product Price:', row[2])
                st.write('Product Availability:', row[3])
                st.write('Average Rating:', row[5])

            with right_column:
                image = Image.open(io.BytesIO(row[4]))
                resize_image=image.resize((1000,1000))
                st.image(resize_image,width=250,caption=row[0])

#############################################################################

    def purchase_product(self):
        if not st.session_state.get("logged_in"):
            st.write("Please log in first")
            return
        email_id=st.text_input('Enter email id')
        prod_name = st.text_input('Enter product name to purchase')
        quantity = st.number_input('Enter quantity')
        quantity=int(quantity)
        purchase = st.button('Purchase')
        if purchase and prod_name and quantity:
            cursor = self.conn.cursor()
            select_sql = "SELECT Name,Price, Availability FROM product_details_new WHERE Name=?"
            cursor.execute(select_sql, (prod_name,))
            data1 = cursor.fetchone()
            cursor = self.conn.cursor()
            create_sql2 = "CREATE TABLE IF NOT EXISTS purchase_details(email_id VARCHAR(255),product_name VARCHAR(255),Quantity VARCHAR(255),Total_Price VARCHAR(255))"
            cursor.execute(create_sql2)
            if data1:
                product_name=data1[0]
                price = data1[1]
                price=float(price)
                availability = data1[2]
                if availability == "True":
                    total_price = price * quantity
                    st.success(f'Your order for {quantity} {prod_name}(s) has been placed. Total Price: {total_price}')
                    insert_sql = "INSERT INTO purchase_details (email_id, product_name, Quantity, Total_Price) VALUES (?, ?, ?, ?)"
                    insert_parameters = (email_id, product_name, quantity, total_price)
                    cursor.execute(insert_sql, insert_parameters)
                    self.conn.commit()

                else:
                    st.warning(f'{prod_name} is currently out of stock')
            else:
                st.error(f'Product {prod_name} not found')



    def give_review(self, user_id):
        
        cursor = self.conn.cursor()
        purchase_check_sql = "SELECT p.product_name FROM purchase_details p INNER JOIN user_details u ON u.Email_ID=p.email_id WHERE u.Email_ID=?"

        cursor.execute(purchase_check_sql, (user_id,))
        user_purchases = cursor.fetchall()
        cursor = self.conn.cursor()
        create_sql2 = "CREATE TABLE IF NOT EXISTS product_reviews(product_name VARCHAR(255),email_id VARCHAR(255),Rating VARCHAR(255),Review VARCHAR(255))"
        cursor.execute(create_sql2)        
        if user_purchases:
            product_names = [row[0] for row in user_purchases]
            product_name = st.selectbox("Select a product to review", product_names)
            review_rating=st.radio("Give Rating",["1","2","3","4","5"])
            review_text = st.text_input("Enter your review")
            submit = st.button("Submit Review")
            if submit and review_rating and review_text:
                product_id = next(row[0] for row in user_purchases if row[0] == product_name)
                insert_sql = "INSERT INTO product_reviews (product_name, email_id,Rating, Review) VALUES (?, ?, ?,?)"
                insert_parameters = (product_name, user_id,review_rating, review_text)
                cursor.execute(insert_sql, insert_parameters)
                self.conn.commit()
                st.success("Review submitted successfully.")
        else:
            st.warning("You haven't purchased any products yet.")




if select == "Shopping":
    conn=sqlite3.connect('marlo.db')
    shop=shopping(conn)
    shop_prod=st.selectbox("",["Product_list","purchase_product","Add_Review"],0)
    if shop_prod=="Product_list":
        shop.show_product_details()
    elif shop_prod=="purchase_product":
        user=User(conn)
        user.login()
        shop.purchase_product()
    elif shop_prod=="Add_Review":
        user=User(conn)
        user.login()
        user_id=st.text_input("Enter the mail_id:")
        shop.give_review(user_id)
        

#######################################################################################################
if select == "Contact":
    aboutme ="""I am interested in pursuing a career as a python developer
                  and eager to learn and grow in this field
                  and working towards becoming a professional in
                  this exciting and rapidly evolving field.!"""
    links={
        "GITHUB": "https://github.com/Aswini-Prabha",
        "LINKEDIN": "https://www.linkedin.com/in/aswini-prabha-a32229268/"}
    column1, column2= st.columns(2)
    with column1:
        column1.image(Image.open(r"C:\Users\Aswini Praba\Documents\Me\photograph.jpg.jpg"),width=150)
    with column2:
        st.subheader("AswiniPrabha")
        st.subheader(f'{"Mail :"}  {"aswiniprabha22@gmail.com"}')
        st.write(aboutme)
        S=st.columns(len(links))
        for i, (x, y) in enumerate(links.items()):
             S[i].write(f"[{x}]({y})")

#######################################################################################################

if select=='Feedback':
    with st.container():
        st.write('---')
        st.subheader("Hope you enjoyed using this webpage!!!:thumbsup:")
        st.write("Please provide your valuable Feedback!!!:speech_balloon:")
        st.write("##")
        contact_form="""
        <form action="https://formsubmit.co/aswiniprabha22@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">      
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here" required></textarea>
            <button type="submit">Send</button>
        </form>
        """
        left_column,right_column=st.columns(2)
        with left_column:
            st.markdown(contact_form,unsafe_allow_html=True)
        with right_column:
            st.caption("Made with ❤️ by @aswinitheaspiringPD")
