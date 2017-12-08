from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def suggest_tags(file_contents):
    document = [file_contents]
    number_features = 1000
    tf_vectorizer = CountVectorizer(max_features=number_features, stop_words='english')
    tf = tf_vectorizer.fit_transform(document)
    tf_feature_names = tf_vectorizer.get_feature_names()

    number_topics = 1
    lda = LatentDirichletAllocation(n_components=number_topics, max_iter=1, learning_method='online', learning_offset=50.,random_state=0).fit(tf)

    number_top_words = 5
    for topic_idx, topic in enumerate(lda.components_):
        return [tf_feature_names[i] for i in topic.argsort()[:-number_top_words - 1:-1]]