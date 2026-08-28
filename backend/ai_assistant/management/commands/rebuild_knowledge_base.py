import os
import json
from django.core.management.base import BaseCommand
from ai_assistant.models import KnowledgeDocument, KnowledgeChunk
from ai_assistant.document_generator import DocumentGenerator
from ai_assistant.chunker import TextChunker
from ai_assistant.embeddings import get_embedding_service
from portfolio.models import Profile, Skill
from projects.models import Project
from experience.models import Experience
from education.models import Education
from certificates.models import Certificate
from github.services import GithubService

class Command(BaseCommand):
    help = 'Rebuilds the RAG knowledge base from portfolio data and GitHub.'

    def handle(self, *args, **options):
        self.stdout.write("Initializing rebuild...")
        
        chunker = TextChunker()
        try:
            embedding_service = get_embedding_service()
            self.stdout.write(f"Using embedding service: {embedding_service.__class__.__name__}")
        except Exception as e:
            self.stderr.write(f"Failed to initialize embedding service: {e}")
            return

        documents = []
        
        self.stdout.write("Extracting Profile...")
        for profile in Profile.objects.all():
            documents.append(DocumentGenerator.generate_profile_document(profile))

        self.stdout.write("Extracting Skills...")
        for skill in Skill.objects.all():
            documents.append(DocumentGenerator.generate_skill_document(skill))
            
        self.stdout.write("Extracting Projects...")
        for project in Project.objects.all():
            documents.append(DocumentGenerator.generate_project_document(project))
            
        self.stdout.write("Extracting Experience...")
        for exp in Experience.objects.all():
            documents.append(DocumentGenerator.generate_experience_document(exp))
            
        self.stdout.write("Extracting Education...")
        for edu in Education.objects.all():
            documents.append(DocumentGenerator.generate_education_document(edu))
            
        self.stdout.write("Extracting Certifications...")
        for cert in Certificate.objects.all():
            documents.append(DocumentGenerator.generate_certification_document(cert))
            
        self.stdout.write("Extracting GitHub Repositories...")
        try:
            repos = GithubService.get_repositories()
            for repo in repos:
                documents.append(DocumentGenerator.generate_github_document(repo))
        except Exception as e:
            self.stderr.write(f"GitHub extraction failed, skipping: {e}")

        self.stdout.write(f"Generated {len(documents)} document templates.")
        
        valid_doc_ids = []
        chunks_created = 0

        for doc_data in documents:
            import hashlib
            content_hash = hashlib.sha256(doc_data['content'].encode('utf-8')).hexdigest()
            
            doc, created = KnowledgeDocument.objects.get_or_create(
                source_type=doc_data['source_type'],
                source_id=doc_data['source_id'],
                defaults={
                    'title': doc_data['title'],
                    'content': doc_data['content'],
                    'metadata': doc_data['metadata'],
                    'content_hash': content_hash
                }
            )
            
            valid_doc_ids.append(doc.id)
            
            if not created and doc.content_hash == content_hash:
                self.stdout.write(f"Skipping unchanged document: {doc.title}")
                continue
                
            if not created:
                doc.title = doc_data['title']
                doc.content = doc_data['content']
                doc.metadata = doc_data['metadata']
                doc.content_hash = content_hash
                doc.save()
                doc.chunks.all().delete()
                self.stdout.write(f"Updating changed document: {doc.title}")
            else:
                self.stdout.write(f"Creating new document: {doc.title}")

            chunks = chunker.chunk_text(doc.content)
            for idx, chunk_text in enumerate(chunks):
                try:
                    embedding = embedding_service.get_embedding(chunk_text)
                    KnowledgeChunk.objects.create(
                        document=doc,
                        content=chunk_text,
                        chunk_index=idx,
                        metadata=doc.metadata,
                        embedding=embedding if isinstance(embedding, list) else list(embedding)
                    )
                    chunks_created += 1
                except Exception as e:
                    self.stderr.write(f"Failed to embed chunk {idx} of {doc.title}: {e}")

        orphaned = KnowledgeDocument.objects.exclude(id__in=valid_doc_ids)
        orphans_count = orphaned.count()
        if orphans_count > 0:
            self.stdout.write(f"Deleting {orphans_count} orphaned documents...")
            orphaned.delete()

        self.stdout.write(self.style.SUCCESS(f"Knowledge base rebuild complete. Created/Updated {chunks_created} chunks."))
