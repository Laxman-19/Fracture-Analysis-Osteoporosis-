import streamlit as st
import pandas as pd
import base64
import joblib
import pickle

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('img.jpg')





st.header('Osteoporotic Fracture Analysis')
st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

Age = st.number_input('Enter your age')
Gender = st.selectbox('Select Gender', ('Male' , 'Female'))
ASSO_MEDICAL_PROB = st.selectbox('Select ASSO MEDICAL PROB', ('no' , 'yes(diabetes)' , 'yes(diabetes,bp)' , 'yes(bp)' , 'yes (diabetes,heart blockage)' , 'kidney stone' , 'yes(increase in heart rate)' , 'yes(diabetes,kidney stone)' ))
HO_INJURYSURGERY = st.selectbox('Select H/O INJURY/SURGERY', ('no','vericose vein surgery' , 'uteres removal' , 'kidney stone opreration' , 'uterus surgery' , 'yes(diverticulities)' , 'shouler surgery' , 'knee surgery' , 'yes(open heart surgery)' ))
DRUG_HISTORY = st.selectbox('Select DRUG HISTORY', ('no' , 'yes' , 'yes(ecosprin)' ))


model = pickle.load(open('Fracture_Detection.pkl','rb'))

st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
prediction = None

with col2:
    if st.button('Submit'):
        
        
        x = pd.DataFrame([[Age,Gender,ASSO_MEDICAL_PROB,HO_INJURYSURGERY,DRUG_HISTORY]], 
                        columns = [ 'AGE' , 'SEX' , 'ASSO MEDICAL PROB' , 'H/O INJURY/SURGERY' , 'DRUG HISTORY'])

        x = x.replace( ['Male' , 'Female'] , [1,0] )
        x = x.replace( ['no' , 'yes(diabetes)' , 'yes(diabetes,bp)' , 'yes(bp)' , 'yes (diabetes,heart blockage)' , 'kidney stone' , 'yes(increase in heart rate)' , 'yes(diabetes,kidney stone)'] , [0,1,2,3,4,5,6,7] )
        x = x.replace( ['no','vericose vein surgery' , 'uteres removal' , 'kidney stone opreration' , 'uterus surgery' , 'yes(diverticulities)' , 'shouler surgery' , 'knee surgery' , 'yes(open heart surgery)'] , [0,1,2,3,4,5,6,7,8] )
        x = x.replace( ['no' , 'yes' , 'yes(ecosprin)'] , [0,1,2] )

        prediction = model.predict(x)[0]

if prediction is not None:
    st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)
    st.subheader("🩺 Prediction Result")
    st.title(f"This person may have: **{prediction}**")

st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)
