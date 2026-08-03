from .embedding import model
from .vectorstore import collection

def retrieve(question):

    vector = model.encode(question).tolist()

    result = collection.query(

        query_embeddings=[vector],

        n_results=4
    )

    return result