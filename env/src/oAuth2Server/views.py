from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import requests
from .serializers import CreateUserSerializer

CLIENT_ID = 'KITaTfGDX3gf5oKes0i3ydme03mivZWuv82MSTb0'
CLIENT_SECRET = 'UVl03Wz9UEffGdMVsquKVeZ5cPG1f2G9ZfsnidPxTHo3SBRDWF5K5oVT2JDC2BVX8DcprSbD75QTX4AZJgO3RBgmdhyO9nYXeO3vuwfNObiR5J4S6tAtZgw0KM2tjD6a'

IP_token = 'http://193.61.36.136:8000/o/token/'
IP_revoke_token = 'http://193.61.36.136:8000/o/revoke_token/'


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    Registers user to the server. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    # Put the data from the request into the serializer
    serializer = CreateUserSerializer(data=request.data)
    # Validate the data
    if serializer.is_valid():
        # If it is valid, save the data (creates a user).
        serializer.save()
        # Then we get a token for the created user.
        # This could be done differentley
        r = requests.post(IP_token,
                          data={
                              'grant_type': 'password',
                              'username': request.data['username'],
                              'password': request.data['password'],
                              'client_id': CLIENT_ID,
                              'client_secret': CLIENT_SECRET,
                          },
                          )
        return Response(r.json())
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(
        IP_token,
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Registers user to the server. Input should be in the format:
    {"refresh_token": "<token>"}
    '''
    r = requests.post(
        IP_token,
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    r = requests.post(
        IP_revoke_token,
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    # If it goes well return sucess message (would be empty otherwise)
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    # Return the error if it goes badly
    return Response(r.json(), r.status_code)
