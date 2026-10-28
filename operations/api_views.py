
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Asset
from .serializers import AssetSerializer
from .permissions import has_role

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def asset_list_api(request):

    if request.method == "GET":
        assets = Asset.objects.all()[:100]
        serializer = AssetSerializer(assets, many=True)

        return Response({"assets": serializer.data})

    if not has_role(request.user, "Admin", "Supervisor"):
        return Response(
            {"detail": "You do not have permission to create assets."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = AssetSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def asset_detail_api(request, pk):
    asset = get_object_or_404(Asset, pk=pk)

    if request.method == "GET":
        serializer = AssetSerializer(asset)
        return Response(serializer.data)

    # Only Admin and Supervisor may modify assets.
    if not has_role(request.user, "Admin", "Supervisor"):
        return Response(
            {"detail": "You do not have permission to update assets."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = AssetSerializer(
        asset,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
