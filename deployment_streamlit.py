#%%writefile app.py 
import streamlit as st
from io import StringIO
import pandas as pd
import joblib
from PIL import Image
from colored import fg
import nltk,re,time,os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
color = fg('blue')
# 
@st.cache_data()# to prevent this function to run every time when you perform some action on app
def load_data():
    #st.write("I ran !") # <--- this should be printed on your app each time this function is run
    filename = "/Users/pratikdomadiya/Desktop/Jupyter Codes/project_AIP/trained_models/finalized_model.sav"

    loaded_pipe = joblib.load(filename)
    print("loaded model")

    return loaded_pipe
def preprocess_text(reviews):
    res =[]
    for review in reviews:  
        # Convert review to lowercase
        review = review.lower()
        
        # Code to remove the Hashtags from the text
        review=re.sub(r'\B#\S+','',review)
        # Code to remove the links from the text
        review=re.sub(r"http\S+", "", review)
        # Code to remove the Special characters from the text 
        review=' '.join(re.findall(r'\w+', review))
        # Code to substitute the multiple spaces with single spaces
        review=re.sub(r'\s+', ' ', review, flags=re.I)
        # Code to remove all the single characters in the text
        review=re.sub(r'\s+[a-zA-Z]\s+', '', review)
        # Remove the twitter handlers
        review=re.sub('@[^\s]+','',review)

        # tokenize and remove the stopwords    
        filtered_sentence = [] 

        stop_words = set(stopwords.words('english')) 

        word_tokens = word_tokenize(review) 

        filtered_sentence = [w for w in word_tokens if not w in stop_words] 
        
        #make a sentence 
        make_sentence = ' '.join([i+' ' for i in filtered_sentence])
        make_sentence=re.sub(r'\s+', ' ', make_sentence, flags=re.I)
        
        # lemmatize the sentence
        lemmatizer = WordNetLemmatizer()
        example = make_sentence
        output_sentence =[]
        word_tokens2 = word_tokenize(example)
        lemmatized_output = [lemmatizer.lemmatize(w) for w in word_tokens2]

        # Remove characters which have length less than 2  
        without_single_chr = [word for word in lemmatized_output if len(word) > 2]
        # Remove numbers
        cleaned_data_title = [word for word in without_single_chr if not word.isnumeric()]
            
        #make a sentences 
        make_sentence = ' '.join([i+' ' for i in cleaned_data_title])
        lemmatized_sentence=re.sub(r'\s+', ' ', make_sentence, flags=re.I)
        print(lemmatized_sentence)
        res.append(lemmatized_sentence)
    return res








# title of our steamlit page
original_title = '<p style=" font-family:cursive; color:yellow; font-size: 59px;">Movie Review Sentiment Analysis</p>'
st.markdown(original_title, unsafe_allow_html=True)
original_title = '<p style="text-align: center; font-family:arial; color:white; font-size: 50px;"><b>AIP - Group D6</b></p>'
st.markdown(original_title, unsafe_allow_html=True)
# background-image: url("https://www.excellarate.com/wp-content/uploads/2021/04/Blog-A-Modern-Hands-On-Approach-to-Sentiment-Analysis.jpg");

st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i0.wp.com/wwcsff.com/wp-content/uploads/2019/05/film-background-1334067869u9d.jpg");
             background-attachment: fixed;
             background-size: cover;
             
         }}
         .stApp {{

         }}
         
         </style>
         """,
         unsafe_allow_html=True
     )

def clear_form():
    st.session_state["review"] = ""
    st.session_state["output"] = ""


# def set_background(png_file):
# set_background('/content/sentiment-analysis.png')
# Creating input box for reviews
form = st.form(key='sentiment-form')
user_input = form.text_area('Enter your review', key="review")
submit = form.form_submit_button('Get  Sentiment')
#app_output = form.text_input('See output ',key="output")
col1, col2= st.columns(2)
reset = col1.button('Start Over',on_click=clear_form)
# fileupload = col2.button('fileupload',on_click=clear_form)


uploaded_file = col2.file_uploader("Upload Reviews (*.txt)",type=['txt'],key="file_uploader")

    # # Can be used wherever a "file-like" object is accepted:
    # dataframe = pd.read_csv(uploaded_file)
    # st.write(dataframe)

# title = "dialog box"




# # dialog box 
# modal = st.expander("Rate Your Experience")
# genre = modal.radio(
#     "select your choice",
#     ('Agree', 'Not Sure!!', 'Disagree',"Don't care"),key='radio')

# if genre == 'Agree':
#     st.write('You selected comedy.')
# else:
#     st.write("You didn\'t select comedy.")

def save_review_to_excel(review,prediction):
    prediction=['Positive' if pred==1 else 'Negative'  for pred in prediction]
    file_name = time.strftime("%Y_%m_%d.xlsx")
    t_= time.strftime("%H:%M:%S")
    print(file_name,time)
    path="./user_reviews/"+file_name
    if (os.path.exists(path) == False):
        # review=['first line of review']
        # prediction = ['Negative']
        time_=[t_ for t in range(len(review))]
        # dataframe with Name and Age columns
        df = pd.DataFrame({'Review': review, 'Model-prediction': prediction, 'Entry-time':time_})

        # create a Pandas Excel writer object using XlsxWriter as the engine
        writer = pd.ExcelWriter(path, engine='xlsxwriter')

        # write data to the excel sheet
        df.to_excel(writer, sheet_name='Sheet1', index=False)

        # close file
        writer.close()
    else:
        print("File Exists")
        # review=['third line of review','forth line of review']
        # prediction = ['Positive','Negative']
        time_=[t_ for t in range(len(review))]
        # new dataframe with same columns
        df = pd.DataFrame({'Review': review, 'Model-prediction': prediction, 'Entry-time':time_})

        # read  file content
        reader = pd.read_excel(path)

        # create writer object
        # used engine='openpyxl' because append operation is not supported by xlsxwriter
        writer = pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists="overlay")

        # append new dataframe to the excel sheet
        df.to_excel(writer, index=False, header=False, startrow=len(reader) + 1)

        # close file
        writer.close()



def my_widget(key):
    # st.subheader("")
    image = Image.open('/Users/pratikdomadiya/Desktop/Jupyter Codes/project_AIP/project images/Screenshot 2023-03-26 at 7.46.43 PM.png')
    new_image = image.resize((125, 125))
    st.image(new_image, caption='Developed by')
    st.markdown("Play around with this excellent Movie review sentiment analysis tool which help you to keep a close eye on your brand’s reputation, find out what is right or wrong about your business, and understand more about your customers")
    
    st.subheader("AIP - Group D6")
    st.subheader("Mentor : Prof. Jagmohan Dutta")
    
    image = Image.open('/Users/pratikdomadiya/Desktop/Jupyter Codes/project_AIP/project images/Screenshot 2023-03-26 at 8.26.23 PM.png')
    new_image = image.resize((125, 125))
    st.image(new_image, caption='Support by')
    # return st.button("Click me " + key)
#
# # This works in the main area
# clicked = my_widget("first")

# # And within an expander
# my_expander = st.expander("Expand", expanded=True)
# with my_expander:
#     clicked = my_widget("second")

st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)
# AND in st.sidebar!
st.sidebar.title("About Us")
with st.sidebar:
    clicked = my_widget("third")


if submit and user_input:
    #st.write(f'hello user')
    #form.text('This is some text.')
    loaded_pipe = load_data()
    print("submit")
    reviews = []
    reviews.append(user_input)
    reviews=preprocess_text(reviews)
    result = loaded_pipe.predict(reviews)
    print(result)
    res ={'Negative':0,'Positive':0}
    if result[0]==0: res['Negative']+=1 
    else: res['Positive']+=1
    # form.text("your review prediction : "+str(result[0]))
    # form.metric(label="The given Review is...",value="Positive", delta="+ve")
    col1, col2= form.columns(2)
    # form.text("your review prediction : ")
    col1.markdown("your review prediction : ")
    col1.dataframe(pd.DataFrame.from_dict(res,orient='index',columns=['Model Prediction Count']))
    if res['Negative']>res['Positive']:
        col1.markdown("Overall Sentiment : **:red[Negative]**")
    elif res['Negative'] < res['Positive']:
        col1.markdown("Overall Sentiment  : **:green[Positive]**")
    else: 
        col1.markdown("Overall Sentiment :  **[Neutral]** ")
    # c"This text is :red[colored red], and this is **:blue[colored]** and bold.")("Overall Sentiment : "+overall_sentiment)
    
    col2.metric(label="The given Review is...",value=str(round((res['Positive'])*100,2))+"% "+"Positive", delta="+ve")
    col2.metric(label="The given Review is...",value=str(round((res['Negative'])*100,2))+"% "+"Negative", delta="-ve")
    

    #save model prdiction to excel file for later analysis
    save_review_to_excel(reviews,result)
    #feedback button
    # st.success("We appreciate your feedback!!       Do you really,satisfy with the result?")
    # col1, col2, col3= st.columns(3)
    # if col1.button("😊 Yes I'm "):
    #     # alert()
    #     st.write("Agree")
    #     print("Agreeeeee")
        
    # if col2.button("😥 No I'm Not"):
    #     st.write("Disagree")
    # if col3.button("😐 Not Sure!!"):
    #     st.write("not sure")

    print("---------------------submit ---------------------")

    

elif uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    # st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    # user_input = form.text_area(string_data)
    data = string_data.split('------------------------')
    print(data)
    
    data=preprocess_text(data)
    st.write(data)
    #test whole model
    loaded_pipe = load_data()
    results = loaded_pipe.predict(data)
    print("data whole tested ",results)




    res ={'Negative':0,'Positive':0}
    result=[]
    for result in results:
        if result==0: res['Negative']+=1 
        else: res['Positive']+=1
    col1, col2= form.columns(2)
    # form.text("your review prediction : ")
    col1.markdown("your review prediction : ")
    col1.dataframe(pd.DataFrame.from_dict(res,orient='index',columns=['Model Prediction Count']))
    if res['Negative']>res['Positive']:
        col1.markdown("Overall Sentiment : **:red[Negative]**")
    elif res['Negative'] < res['Positive']:
        col1.markdown("Overall Sentiment  : **:green[Positive]**")
    else: 
        col1.markdown("Overall Sentiment : Neutral ")
    col2.metric(label="The given Review is...",value=str(round((res['Positive']/len(data))*100,2))+"% "+"Positive", delta="+ve")
    col2.metric(label="The given Review is...",value=str(round((res['Negative']/len(data))*100,2))+"% "+"Negative", delta="-ve")

    #save model prdiction to excel file for later analysis
    save_review_to_excel(data,results)
    
    #feedback button
    # st.success("We appreciate your feedback!!       Do you really,satisfy with the result?")
    # col1, col2, col3= st.columns(3)
    # if col1.button("😊 Yes I'm "):
    #     col1.write("Agree")
    # if col2.button("😥 No I'm Not"):
    #     st.write("Disagree")
    # if col3.button("😐 Not Sure!!"):
    #     st.write("not sure")
    # print("--------------------file upload ----------------------")
    # st.write(data)

else:
    form.text('Enter Some Text First Please!!!')
    

