import streamlit as st
from utils.analysis import analyze_midi,display_feedback

st.title("🎹 AI Piano Analyzer")
uploaded_file = st.file_uploader("📁Upload the file in .mid or .midi format",type = [".mid" , ".midi"])
if uploaded_file:
    with open ("temp.mid","wb") as f:
        f.write(uploaded_file.read())

    st.success("✅MIDI file uploaded succesfully")
    result = analyze_midi("temp.mid")
    display_feedback(result)

