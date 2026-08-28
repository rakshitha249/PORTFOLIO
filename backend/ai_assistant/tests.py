from django.test import TestCase
from unittest.mock import patch, MagicMock
from ai_assistant.models import KnowledgeDocument, KnowledgeChunk
from ai_assistant.chunker import TextChunker
from ai_assistant.document_generator import DocumentGenerator

class AIAssistantTests(TestCase):
    def test_chunker(self):
        chunker = TextChunker(chunk_size=20, chunk_overlap=5)
        text = "Hello world! This is a test of the text chunking functionality."
        chunks = chunker.chunk_text(text)
        self.assertTrue(len(chunks) > 1)

    def test_document_generator(self):
        class MockProject:
            id = 1
            title = "Test Project"
            description = "Description"
            technologies = "Python"
            slug = "test-project"
            
        doc = DocumentGenerator.generate_project_document(MockProject())
        self.assertEqual(doc['title'], "Test Project")
        self.assertEqual(doc['source_type'], "project")
        self.assertTrue("Python" in doc['content'])

    @patch('ai_assistant.management.commands.rebuild_knowledge_base.GithubService')
    @patch('ai_assistant.embeddings.get_embedding_service')
    def test_rebuild_command(self, mock_get_embedding, mock_github):
        mock_service = MagicMock()
        mock_service.get_embedding.return_value = [0.1] * 768
        mock_get_embedding.return_value = mock_service
        
        mock_github.get_repositories.return_value = []
        
        from django.core.management import call_command
        call_command('rebuild_knowledge_base')
        
        self.assertEqual(KnowledgeDocument.objects.count(), 0)

    @patch('ai_assistant.views.get_embedding_service')
    def test_search_endpoint(self, mock_get_embedding):
        mock_service = MagicMock()
        mock_service.get_embedding.return_value = [0.1] * 768
        mock_get_embedding.return_value = mock_service

        doc = KnowledgeDocument.objects.create(
            title="Test", source_type="project", source_id="1", content="test"
        )
        KnowledgeChunk.objects.create(
            document=doc, content="test chunk", chunk_index=0, embedding=[0.1] * 768
        )
        
        from django.urls import reverse
        response = self.client.post(reverse('ai-search'), {'query': 'test'})
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('results' in response.data)
        self.assertEqual(len(response.data['results']), 1)
