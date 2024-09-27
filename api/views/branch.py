from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from organization.models import Branch, Terminal

class GetBranchImageView(APIView):
    def get(self, request, branch_id, terminal_no, format=None):
        try:
            # Get the branch object by its ID
            branch = Branch.objects.get(pk=branch_id)

            terminal_obj = Terminal.objects.filter(branch=branch, terminal_no=terminal_no).first()

 
            # # Check if the branch has an associated image
            # if branch.branch_image:
            #     # Return the URL to the branch's image
            #     image_url = branch.branch_image.url
            if terminal_obj.terminal_image:
                image_url = terminal_obj.terminal_image.url
                return Response({'branch_image_url': image_url}, status=status.HTTP_200_OK)
                # return Response({'branch_image_url': image_url}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No image found for this branch.'}, status=status.HTTP_404_NOT_FOUND)
        except Branch.DoesNotExist:
            return Response({'message': 'Branch not found.'}, status=status.HTTP_404_NOT_FOUND)