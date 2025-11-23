import streamlit as st
from backend import process_video

st.title("Communication Insights Generator")

url = st.text_input("Enter a public video URL (YouTube, Loom, MP4, etc.)")

if st.button("Analyze Video"):
    if not url.strip():
        st.error("Please enter a valid video URL.")
    else:
        with st.spinner("Processing video..."):
            try:
                result = process_video(url)

                st.success("Analysis Completed!")

                st.metric("Clarity Score", f"{result['clarity']}%")
                st.write("### 🎯 Communication Focus")
                st.info(result['focus'])

                with st.expander("📝 Transcript"):
                    st.write(result['transcript'])

            except Exception as e:
                st.error(f"Error: {e}")
