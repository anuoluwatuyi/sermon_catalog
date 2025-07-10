import streamlit as st
import pandas as pd
import datetime
import random

# Page configuration
st.set_page_config(
    page_title="Sermon Analyzer",
    page_icon="🙏",
    layout="wide"
)

# App title and description
st.title("Sermon Analyzer")
st.markdown("""
This app helps analyze sermon videos from a YouTube channel. 
- Extract and analyze sermon content
- Classify sermons by topics
- Generate sermon curriculum
""")

# Sidebar for configuration
with st.sidebar:
    st.title("Configuration")
    api_key = st.text_input("YouTube API Key", placeholder="Enter your API key", type="password",
                            value="dummy-api-key-for-testing")
    channel_id = st.text_input("YouTube Channel ID", placeholder="Enter channel ID",
                               value="UC123456789")

    st.subheader("Topic Settings")
    default_topics = ["faith", "prayer", "salvation", "love", "forgiveness", "hope"]
    topics_text = st.text_area("Topics (one per line)", "\n".join(default_topics))


# Create dummy data
def create_dummy_videos(num_videos=10):
    video_ids = [f"vid{i}" for i in range(1, num_videos + 1)]
    titles = [
        "Finding Faith in Difficult Times",
        "The Power of Prayer",
        "Understanding God's Love",
        "Forgiveness: The Path to Freedom",
        "Hope in the Midst of Trials",
        "Living a Life of Purpose",
        "The Grace of God",
        "Finding Strength in Weakness",
        "Walking in Obedience",
        "The Promise of Salvation"
    ]

    descriptions = [
        "This sermon explores how to maintain faith during challenging seasons of life.",
        "Discover the transformative power of prayer in your daily walk with God.",
        "An exploration of God's unconditional love and how it changes us.",
        "Learn why forgiveness is essential for spiritual and emotional health.",
        "Finding hope when circumstances seem hopeless.",
        "How to discover and live out God's purpose for your life.",
        "Understanding the depth and breadth of God's grace.",
        "Why our weaknesses are opportunities for God's strength to be displayed.",
        "The importance of obedience in the Christian life.",
        "Understanding the gift of salvation and its implications."
    ]

    # Generate random dates within the last 3 years
    current_date = datetime.datetime.now()
    dates = []
    for _ in range(num_videos):
        days_back = random.randint(1, 1095)  # Up to 3 years
        random_date = current_date - datetime.timedelta(days=days_back)
        dates.append(random_date.strftime("%Y-%m-%d"))

    # Assign random topics to each video
    topics_list = []
    for _ in range(num_videos):
        num_topics = random.randint(1, 3)
        topics = random.sample(default_topics, num_topics)
        topics_list.append(", ".join(topics))

    # Create thumbnails (just URLs for dummy data)
    thumbnails = [f"https://img.youtube.com/vi/dummy{i}/0.jpg" for i in range(1, num_videos + 1)]

    return pd.DataFrame({
        'video_id': video_ids,
        'title': titles[:num_videos],
        'description': descriptions[:num_videos],
        'publish_date': dates,
        'topics': topics_list,
        'thumbnail': thumbnails
    })


# Create dummy data
dummy_videos = create_dummy_videos()

# Main app tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Fetch Videos", "Analyze Videos", "View Database", "Generate Curriculum"
])

# Fetch Videos Tab
with tab1:
    st.header("Fetch Videos from YouTube")

    st.info("This is a demo version with dummy data. API functionality will be implemented later.")

    if st.button("Fetch Demo Videos"):
        st.session_state['fetched_videos'] = dummy_videos
        st.success(f"Successfully fetched {len(dummy_videos)} demo videos!")

        # Display fetched videos
        for _, video in dummy_videos.iterrows():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(video["thumbnail"], width=120)
                st.markdown(f"[Watch Video](https://www.youtube.com/watch?v={video['video_id']})")
            with col2:
                st.subheader(video["title"])
                st.caption(f"Published: {video['publish_date']}")
                st.write(video["description"])

# Analyze Videos Tab
with tab2:
    st.header("Analyze Videos")

    if 'fetched_videos' not in st.session_state:
        st.info("Please fetch videos from the 'Fetch Videos' tab first.")
    else:
        video_titles = st.session_state['fetched_videos']['title'].tolist()
        selected_title = st.selectbox("Select a video to analyze", video_titles)

        selected_video = \
        st.session_state['fetched_videos'][st.session_state['fetched_videos']['title'] == selected_title].iloc[0]

        st.subheader(selected_title)
        st.write(f"**Published:** {selected_video['publish_date']}")

        # Create dummy placeholder for video
        st.image(selected_video['thumbnail'], width=400)
        st.caption("Dummy video placeholder - actual video player will be implemented later")

        if st.button("Process Video"):
            st.success("Video processed successfully!")

            # Dummy subtitle text
            subtitle_text = "This is a sample transcript. It contains words like faith, prayer, and love. The sermon talks about the importance of salvation and how forgiveness leads to spiritual growth. We should always have hope in difficult times."

            # Extract topics from the dummy subtitle
            topics = [topic for topic in default_topics if topic in subtitle_text]

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Detected Topics")
                for topic in topics:
                    st.write(f"- {topic}")

            with col2:
                # Let user edit topics
                st.subheader("Edit Topics")
                edited_topics_text = st.text_area("Edit topics (one per line)", "\n".join(topics))

# View Database Tab
with tab3:
    st.header("View Database")

    st.info("This is a demo version. Database functionality will be implemented later.")

    # Use the dummy data for database view as well
    if 'fetched_videos' in st.session_state:
        # Display statistics
        total_videos = len(st.session_state['fetched_videos'])
        st.metric("Total Videos", total_videos)

        # Show data table
        st.subheader("Stored Videos")
        st.dataframe(st.session_state['fetched_videos'][['video_id', 'title', 'publish_date', 'topics']])

        # Show video details on select
        video_ids = st.session_state['fetched_videos']['video_id'].tolist()
        titles = st.session_state['fetched_videos']['title'].tolist()
        video_options = {vid: title for vid, title in zip(video_ids, titles)}

        selected_video_id = st.selectbox("Select a video to view details",
                                         options=video_ids,
                                         format_func=lambda x: video_options[x])

        if selected_video_id:
            video_data = st.session_state['fetched_videos'][
                st.session_state['fetched_videos']['video_id'] == selected_video_id].iloc[0]

            st.subheader(video_data['title'])
            st.write(f"**Published:** {video_data['publish_date']}")
            st.write(f"**Topics:** {video_data['topics']}")

            with st.expander("Description"):
                st.write(video_data['description'])

            with st.expander("Subtitle Text (Dummy)"):
                st.write(
                    "This is a placeholder for the video's transcript. In the actual app, this would contain the full transcript of the sermon.")

            st.image(video_data['thumbnail'], width=400)
    else:
        st.info("No videos in the database yet. Process some videos first.")

# Generate Curriculum Tab
with tab4:
    st.header("Generate Sermon Curriculum")

    if st.button("Generate Curriculum"):
        # Create a dummy curriculum
        curriculum = """
# Sermon Curriculum

## Faith (2024)
- [Finding Faith in Difficult Times](https://www.youtube.com/watch?v=vid1)
- [Walking in Obedience](https://www.youtube.com/watch?v=vid9)

## Prayer (2024)
- [The Power of Prayer](https://www.youtube.com/watch?v=vid2)
- [Finding Strength in Weakness](https://www.youtube.com/watch?v=vid8)

## Love (2023)
- [Understanding God's Love](https://www.youtube.com/watch?v=vid3)
- [The Grace of God](https://www.youtube.com/watch?v=vid7)

## Forgiveness (2023)
- [Forgiveness: The Path to Freedom](https://www.youtube.com/watch?v=vid4)

## Hope (2022)
- [Hope in the Midst of Trials](https://www.youtube.com/watch?v=vid5)
- [Living a Life of Purpose](https://www.youtube.com/watch?v=vid6)

## Salvation (2022)
- [The Promise of Salvation](https://www.youtube.com/watch?v=vid10)
"""
        st.session_state['curriculum'] = curriculum

    if 'curriculum' in st.session_state:
        st.markdown(st.session_state['curriculum'])

        # Download option
        st.download_button(
            label="Download Curriculum",
            data=st.session_state['curriculum'],
            file_name="sermon_curriculum.md",
            mime="text/markdown"
        )