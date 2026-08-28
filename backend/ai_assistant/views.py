from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from drf_spectacular.utils import extend_schema, OpenApiTypes
from .models import KnowledgeChunk, is_postgres
from .embeddings import get_embedding_service
import json
import math

class SemanticSearchView(APIView):
    """
    Endpoint for semantic search over the knowledge base.
    """
    @extend_schema(
        request={'application/json': {'type': 'object', 'properties': {
            'query': {'type': 'string'},
            'top_k': {'type': 'integer', 'default': 5},
            'source_type': {'type': 'string', 'enum': ['profile', 'skill', 'project', 'education', 'experience', 'certification', 'github']}
        }}},
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request):
        query = request.data.get('query')
        top_k = request.data.get('top_k', 5)
        source_type = request.data.get('source_type')

        if not query or not isinstance(query, str):
            return Response({'error': 'Invalid or missing query'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            top_k = int(top_k)
            if top_k <= 0 or top_k > 50:
                 return Response({'error': 'top_k must be between 1 and 50'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid top_k'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            embedding_service = get_embedding_service()
            query_embedding = embedding_service.get_embedding(query)
        except Exception as e:
            return Response({'error': f'Embedding generation failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        qs = KnowledgeChunk.objects.select_related('document').all()
        if source_type:
            qs = qs.filter(document__source_type=source_type)
            
        results = []

        if is_postgres():
            from pgvector.django import L2Distance
            qs = qs.annotate(distance=L2Distance('embedding', query_embedding)).order_by('distance')[:top_k]
            
            for chunk in qs:
                results.append({
                    'title': chunk.document.title,
                    'content': chunk.content,
                    'source_type': chunk.document.source_type,
                    'source_id': chunk.document.source_id,
                    'similarity_score': 1.0 / (1.0 + getattr(chunk, 'distance', 0)),
                    'metadata': chunk.document.metadata
                })
        else:
            def cosine_similarity(v1, v2):
                dot_product = sum(a * b for a, b in zip(v1, v2))
                norm1 = math.sqrt(sum(a * a for a in v1))
                norm2 = math.sqrt(sum(b * b for b in v2))
                if norm1 == 0 or norm2 == 0:
                    return 0
                return dot_product / (norm1 * norm2)

            all_chunks = list(qs)
            scored_chunks = []
            
            for chunk in all_chunks:
                if chunk.embedding:
                    try:
                        emb = chunk.embedding if isinstance(chunk.embedding, list) else json.loads(chunk.embedding)
                        sim = cosine_similarity(query_embedding, emb)
                        scored_chunks.append((sim, chunk))
                    except Exception:
                        pass
                        
            scored_chunks.sort(key=lambda x: x[0], reverse=True)
            
            for sim, chunk in scored_chunks[:top_k]:
                 results.append({
                    'title': chunk.document.title,
                    'content': chunk.content,
                    'source_type': chunk.document.source_type,
                    'source_id': chunk.document.source_id,
                    'similarity_score': sim,
                    'metadata': chunk.document.metadata
                })

        return Response({'results': results})
