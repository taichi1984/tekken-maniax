from rest_framework import serializers
from .models import GuideComment
from top.models import UserProfile

#class UserProfileSerializer(serializers.ModelSerializer):


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'  # ユーザー名のみを含める場合

class CommentSerializer(serializers.ModelSerializer):
    contributor = UserProfileSerializer(source='contributor.userprofile',read_only=True)

    class Meta:
        model = GuideComment
        fields = '__all__'  # すべてのフィールドを含む