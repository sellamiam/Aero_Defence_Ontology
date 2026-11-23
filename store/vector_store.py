"""
Vector & Semantic Retrieval Store.
Hybrid Neural + Lexical retrieval engine combining open-source SentenceTransformers
dense embeddings (384-dimensional latent semantic space) with n-gram TF-IDF matching.
Enables vocabulary-independent semantic matching, typo tolerance, and fast cosine similarity.
"""

from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger("VectorStore")

# Check if sentence-transformers is available
_HAS_SENTENCE_TRANSFORMERS = False
try:
    from sentence_transformers import SentenceTransformer
    _HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    _HAS_SENTENCE_TRANSFORMERS = False


class VectorStore:
    """Manages semantic capability embeddings and fast hybrid vector similarity searches."""

    _cached_model: Optional[Any] = None

    def __init__(self, index_file: Optional[Path] = None, model_name: str = "all-MiniLM-L6-v2"):
        self.workspace_root = Path(__file__).resolve().parent.parent
        self.index_file = index_file or (self.workspace_root / "data" / "graph" / "vector_index.pkl")
        self.model_name = model_name
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix: Optional[Any] = None
        self.dense_matrix: Optional[np.ndarray] = None
        self.corpus_metadata: List[Dict[str, Any]] = []

    @classmethod
    def _get_transformer_model(cls, model_name: str = "all-MiniLM-L6-v2"):
        """Cached lazy-loader for local open-source transformer model."""
        if not _HAS_SENTENCE_TRANSFORMERS:
            return None
        if cls._cached_model is None:
            logger.info(f"Loading local open-source neural model '{model_name}'...")
            try:
                cls._cached_model = SentenceTransformer(model_name, local_files_only=True)
            except Exception:
                cls._cached_model = SentenceTransformer(model_name)
        return cls._cached_model

    def build_index_from_graph(self, graph_store: Any) -> Dict[str, Any]:
        """Extracts capability statements from the GraphStore and builds hybrid vector matrices."""
        logger.info("Extracting capabilities from GraphStore for hybrid vector indexing...")
        sparql = """
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?cage ?companyName ?title ?desc ?kic ?trl ?country ?province ?city WHERE {
                ?c aero:cageCode ?cage ;
                   aero:legalName ?companyName ;
                   aero:headquartersCountry ?country ;
                   aero:headquartersCity ?city ;
                   aero:hasCapability ?cap .
                ?cap rdfs:label ?title ;
                     aero:capabilityDescription ?desc .
                OPTIONAL { ?c aero:headquartersProvince ?province . }
                OPTIONAL { ?cap aero:alignedWithKIC ?kic . }
                OPTIONAL { ?cap aero:trlValue ?trl . }
            }
        """
        rows = graph_store.query_sparql(sparql)
        logger.info(f"Retrieved {len(rows)} capability records for vector indexing.")

        corpus_texts = []
        self.corpus_metadata = []

        for r in rows:
            text = f"{r['title']} {r['desc']} {r.get('kic', '')}"
            corpus_texts.append(text)
            self.corpus_metadata.append({
                "cage_code": r["cage"],
                "company_name": r["companyName"],
                "country": r["country"],
                "province": r.get("province"),
                "city": r.get("city"),
                "title": r["title"],
                "description": r["desc"],
                "kic": r.get("kic"),
                "trl": int(r["trl"]) if r.get("trl") else None,
            })

        if not corpus_texts:
            logger.warning("No capability texts found to index.")
            return {"indexed_count": 0}

        # 1. Lexical TF-IDF Matrix (for exact terms, CAGE codes, acronyms)
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            sublinear_tf=True,
            stop_words="english",
            max_features=25000,
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus_texts)
        logger.info(f"Lexical TF-IDF matrix constructed: shape {self.tfidf_matrix.shape}")

        # 2. Neural Dense Embeddings (open-source SentenceTransformer)
        model = self._get_transformer_model(self.model_name)
        if model is not None:
            logger.info(f"Encoding {len(corpus_texts)} capabilities using open-source neural embeddings ({self.model_name})...")
            self.dense_matrix = model.encode(
                corpus_texts,
                batch_size=128,
                show_progress_bar=False,
                normalize_embeddings=True,
            )
            logger.info(f"Neural dense embedding matrix constructed: shape {self.dense_matrix.shape}")
        else:
            logger.info("SentenceTransformers not available; defaulting to lexical TF-IDF store.")
            self.dense_matrix = None

        # Persist index
        self.save_index()
        return {
            "indexed_count": len(self.corpus_metadata),
            "lexical_dims": self.tfidf_matrix.shape[1],
            "neural_dims": self.dense_matrix.shape[1] if self.dense_matrix is not None else 0,
        }

    def query_semantic(self, query_text: str, top_k: int = 50, alpha: float = 0.85) -> List[Dict[str, Any]]:
        """
        Computes hybrid cosine similarity:
        score = alpha * neural_score + (1 - alpha) * tfidf_score
        """
        if self.corpus_metadata is None or len(self.corpus_metadata) == 0:
            if not self.load_index():
                raise RuntimeError("Vector index not initialized. Call build_index_from_graph first.")

        # Compute neural similarity if dense matrix is available
        neural_sims: Optional[np.ndarray] = None
        model = self._get_transformer_model(self.model_name)
        if model is not None and self.dense_matrix is not None:
            try:
                q_emb = model.encode([query_text], normalize_embeddings=True)
                # Cosine similarity is simply dot product because vectors are L2-normalized
                neural_sims = np.dot(self.dense_matrix, q_emb.T).flatten()
            except Exception as e:
                logger.warning(f"Neural embedding failed: {e}; falling back to lexical.")
                neural_sims = None

        # Compute TF-IDF lexical similarity
        tfidf_sims: Optional[np.ndarray] = None
        if self.vectorizer is not None and self.tfidf_matrix is not None:
            query_vec = self.vectorizer.transform([query_text])
            tfidf_sims = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Hybrid fusion
        if neural_sims is not None and tfidf_sims is not None:
            similarities = alpha * neural_sims + (1.0 - alpha) * tfidf_sims
        elif neural_sims is not None:
            similarities = neural_sims
        elif tfidf_sims is not None:
            similarities = tfidf_sims
        else:
            raise RuntimeError("No index matrix available for similarity computation.")

        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score <= 0.001:
                continue
            meta = self.corpus_metadata[idx]
            results.append({
                "cage_code": meta["cage_code"],
                "company_name": meta["company_name"],
                "country": meta["country"],
                "province": meta.get("province"),
                "city": meta.get("city"),
                "similarity_score": round(score, 4),
                "matched_capability_title": meta["title"],
                "matched_capability_description": meta["description"],
                "kic": meta["kic"],
                "trl": meta["trl"],
            })

        return results

    def save_index(self):
        """Serializes vectorizer, matrix, dense matrix, and metadata to disk."""
        self.index_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_file, "wb") as f:
            pickle.dump({
                "vectorizer": self.vectorizer,
                "matrix": self.tfidf_matrix,
                "dense_matrix": self.dense_matrix,
                "metadata": self.corpus_metadata,
                "model_name": self.model_name,
            }, f)
        logger.info(f"Vector store saved to {self.index_file}")

    def load_index(self) -> bool:
        """Loads serialized vector store from disk."""
        if not self.index_file.exists():
            return False
        try:
            with open(self.index_file, "rb") as f:
                data = pickle.load(f)
                self.vectorizer = data.get("vectorizer")
                self.tfidf_matrix = data.get("matrix")
                self.dense_matrix = data.get("dense_matrix")
                self.corpus_metadata = data.get("metadata", [])
                self.model_name = data.get("model_name", "all-MiniLM-L6-v2")
            return True
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            return False
