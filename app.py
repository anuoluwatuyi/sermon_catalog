import streamlit as st
import pandas as pd
import datetime
import random

# Page configuration
st.set_page_config(
    page_title="Sermon Library",
    page_icon="🙏",
    layout="wide"
)


# Create dummy data for demonstration
def create_dummy_videos(num_videos=20):
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
        "The Promise of Salvation",
        "Overcoming Fear",
        "The Kingdom of God",
        "Worship as a Lifestyle",
        "God's Faithfulness",
        "The Fruit of the Spirit",
        "Spiritual Disciplines",
        "Understanding Scripture",
        "Serving Others",
        "Marriage and Family",
        "Stewardship and Generosity"
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
        "Understanding the gift of salvation and its implications.",
        "Breaking free from fear and anxiety through faith.",
        "Understanding the principles of God's kingdom.",
        "How worship extends beyond Sunday services.",
        "Stories and lessons about God's faithfulness.",
        "Developing the fruit of the Spirit in everyday life.",
        "Practices that deepen your relationship with God.",
        "How to read and apply Scripture effectively.",
        "The importance of serving others in the Christian life.",
        "Biblical principles for healthy family relationships.",
        "Managing resources according to biblical principles."
    ]

    # Generate random dates within the last 3 years, sorted from newest to oldest
    current_date = datetime.datetime.now()
    dates = []
    for i in range(num_videos):
        days_back = i * 30 + random.randint(0, 15)  # Roughly monthly sermons with some variation
        random_date = current_date - datetime.timedelta(days=days_back)
        dates.append(random_date.strftime("%Y-%m-%d"))

    # Define topics
    all_topics = ["faith", "prayer", "salvation", "love", "forgiveness", "hope",
                  "worship", "family", "service", "scripture", "stewardship"]

    # Assign topics to each video
    topics_list = []
    topics_detailed = []
    for _ in range(num_videos):
        num_topics = random.randint(1, 3)
        topics = random.sample(all_topics, num_topics)
        topics_list.append(", ".join(topics))
        topics_detailed.append(topics)

    # Create thumbnails (just URLs for dummy data)
    thumbnails = [f"https://img.youtube.com/vi/dummy{i}/0.jpg" for i in range(1, num_videos + 1)]

    # Create view counts
    views = [random.randint(100, 5000) for _ in range(num_videos)]

    # Duration in minutes
    durations = [random.randint(20, 60) for _ in range(num_videos)]

    return pd.DataFrame({
        'video_id': video_ids,
        'title': titles[:num_videos],
        'description': descriptions[:num_videos],
        'publish_date': dates,
        'topics': topics_list,
        'topics_list': topics_detailed,
        'thumbnail': thumbnails,
        'views': views,
        'duration_minutes': durations
    })


# Create dummy data if not already in session state
if 'videos_data' not in st.session_state:
    st.session_state['videos_data'] = create_dummy_videos()

# Navigation
page = st.sidebar.radio("Navigation", ["Home", "Video Library", "Curriculum"])

# Sidebar with channel info
with st.sidebar:
    st.title("Pastor Smith's Sermons")
    st.write("Welcome to our sermon library where you can explore teachings on various topics.")

    st.divider()

    st.metric("Total Sermons", len(st.session_state['videos_data']))

    # Latest video update
    latest_date = max(st.session_state['videos_data']['publish_date'])
    st.write(f"Latest sermon: {latest_date}")

    st.divider()
    st.write("© 2025 Our Church")

# Home Page
if page == "Home":
    st.title("Welcome to Our Sermon Library")

    # Featured/Latest sermon
    latest_video = st.session_state['videos_data'].iloc[0]

    st.header("Latest Sermon")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(latest_video['thumbnail'])

    with col2:
        st.subheader(latest_video['title'])
        st.caption(f"Published: {latest_video['publish_date']} • {latest_video['duration_minutes']} minutes")
        st.write(latest_video['description'])
        st.write(f"**Topics:** {latest_video['topics']}")
        st.button("▶️ Watch Now", key="watch_latest")

    # Topic exploration section
    st.header("Explore by Topic")

    # Extract all unique topics
    all_topics = []
    for topics in st.session_state['videos_data']['topics_list']:
        all_topics.extend(topics)
    unique_topics = sorted(list(set(all_topics)))

    # Create topic buttons in rows of 4
    cols = st.columns(4)
    for i, topic in enumerate(unique_topics):
        col_idx = i % 4
        with cols[col_idx]:
            if st.button(f"📚 {topic.capitalize()}", key=f"topic_{topic}"):
                st.session_state['selected_topic'] = topic
                st.session_state['page'] = "Video Library"
                st.experimental_rerun()

    # Popular sermons section
    st.header("Popular Sermons")
    popular_videos = st.session_state['videos_data'].sort_values('views', ascending=False).head(3)

    for i, (_, video) in enumerate(popular_videos.iterrows()):
        col1, col2 = st.columns([1, 3])

        with col1:
            st.image(video['thumbnail'])

        with col2:
            st.subheader(video['title'])
            st.caption(f"Published: {video['publish_date']} • {video['views']} views")
            st.write(video['description'][:100] + "..." if len(video['description']) > 100 else video['description'])
            st.write(f"**Topics:** {video['topics']}")
            st.button("Watch", key=f"watch_popular_{i}")

    # Recent sermon series
    st.header("Recent Series")
    st.info("Coming soon: Organized sermon series")

# Video Library Page
elif page == "Video Library":
    st.title("Video Library")

    # Filter options
    col1, col2 = st.columns(2)

    with col1:
        # Check if there's a selected topic from the home page
        default_topic = st.session_state.get('selected_topic', "All")

        # Extract all unique topics
        all_topics = []
        for topics in st.session_state['videos_data']['topics_list']:
            all_topics.extend(topics)
        unique_topics = sorted(list(set(all_topics)))

        # Add "All" option
        filter_options = ["All"] + unique_topics
        selected_topic = st.selectbox("Filter by Topic",
                                      options=filter_options,
                                      index=filter_options.index(
                                          default_topic) if default_topic in filter_options else 0)

    with col2:
        sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Most Viewed", "Title A-Z"])

    # Apply filters and sorting
    filtered_data = st.session_state['videos_data'].copy()

    if selected_topic != "All":
        filtered_data = filtered_data[filtered_data['topics_list'].apply(lambda x: selected_topic in x)]

    if sort_by == "Newest First":
        filtered_data = filtered_data.sort_values('publish_date', ascending=False)
    elif sort_by == "Oldest First":
        filtered_data = filtered_data.sort_values('publish_date', ascending=True)
    elif sort_by == "Most Viewed":
        filtered_data = filtered_data.sort_values('views', ascending=False)
    elif sort_by == "Title A-Z":
        filtered_data = filtered_data.sort_values('title')

    # Display filter results
    st.write(f"Found {len(filtered_data)} sermons")

    # Display videos in a grid
    for i in range(0, len(filtered_data), 2):
        cols = st.columns(2)

        for j in range(2):
            if i + j < len(filtered_data):
                video = filtered_data.iloc[i + j]
                with cols[j]:
                    st.image(video['thumbnail'], width=250)
                    st.subheader(video['title'])
                    st.caption(f"Published: {video['publish_date']} • {video['duration_minutes']} minutes")
                    st.write(
                        video['description'][:150] + "..." if len(video['description']) > 150 else video['description'])
                    st.write(f"**Topics:** {video['topics']}")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.button("Watch", key=f"watch_{i}_{j}")
                    with col2:
                        st.button("Save", key=f"save_{i}_{j}")

                    st.divider()

# Curriculum Page
elif page == "Curriculum":
    st.title("Sermon Curriculum")

    st.write("""
    Our sermon curriculum organizes messages by topic and year, 
    providing a structured way to grow in your faith journey.
    """)

    # Create curriculum from the data
    videos_df = st.session_state['videos_data'].copy()

    # Extract year from publish_date
    videos_df['year'] = videos_df['publish_date'].apply(lambda x: x.split('-')[0])

    # Explode the topics_list to have one row per video-topic pair
    exploded_df = videos_df.explode('topics_list')

    # Group by topic and year
    grouped = exploded_df.groupby(['topics_list', 'year'])

    # For each topic-year group, create a section
    all_topics = sorted(exploded_df['topics_list'].unique())

    for topic in all_topics:
        st.header(f"{topic.capitalize()}")

        # Get years for this topic
        topic_data = exploded_df[exploded_df['topics_list'] == topic]
        years = sorted(topic_data['year'].unique(), reverse=True)

        for year in years:
            st.subheader(f"{year}")

            # Get videos for this topic and year
            videos = topic_data[topic_data['year'] == year]

            for _, video in videos.iterrows():
                col1, col2 = st.columns([1, 4])

                with col1:
                    st.image(video['thumbnail'], width=100)

                with col2:
                    st.write(f"**{video['title']}**")
                    st.caption(f"{video['publish_date']} • {video['duration_minutes']} minutes")
                    st.button("Watch", key=f"curriculum_{video['video_id']}")

            st.divider()

        st.divider()

    # Add download button for the curriculum
    st.download_button(
        label="Download Curriculum (PDF)",
        data=b"Dummy PDF content",
        file_name="sermon_curriculum.pdf",
        mime="application/pdf"
    )