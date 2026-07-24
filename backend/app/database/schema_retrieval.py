from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

TABLE_DOCS = [
    Document(
        page_content=(
            "Table: customers. Columns: customer_id (PK), name, region "
            "(North/South/East/West), signup_date. Use for questions about "
            "who customers are or which region they belong to."
        ),
        metadata={"table": "customers"},
    ),
    Document(
        page_content=(
            "Table: products. Columns: product_id (PK), name, category "
            "(Electronics/Furniture/Stationery), price. Use for questions "
            "about product pricing or category."
        ),
        metadata={"table": "products"},
    ),
    Document(
        page_content=(
            "Table: orders. Columns: order_id (PK), customer_id (FK -> "
            "customers), order_date, status (completed/cancelled). Use for "
            "questions about when orders happened or their status."
        ),
        metadata={"table": "orders"},
    ),
    Document(
        page_content=(
            "Table: order_items. Columns: order_item_id (PK), order_id "
            "(FK -> orders), product_id (FK -> products), quantity. Use "
            "together with orders and products for revenue or "
            "quantity-sold questions."
        ),
        metadata={"table": "order_items"},
    ),
]

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(
    documents=TABLE_DOCS,
    embedding=embeddings,
    collection_name="schema_docs",
)


def retrieve_schema_context(question: str, k: int = 3) -> tuple[str, list[str]]:
    results = vectorstore.similarity_search(question, k=k)
    context_text = "\n\n".join(doc.page_content for doc in results)
    allowed_tables = [doc.metadata["table"] for doc in results]
    return context_text, allowed_tables