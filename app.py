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

# st.write(st.session_state.videos_data)
# st.write('dummy')

# Navigation
page = st.sidebar.radio("Navigation", ["Home", "Video Library", "Curriculum"], key='pages_radio')

# Sidebar with channel info
with st.sidebar:
    st.title("Apostle Arome Osayi Sermons")
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
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(latest_video['thumbnail'])

    with col2:
        st.subheader(latest_video['title'])
        st.caption(f"Published: {latest_video['publish_date']} • {latest_video['duration_minutes']} minutes")
        st.write(latest_video['description'])
        st.write(f"**Topics:** {latest_video['topics']}")
        st.button("▶️ Watch Now", key="watch_latest")


    # Extract all unique topics
    all_topics = []
    for topics in st.session_state['videos_data']['topics_list']:
        all_topics.extend(topics)
    unique_topics = sorted(list(set(all_topics)))

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


    # Replace the "Explore by Topic" section with "Popular Topics" using pills
    st.header("Popular Topics")

    # Extract all unique topics
    all_topics = []
    for topics in st.session_state['videos_data']['topics_list']:
        all_topics.extend(topics)

    # Count occurrences of each topic
    topic_counts = {}
    for topic in all_topics:
        if topic in topic_counts:
            topic_counts[topic] += 1
        else:
            topic_counts[topic] = 1

    # Sort topics by popularity (count)
    sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
    popular_topics = [topic for topic, count in sorted_topics[:8]]  # Get top 8 most popular topics

    # Use pills for topic selection
    selected_topic = st.pills(
        label="Select a topic to explore",
        options=[topic.capitalize() for topic in popular_topics],
        label_visibility="collapsed"
    )

    # Display videos for selected topic if a pill is selected
    if selected_topic:
        selected_topic_lower = selected_topic.lower()
        st.subheader(f"{selected_topic} Sermons")

        # Filter videos by the selected topic
        topic_videos = st.session_state['videos_data'][
            st.session_state['videos_data']['topics_list'].apply(lambda x: selected_topic_lower in x)
        ].head(3)  # Show top 3 videos for this topic

        for i, (_, video) in enumerate(topic_videos.iterrows()):
            col1, col2 = st.columns([1, 3])

            with col1:
                st.image(video['thumbnail'], width=150)

            with col2:
                st.subheader(video['title'])
                st.caption(f"Published: {video['publish_date']} • {video['duration_minutes']} minutes")
                st.write(
                    video['description'][:100] + "..." if len(video['description']) > 100 else video['description'])
                st.button("▶️ Watch", key=f"topic_video_{i}")

        # Add a "See all" button to go to the Video Library with this topic selected
        if st.button(f"See all {selected_topic} sermons"):
            st.session_state['selected_topic'] = selected_topic_lower
            st.session_state['page'] = "Video Library"
            st.rerun()

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
    Our sermon curriculum organizes messages by topic and year.
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

    # Create expanders for each topic
    for topic in all_topics:
        with st.expander(f"📚 {topic.capitalize()}", expanded=False):
            # Get years for this topic
            topic_data = exploded_df[exploded_df['topics_list'] == topic]
            years = sorted(topic_data['year'].unique(), reverse=True)

            # Create nested expanders for each year
            for year in years:
                with st.expander(f"📅 {year}", expanded=False):
                    # Get videos for this topic and year
                    videos = topic_data[topic_data['year'] == year]

                    for _, video in videos.iterrows():
                        col1, col2, col3 = st.columns([1, 3, 1])

                        with col1:
                            st.image(video['thumbnail'], width=100)

                        with col2:
                            st.write(f"**{video['title']}**")
                            st.caption(f"{video['publish_date']} • {video['duration_minutes']} minutes")
                            st.write(video['description'][:150] + "..." if len(video['description']) > 150 else video[
                                'description'])

                        with col3:
                            st.button("▶️ Watch", key=f"curriculum_{video['video_id']}_{year}_{topic}")
                            # st.download_button("📥 Download",
                            #                    data=b"Dummy sermon notes",
                            #                    file_name=f"{video['title']}_notes.pdf",
                            #                    mime="application/pdf",
                            #                    key=f"download_{video['video_id']}_{year}_{topic}")

                    # Add a note about the number of sermons
                    st.info(f"{len(videos)} sermons on {topic} from {year}")

            # Add a summary for this topic
            total_topic_sermons = len(topic_data)
            years_covered = ", ".join(years)
            st.write(f"**Summary:** {total_topic_sermons} sermons on {topic} from {years_covered}")
    st.divider()
    # Add download button for the curriculum
    st.download_button(
        label="📥 Download Complete Curriculum (PDF)",
        data=b"Dummy PDF content",
        file_name="sermon_curriculum.pdf",
        mime="application/pdf"
    )

    # st.divider()
    # # Add download button for the curriculum
    # st.download_button(
    #     label="Download Curriculum (PDF)",
    #     data=b"Dummy PDF content",
    #     file_name="sermon_curriculum.pdf",
    #     mime="application/pdf"
    # )