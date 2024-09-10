import streamlit as st
from news_scraper import scrape_all_sources

st.title('Personalized News Aggregator')

# Search bar for keywords
search_query = st.text_input('Search for news by keyword:', '')

# Displaying the news articles
articles = scrape_all_sources()
filtered_articles = [article for article in articles if any(search_query.lower() in keyword.lower() for keyword in article['keywords'])]

st.subheader('Trending Topics/Headlines:')
for article in filtered_articles[:10]:  # Displaying top 10 articles
    st.write(f"**{article['title']}**")
    st.write(f"[Read more]({article['link']})")
    st.write(f"Keywords: {', '.join(article['keywords'])}")
    st.write('---')

if search_query:
    st.subheader(f'Results for "{search_query}":')
    for article in filtered_articles:
        st.write(f"**{article['title']}**")
        st.write(f"[Read more]({article['link']})")
        st.write(f"Keywords: {', '.join(article['keywords'])}")
        st.write('---')
else:
    st.subheader('All News:')
    for article in articles:
        st.write(f"**{article['title']}**")
        st.write(f"[Read more]({article['link']})")
        st.write(f"Keywords: {', '.join(article['keywords'])}")
        st.write('---')

