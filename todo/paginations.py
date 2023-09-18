
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework import status
class Custom_pagination_response(pagination.PageNumberPagination):
    '''
    this class deals with the custom response in the return of get_paginated_response
    '''

    def get_paginated_response(self,data):
        return Response({
            "next":self.get_next_link(),
            "prev":self.get_previous_link(),
            "status":1,
            "message":"success",
            "data":data
        },status=status.HTTP_200_OK)
