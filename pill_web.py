# DB
from multiprocessing.sharedctypes import Value
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from wordcloud import wordcloud,STOPWORDS,ImageColorGenerator
import sqlite3
import numpy as np
from PIL import Image
import cv2
from parinya import LINE
import datetime
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Functions
def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate DATE,numpill INTEGER,manypill INTEGER,blog_meal TEXT,str_blog_options TEXT)')
def add_data(author,title,article,postdate,numpill,manypill,blog_meal,str_blog_options):
	st.write('You selected:', author)
	st.write('You selected:', title)
	st.write('You selected:', article)
	st.write('You selected:', postdate)
	st.write('----------------------------------------')
	st.write('You selected:', numpill)
	st.write('You selected:', manypill)
	st.write('You selected:', blog_meal)
	st.write('You selected:', str_blog_options)
	# st.write('You selected:', blog_options[0])
	# st.write('You selected:', blog_options[1])
	c.execute('INSERT INTO blogtable(author,title,article,postdate,numpill,manypill,blog_meal,str_blog_options) VALUES (?,?,?,?,?,?,?,?)',(author,title,article,postdate,numpill,manypill,blog_meal,str_blog_options))
	conn.commit()
def view_all_notes():
	c.execute('SELECT * FROM blogtable')
	data = c.fetchall()
	return data
def view_all_titles():
	c.execute('SELECT DISTINCT title FROM blogtable')
	data = c.fetchall()
	return data
def get_blog_by_title(title):
	c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
	data = c.fetchall()
	return data
def get_blog_by_author(author):
	c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
	data = c.fetchall()
	return data
def delete_data(title):
	c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
	conn.commit()
# def checked():
# 	value = True

# Layout Templates
html_temp = """
<div style="background-color:{};padding:10px;border-radius:10px">
<h1 style="color:{};text-align:center;">AAAAAAAAAAAAAAAAAA </h1>
</div>
"""
title_temp ="""
<div style="background-color:#3dc9b3;padding:10px;border-radius:10px;margin:10px;">
<h5 style="color:black;text-align:center;padding:8px;">{}</h1>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
<h6>Author : {}</h6>
<p style="text-align:justify">Description : {}</p>
<p>Post Date : {}</p>
</div>
"""
article_temp ="""
<div style="background-color:#3dc9b3;padding:10px;border-radius:5px;margin:10px;">
<h5 style="color:white;text-align:center;padding:8px;">{}</h1>
<h6>Author :{}</h6> 
<p>Post Date : {}</p>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
<br/>
<br/>
<p style="text-align:justify">{}</p>
</div>
"""
head_message_temp ="""
<div style="background-color:#3dc9b3;padding:10px;border-radius:5px;margin:10px;">
<h5 style="color:black;text-align:center;padding:8px;">{}</h1>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;">
<h6>Author :{}</h6>
<p>Post Date : {}</p>
</div>
"""
full_message_temp ="""
<div style="background-color:#34B19D;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
<p style="text-align:justify;color:black;padding:10px">Description : {}</p>
</div>
"""

def main():
	"""A Simple CRUD  Blog"""

	st.markdown(html_temp.format('royalblue','white'),unsafe_allow_html=True)

	menu = ["Home","Your Medicine","Add Medicine","Search","Manage Medicine","Pill Counts"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")
		result = view_all_notes()

		for i in result:
			b_author = i[0]
			b_title = i[1]
			b_article = str(i[2])[0:30]
			b_post_date = i[3]
			st.markdown(title_temp.format(b_title,b_author,b_article,b_post_date),unsafe_allow_html=True)

	elif choice == "Your Medicine":
		st.subheader("Your Medicine")
		all_titles = [i[0] for i in view_all_titles()]
		postlist = st.sidebar.selectbox("Your Medicine",all_titles)
		post_result = get_blog_by_title(postlist)
		for i in post_result:
			b_author = i[0]
			b_title = i[1]
			b_article = i[2]
			b_post_date = i[3]
			b_numpill = i[4]
			b_manypill = i[5]
			b_meal = i[6]
			b_str_blog_options = i[7]

			# st.text("Reading Time:{}".format(readingtime(b_article)))
			# st.markdown(head_message_temp.format(b_title,b_author,b_post_date),unsafe_allow_html=True)
			# st.markdown(full_message_temp.format(b_article),unsafe_allow_html=True)
			st.markdown(title_temp.format(b_title,b_author,b_article,b_post_date),unsafe_allow_html=True)

			array_result = b_str_blog_options.split()

			print("ใน your medicine 1. {}".format(len(array_result)))

			if b_meal == 'ยาก่อนอาหาร':
				for i in array_result:
					if  i == 'เช้า':
						before_br = st.checkbox('รับประทาน{0} มื้อ{1} (07 : 00)'.format(b_meal, i))
					elif i == 'เที่ยง':
						before_lun = st.checkbox('รับประทาน{0} มื้อ{1} (12 : 15)'.format(b_meal, i))
					elif i == 'เย็น':
						before_din = st.checkbox('รับประทาน{0} มื้อ{1} (17 : 45)'.format(b_meal, i))
					elif i == 'ก่อนนอน':
						before_sl = st.checkbox('รับประทาน{0} มื้อ{1} (20 : 00)'.format(b_meal, i))
					# st.checkbox("รับประทาน{} มื้อ{}".format(blog_meal,options[0]))
			elif b_meal == 'ยาหลังอาหาร':
				for i in array_result:
					if  i == 'เช้า':
						after_br = st.checkbox('รับประทาน{0} มื้อ{1} (07 : 45)'.format(b_meal, i))
					elif i == 'เที่ยง':
						after_lun = st.checkbox('รับประทาน{0} มื้อ{1} (13 : 00)'.format(b_meal, i))
					elif i == 'เย็น':
						after_din = st.checkbox('รับประทาน{0} มื้อ{1} (18 : 10)'.format(b_meal, i))
					elif i == 'ก่อนนอน':
						after_sl = st.checkbox('รับประทาน{0} มื้อ{1} (20 : 30)'.format(b_meal, i))
	elif choice == "Add Medicine":
		st.subheader("Add information")
		create_table()
		blog_author = st.text_input("Enter username",max_chars=50)
		blog_title = st.text_input("Enter pill name")
		blog_article = st.text_area("Description",height=100)
		blog_post_date = st.date_input("Date")
		col1, col2 = st.columns(2)
		with col1:
			blog_numpill = st.slider('Number of pills',min_value=1,max_value=120,value=20)
		with col2:
			blog_manypill = st.number_input('How many pills do you take each time ?',min_value=1,max_value=8)
		col3, col4 = st.columns(2)
		with col3:
			before_after = st.radio("Medication time",('ยาหลังอาหาร', 'ยาก่อนอาหาร'))
			if before_after == 'ยาก่อนอาหาร':
				blog_meal = "ยาก่อนอาหาร"
			else:
				blog_meal = "ยาหลังอาหาร"
		with col4:
			blog_options =  st.multiselect('Meals time',['เช้า', 'เที่ยง', 'เย็น', 'ก่อนนอน'],['เช้า', 'เที่ยง', 'เย็น', 'ก่อนนอน'])
			print("ใน form Add {} ".format(blog_options))
			str_blog_options = ' '.join(map(str,blog_options))
			print("ใน Add{}".format(str_blog_options))
		# st.write('You selected:', blog_author)
		# st.write('You selected:', blog_title)
		# st.write('You selected:', blog_article)
		# st.write('You selected:', blog_post_date)
		# st.write('----------------------------------------')
		# st.write('You selected:', blog_numpill)
		# st.write('You selected:', blog_manypill)
		# st.write('You selected:', blog_meal)
		# st.write('You selected:', blog_options)
		# st.write('You selected:', blog_options[0])
		# st.write('You selected:', blog_options[1])
		if st.button("Add"):
			add_data(blog_author,blog_title,blog_article,blog_post_date,blog_numpill,blog_manypill,blog_meal,str_blog_options)
			st.success("ได้บันทึกข้อมูลยา {} แล้ว".format(blog_title))

	elif choice == "Search":
		st.subheader("Search Articles")
		search_term = st.text_input('Enter Search Term')
		search_choice = st.radio("Field to Search By",("Pill name","Username"))

		if st.button("Search"):

			if search_choice == "Pill name":
				article_result = get_blog_by_title(search_term)
			elif search_choice == "Username":
				article_result = get_blog_by_author(search_term)

			for i in article_result:
				b_author = i[0]
				b_title = i[1]
				b_article = i[2]
				b_post_date = i[3]
				# st.text("Reading Time: {}".format(readingtime(b_article)))
				# st.markdown(head_message_temp.format(b_title,b_author,b_post_date),unsafe_allow_html=True)
				# st.markdown(full_message_temp.format(b_article),unsafe_allow_html=True)
				st.markdown(title_temp.format(b_title,b_author,b_article,b_post_date),unsafe_allow_html=True)


	elif choice == "Manage Medicine":
		st.subheader("Recorded data")

		result = view_all_notes()
		clean_db = pd.DataFrame(result,columns=["Author","Title","Articles","Post Date","numpill","manypill","blog_meal","เวลารับประทานยา"])
		st.dataframe(clean_db)

		unique_titles = [i[0] for i in view_all_titles()]
		delete_blog_by_title = st.selectbox("Select your pill name to delete",unique_titles)
		new_df = clean_db
		if st.button("Delete"):
			delete_data(delete_blog_by_title)
			st.warning("Deleted: '{}'".format(delete_blog_by_title))

		if st.checkbox("Metrics"):

			new_df['Length'] = new_df['Articles'].str.len()
			st.dataframe(new_df)

			st.subheader("Author Stats")
			new_df["Author"].value_counts().plot(kind='bar')
			st.pyplot()

			st.subheader("Author Stats")
			new_df['Author'].value_counts().plot.pie(autopct="%1.1f%%")
			st.pyplot()

		if st.checkbox("Word Cloud"):
			st.subheader("Generate Word Cloud")
			# text = new_df['Articles'].iloc[0]
			text = ','.join(new_df['Articles'])
			wordcloud = wordcloud().generate(text)
			plt.imshow(wordcloud,interpolation='bilinear')
			plt.axis("off")
			st.pyplot()

		if st.checkbox("BarH Plot"):
			st.subheader("Length of Articles")
			new_df = clean_db
			new_df['Length'] = new_df['Articles'].str.len()
			barh_plot = new_df.plot.barh(x='Author',y='Length',figsize=(20,10))
			st.pyplot()

	elif choice == "Pill Counts":
		def blur_image(image, amount):
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			blur_img = cv2.GaussianBlur(gray, (11, 11), amount)
			canny = cv2.Canny(blur_img, 30, 150, 3)

			return canny
		def dilated_image(image, amount):
			dilated = cv2.dilate(image, (1,1), iterations = amount)
			return dilated
		def erosion_image(image, amount):
			erosion = cv2.erode(image, (1,1), iterations = amount)
			return erosion

		def contour_image(image, image_threshold):
			(cnt, heirarchy) = cv2.findContours(image_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
			cv2.drawContours(image, cnt, -1, (0,255,0), 2)

			return len(cnt)

	#1.แสดงข้อมูลเกี่ยวกับเว็ป
		st.title("Pill Counter")
		st.subheader("This app can count pill or everything in image")
		st.text("We use OpenCV and Streamlit for this demo")

	#2.แถบปรับปรุง
		blur_rate = st.sidebar.slider("Blurring", min_value=0.5, max_value=3.5, value=1.3)
		# brightness_amount = st.sidebar.slider("Brightness", min_value=-50, max_value=50, value=0)
		dilated_amount = st.sidebar.slider("Dilation", min_value=0, max_value=15, value=2)
		erosion_amount = st.sidebar.slider("Erosion", min_value=0, max_value=15, value=1)

	#3.ที่ upload file
		# image_file = st.camera_input("Take a picture")
		# if image_file is not None:
		#     image_file = Image.open(image_file)
		image_file = st.file_uploader("Upload Your Image", type=['jpg', 'png', 'jpeg'])
		if not image_file:
			return None

	#4.ประมวลผล
		original_image = Image.open(image_file)
		original_image = np.array(original_image)

		processed_image = blur_image(original_image, blur_rate)
		# processed_image = brighten_image(processed_image, brightness_amount)
		processed_image = dilated_image(processed_image, dilated_amount)
		processed_image = erosion_image(processed_image, erosion_amount)
		counter_contour_image = contour_image(original_image, processed_image)

	#5.แสดงภาพทั้งสอง
		st.text("Original Image")
		st.image([original_image,])
		st.text("Processed Image")
		st.image([processed_image])
		st.subheader('Count : {}'.format(counter_contour_image))

if __name__ == '__main__':
	main()