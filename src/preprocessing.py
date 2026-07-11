import ast

def convert(text):
    return [i['name'] for i in ast.literal_eval(text)]

def get_top_cast(text):
    return [i['name'] for i in ast.literal_eval(text)[:5]]

def get_director(text):
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            return i['name']
    return ""

def create_tags(df):
    df['overview'] = df['overview'].apply(lambda x: x.split())
    df['genres'] = df['genres'].apply(convert)
    df['keywords'] = df['keywords'].apply(convert)
    df['cast'] = df['cast'].apply(get_top_cast)
    df['crew'] = df['crew'].apply(get_director)

    df['tags'] = (
    df['overview']
    + df['genres']
    + df['keywords']
    + df['cast']
    + df['cast']
    + df['cast']
    + df['crew'].apply(lambda x: [x])
    + df['crew'].apply(lambda x: [x])
    + df['crew'].apply(lambda x: [x])
)

    df['tags'] = df['tags'].apply(lambda x: " ".join(x).lower())
    return df[['id', 'title', 'tags']]
