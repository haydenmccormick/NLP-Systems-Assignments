from collections import Counter
from operator import itemgetter

import streamlit as st
import pandas as pd
import altair as alt
import graphviz

import ner


example = (
        "When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")


# st.set_page_config(layout='wide')
st.markdown('## spaCy Named Entity Recognition')

text = st.text_area('Text to process', value=example, height=100)

doc = ner.SpacyDocument(text)

# Settings
with st.sidebar:
    st.markdown('## Settings')
    screen_choice = st.radio('Select view', ['entities', 'dependencies'])

def show_entities():
    entities = doc.get_entities()
    tokens = doc.get_tokens()
    counter = Counter(tokens)
    words = list(sorted(counter.most_common(30)))

    # https://pandas.pydata.org
    chart = pd.DataFrame({
        'frequency': [w[1] for w in words],
        'word': [w[0] for w in words]})

    # https://pypi.org/project/altair/
    bar_chart = alt.Chart(chart).mark_bar().encode(x='word', y='frequency')

    st.markdown(f'Total number of tokens: {len(tokens)}<br/>'
                f'Total number of types: {len(counter)}', unsafe_allow_html=True)

    # https://docs.streamlit.io/library/api-reference/data/st.table
    st.table(entities)

    # https://docs.streamlit.io/library/api-reference/charts/st.altair_chart
    st.altair_chart(bar_chart)

def show_dependencies():
    table_tab, graph_tab = st.tabs(['table', 'graph'])
    # Table tab
    deps = doc.get_dependencies()
    deps_df = pd.DataFrame(deps, columns=['head', 'relation', 'child'])
    table_tab.write(deps_df)
    # Graph tab
    graph = graphviz.Digraph()
    for head, relation, child in deps:
        graph.edge(head, child, label=relation)
    graph_tab.graphviz_chart(graph)


if screen_choice == "entities":
    show_entities()
else: 
    show_dependencies()