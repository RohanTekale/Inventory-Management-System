from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True, required=False)  # Add this

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role', None)  # extract role
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Assign role to group
        if role:
            try:
                group = Group.objects.get(name=role)
                user.groups.add(group)
            except Group.DoesNotExist:
                raise serializers.ValidationError(f"Group '{role}' does not exist.")

        return user


