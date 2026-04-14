from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Material, Tag
from .utils import generate_file_hash, extract_text_from_file
from .ml_engine import classifier # Import our new classifier

from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import MaterialSerializer

    
from django.shortcuts import get_object_or_404
from .models import Favorite

from rest_framework.exceptions import PermissionDenied
from .models import Sharing
from rest_framework.exceptions import PermissionDenied


class MaterialUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        title = request.data.get('title')

        if not file_obj or not title:
            return Response({"error": "Title and file are required."}, status=status.HTTP_400_BAD_REQUEST)

        # 1. THE FIX: Read the raw bytes from the Django wrapper immediately
        file_bytes = file_obj.read()
        
        # 2. Reset the pointer right away so Django's save() method doesn't write a 0-byte file later!
        file_obj.seek(0) 

        # 3. Pass the pure bytes to our utility functions
        file_hash = generate_file_hash(file_bytes)
        if Material.objects.filter(file_hash=file_hash).exists():
            return Response({"error": "This file has already been uploaded to the platform."}, status=status.HTTP_409_CONFLICT)

        extracted_text = extract_text_from_file(file_bytes, file_obj.name)

        # --- INTELLIGENCE LAYER INTEGRATION ---
        classification_result = classifier.classify_text(extracted_text)
        final_status = classification_result["status"]
        suggested_tag_names = classification_result["suggested_tags"]
        # ------------------------------------------

        # 4. Save to database using the original file_obj
        material = Material.objects.create(
            title=title,
            file=file_obj, 
            file_hash=file_hash,
            uploader=request.user,
            extracted_text=extracted_text,
            status=final_status 
        )

        if final_status == 'AUTO_FILED' and suggested_tag_names:
            for tag_name in suggested_tag_names:
                tag_obj, created = Tag.objects.get_or_create(name=tag_name, defaults={'category': 'COURSE'})
                material.tags.add(tag_obj)

        return Response({
            "message": "File processed.",
            "material_id": material.id,
            "title": material.title,
            "status": final_status,
            "confidence_score": classification_result.get("confidence_score"),
            "assigned_tags": [tag.name for tag in material.tags.all()]
        }, status=status.HTTP_201_CREATED)


class MaterialListView(generics.ListAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # THE PERMISSION GATEKEEPER
        # Users can see: 
        # 1. Their own materials (even if pending or private)
        # 2. Public materials (that are auto-filed)
        # 3. Targeted materials aimed at their department (that are auto-filed)
        queryset = Material.objects.filter(
            Q(uploader=user) | 
            (
                Q(status='AUTO_FILED') & 
                (
                    Q(sharing_settings__permission_type='PUBLIC') |
                    Q(sharing_settings__permission_type='TARGETED', sharing_settings__target_group=user.department)
                )
            )
        )
        
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(extracted_text__icontains=search_query)
            ).distinct() # Use distinct() to avoid duplicates when joining tables

        tag_id = self.request.query_params.get('tag', None)
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        uploader_id = self.request.query_params.get('uploader', None)
        if uploader_id:
            queryset = queryset.filter(uploader__id=uploader_id)


        # 4. Filter by Favorites
        is_favorited_query = self.request.query_params.get('is_favorited', None)
        if is_favorited_query == 'true':
            # 'favorited_by' is the related_name we set on the Favorite model
            queryset = queryset.filter(favorited_by__user=user)
        return queryset.order_by('-upload_time')
    
    
class MaterialDetailView(generics.RetrieveAPIView):
    """Fetches a single material by ID, respecting sharing permissions."""
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Material.objects.filter(
            Q(uploader=user) | 
            (
                Q(status='AUTO_FILED') & 
                (
                    Q(sharing_settings__permission_type='PUBLIC') |
                    Q(sharing_settings__permission_type='TARGETED', sharing_settings__target_group=user.department)
                )
            )
        )

class ToggleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, material_id):
        material = get_object_or_404(Material, id=material_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, material=material)

        if not created:
            # If it already exists, the user is "un-favoriting" it
            favorite.delete()
            return Response({"message": "Removed from favorites."}, status=status.HTTP_200_OK)

        return Response({"message": "Added to favorites."}, status=status.HTTP_201_CREATED)
    
    


class UpdateSharingView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, material_id):
        material = get_object_or_404(Material, id=material_id)
        
        # Security check: Only the uploader can change permissions
        if material.uploader != request.user:
            raise PermissionDenied("You do not have permission to modify this resource.")

        sharing_setting = material.sharing_settings
        
        # Update the fields if they are provided in the request
        if 'permission_type' in request.data:
            sharing_setting.permission_type = request.data['permission_type']
        if 'target_group' in request.data:
            sharing_setting.target_group = request.data['target_group']
            
        sharing_setting.save()

        return Response({"message": "Sharing permissions updated successfully.", 
                         "current_permission": sharing_setting.permission_type}, 
                         status=status.HTTP_200_OK)
        
        
        

class MaterialDeleteView(generics.DestroyAPIView):
    """Allows a user to permanently delete their own material."""
    queryset = Material.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        # 1. Security Check: Only the uploader can delete it
        if instance.uploader != self.request.user:
            raise PermissionDenied("You do not have permission to delete this resource.")
        
        # 2. Storage Cleanup: Delete the physical file from the media folder
        if instance.file:
            instance.file.delete(save=False)
            
        # 3. Delete the database record (this also cascades and deletes associated Sharing/Favorite records)
        instance.delete()