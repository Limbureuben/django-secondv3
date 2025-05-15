from myapp.models import Report
from .models import *
from rest_framework import serializers # type: ignore

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        
        
class ProblemReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UssdReport
        fields = ['id', 'phone_number', 'open_space', 'description', 'reference_number', 'status']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_staff']


class ProfileImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_image']

# serializers.py
class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'profile_image']

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            return request.build_absolute_uri(obj.profile_image.url)
        return None
    

# class OpenSpaceBookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OpenSpaceBooking
#         exclude = ['user']  # Prevent users from setting this directly

#     def create(self, validated_data):
#         user = self.context['request'].user  # Get user from request context
#         booking = OpenSpaceBooking(user=user, **validated_data)
#         booking.end_time = booking.calculate_end_time()

#         open_space = booking.open_space
#         if open_space.status == 'unavailable':
#             raise serializers.ValidationError("This open space is already booked.")

#         booking.save()
#         open_space.status = 'unavailable'
#         open_space.save()
#         return booking


class OpenSpaceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenSpaceBooking
        fields = '__all__'
        extra_kwargs = {
            'space': {'required': False}  # not required from input
        }
    
    def create(self, validated_data):
        request = self.context.get('request')
        space_id = request.data.get('space_id') if request else None

        if not space_id:
            raise serializers.ValidationError({"space": "This field is required."})

        try:
            space = OpenSpace.objects.get(id=space_id)
        except OpenSpace.DoesNotExist:
            raise serializers.ValidationError({"space": "Open space not found."})

        if space.status == 'unavailable':
            raise serializers.ValidationError({"space": "This open space has already been booked and is unavailable."})

        validated_data.pop('space', None)  # Remove if present
        booking = OpenSpaceBooking.objects.create(space=space, **validated_data)
        return booking



