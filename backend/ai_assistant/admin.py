from django.contrib import admin
from .models import KnowledgeDocument, KnowledgeChunk

@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'source_type', 'source_id', 'created_at', 'updated_at')
    list_filter = ('source_type',)
    search_fields = ('title', 'content', 'source_id')
    readonly_fields = ('content_hash', 'created_at', 'updated_at')

@admin.register(KnowledgeChunk)
class KnowledgeChunkAdmin(admin.ModelAdmin):
    list_display = ('document', 'chunk_index', 'created_at')
    list_filter = ('document__source_type',)
    search_fields = ('document__title', 'content')
    readonly_fields = ('content_hash', 'embedding', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('document')
