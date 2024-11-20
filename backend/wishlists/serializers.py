from rest_framework.serializers import ModelSerializer
from rooms.serializers import RoomListSerializer
from .models import Wishlist

class WishListSerializer(ModelSerializer):
    
    room = RoomListSerializer(
        many=True,
        read_only=True,
    )
    
    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )