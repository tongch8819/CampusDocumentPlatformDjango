from rest_framework import serializers
from .models import Material, Tag, Comment, Favorite, Sharing
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'department']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'category']

# Add this new serializer
class SharingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sharing
        fields = ['permission_type', 'target_group']

class MaterialSerializer(serializers.ModelSerializer):
    uploader = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    sharing_settings = SharingSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()
    
    # NEW: Add a dynamic field to check the favorite status
    is_favorited = serializers.SerializerMethodField() 

    class Meta:
        model = Material
        # Make sure to add 'is_favorited' to the fields list!
        fields = ['id', 'title', 'file_url', 'uploader', 'tags', 'status', 'upload_time', 'sharing_settings', 'is_favorited', 'extracted_text'] 

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            return request.build_absolute_uri(obj.file.url)
        return None

    # NEW: Logic to determine if the current user favorited this item
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Returns True if a favorite record exists for this user and material
            return Favorite.objects.filter(user=request.user, material=obj).exists()
        return False

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']