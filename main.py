import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from time import sleep
from utils import make_certificates

datas = pd.read_csv('kurs2.csv')

st.set_page_config('Sertifikatlar sahifasi','📔','centered','collapsed')

st.write("""
# 1-oraliq nazorat ballari
O'zbekiston Milliy universitetining Jizzax filiali Kompyuter ilmlari va dasturlash texnologiyalari yo'nalishi 171-23 va 172-23 guruh talabalarining oraliq nazorat baholarini chop etishning
""")
st.markdown("## :rainbow[SERTIFIKATLAR BO'LIMI]")


st.logo('jbnuu_logo.png')

tab1,tab2 = st.tabs(["Ma'lumotlar bo'limi", "Statistika bo'limi"])

fio = datas['FIO']
group = datas['Guruh']

with tab1:
    selected_fio = datas[datas['FIO']==st.selectbox("O'z FIO ingizni tanlang", fio)]
    st.dataframe(selected_fio)
    
    savol_ustunlari = ['Savol1', 'Savol2', 'Savol3', 'Savol4', 'Savol5']
    umumiy_ball = selected_fio[savol_ustunlari].sum(axis=1).iloc[0]
    st.write("Sizning umumiy ballingiz:",int(umumiy_ball))
    
    sertifikat_tayyorlash = st.button("Sertifikat tayyorlash",type='primary')
    if sertifikat_tayyorlash:
        with st.spinner("Ma'lumotlaringiz qabul qilindi. Iltimos ozgina vaqt kutib turing"):
            # Sertifikat rasmini yaratish
            sertifikat_bytes = make_certificates(str(selected_fio['FIO'].iloc[0]), str(int(100*umumiy_ball/5))+'%')
            
            # Rasmni ko'rsatish
            st.image(sertifikat_bytes)
            
            # Yuklab olish tugmasini ko'rsatish
            st.download_button(
                label="Sertifikatni yuklab olish",
                data=sertifikat_bytes,
                file_name=f"sertifikat_{selected_fio['FIO'].iloc[0]}.png",
                mime="image/png",
                type='primary'
            )
           
with tab2:
   st.header("Guruhlar bo'yicha statistika")
   
   # Har bir talabaning umumiy ballini hisoblash
   datas['Umumiy_ball'] = datas[savol_ustunlari].sum(axis=1)
   
   # Guruhlar bo'yicha o'rtacha ballni hisoblash
   guruh_statistika = datas.groupby('Guruh')['Umumiy_ball'].agg(['mean', 'count']).reset_index()
   guruh_statistika.columns = ['Guruh', "O'rtacha ball", 'Talabalar soni']
   
   # Ustunli diagramma yaratish
   plt.figure(figsize=(10, 6))
   sns.barplot(data=guruh_statistika, x='Guruh', y="O'rtacha ball")
   plt.title("Guruhlar bo'yicha o'rtacha ballar")
   
   # Diagrammani ko'rsatish
   st.pyplot(plt)
   
   # Statistik ma'lumotlarni jadval ko'rinishida ko'rsatish
   st.write("Guruhlar bo'yicha batafsil ma'lumot:")
   st.dataframe(guruh_statistika)
   
   # Har bir savol bo'yicha statistika
   st.header("Savollar bo'yicha statistika")
   
   # Har bir savol uchun alohida pie chart
   for savol in savol_ustunlari:
       plt.figure(figsize=(8, 8))
       savol_statistika = datas[savol].value_counts()
       plt.pie(savol_statistika.values, labels=savol_statistika.index, 
               autopct='%1.1f%%', startangle=90)
       plt.title(f"{savol} bo'yicha statistika")
       st.pyplot(plt)
       
       # Savol bo'yicha o'rtacha ball
       st.write(f"{savol} bo'yicha o'rtacha ball: {datas[savol].mean():.2f}")
       st.write(f"{savol} bo'yicha maksimal ball: {datas[savol].max()}")
       st.write(f"{savol} bo'yicha minimal ball: {datas[savol].min()}")
       st.write("---")
