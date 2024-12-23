import streamlit as st
from embeddings import get_sorted_similarities


with st.sidebar:
    st.title('로그인')

    input_first_jogak = st.text_input('☺️ 나의 첫 조각 입력!') 
    st.caption('첫 조각을 입력해서 나와 비슷한 시작을 하고 있는 사람들을 둘러봐요!') 
    signup_btn = st.button("시작!") 
    if signup_btn:
        st.success(f'[{input_first_jogak}]와 시작이 유사했던 유저들을 확인해보세요!')


st.title('조각 커뮤니티🍊')
st.write('나와 비슷한 꿈을 갖고 있는 사람들의 첫 시작을 통해 동기부여를 받아요.')
st.write('')
st.write('모두의 시작은 작았습니다. 작게작게 버겁지 않게 시작해보세요!')


st.write("<br><br>", unsafe_allow_html=True) #빈칸 여백


def recordContainer(jogak, slices:list):
    with st.container(height=300, border=True):
        col1, col2 = st.columns([1,2])
        with col1:
            st.write()
            st.subheader(jogak)
            st.write(':orange[첫 조각이 위와 같았던 유저:]')

        with col2:
            st.write()
            st.write(':blue[이렇게 작게 시작해 목표를 꾸준히 이루어내고 있습니다!]')
            with st.container(height=200, border=True):
                i=1
                for slice in slices:
                    st.write(f'{i}번째 한입 : {slice}')
                    i += 1

sorted_jogak_dict = get_sorted_similarities(input_first_jogak)

if input_first_jogak:
    for jogak, slices in sorted_jogak_dict.items():
        recordContainer(jogak, slices=slices)