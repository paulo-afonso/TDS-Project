from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from dotenv import load_dotenv
from treegia.settings import TRELLO_URL, STR_URL
import os
import requests
import json
import base64


load_dotenv()
LOGIN_STR = os.getenv('LOGIN_STR')
PASS_STR = os.getenv('PASS_STR')
TRELLO_KEY = os.getenv('TRELLO_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')


@api_view(['GET'])
def get_boards(request):
    if request.method == 'GET':
        board_endpoint = TRELLO_URL+'members/me/boards'

        jsonObj = {'fields':'name,id', 'key':TRELLO_KEY, 'token':TRELLO_TOKEN}
        
        boards = requests.get(board_endpoint, json=jsonObj)

        return Response(json.loads(boards.text))


id_board = '61a51aad8f90374fceb71379'

@api_view(['GET'])
def get_lists(request):
    if request.method == 'GET':
        #id_board = request.hearder['id_board']
        list_endpoint = TRELLO_URL+ 'boards/' + id_board + '/lists'
        jsonObj = {'fields':'name,id', 'id':id_board, 'key':TRELLO_KEY, 'token':TRELLO_TOKEN}
        
        lists = requests.get(list_endpoint, json=jsonObj)
        
        return Response(json.loads(lists.text))



### Gettting cards of each list

@api_view(['GET'])
def get_cards(request):
    if request.method == 'GET':
        id_list = request.hearder['id_list']
        card_endpoint = TRELLO_URL+ 'lists/' + id_list + '/cards'
        jsonObj = {'fields':'name,id', 'id':id_list, 'key':TRELLO_KEY, 'token':TRELLO_TOKEN}
        
        cards = requests.get(card_endpoint, json=jsonObj)
        
        return Response(json.loads(cards.text))



### Getting checkpoints of a card

@api_view(['GET'])
def get_cards_checks(request):
    if request.method == 'GET':
        id_card = request.hearder['id_card']
        card_info_endpoint = TRELLO_URL + 'cards/' + id_card + '/checklists'
        jsonObj = {'fields':'checkItems', 'id':id_card, 'key':TRELLO_KEY, 'token':TRELLO_TOKEN}
        
        card_info = requests.get(card_info_endpoint, json=jsonObj)
        
        return Response(json.loads(card_info.text))
    

### CONSUMING STRATEEGIA API ###


@api_view(['POST'])
def login(request):
    login_url = STR_URL + 'users/v1/auth/signin'
    username = request.header['username']
    password = request.header['password']
    userpass = username + ':' + password
    encoded_u = base64.b64encode(userpass.encode()).decode()
    headers = {
        'Content-Type':'application/json',
        "Authorization" : f"Basic {encoded_u}" 
    }
    
    r = requests.post(login_url, headers=headers)
    
 
    return r.json()

token = login(LOGIN_STR, PASS_STR)['access_token']


### Creating project with board name

@api_view(['POST'])
def post_projects(request):
    project_url = STR_URL + 'projects/v1/project'
    header = {
        'Content-Type':'application/json',
        'Authorization':f'Bearer {token}'
    }
    payload = {
        "color":request.hearder['color'],
        'description':request.hearder['description'],
        "lab_owner_id":request.hearder['lab_owner_id'],
        "title":request.hearder['title']
    }

    posts = requests.post(project_url, data = json.dumps(payload), headers=header)
    

    return posts.json()

### Creating map with list name

projectID = '61d35bc35828d95a53150603'

@api_view(['POST'])
def post_maps(request):
    url_maps = STR_URL + 'projects/v1/project/{}/map'.format(projectID)
    header = {
        'Content-Type':'application/json',
        'Authorization':'Bearer {}'.format(token)
    }
    payloads = {
        "title":request.hearder['title']
    }

    postss = requests.post(url_maps, data = json.dumps(payloads), headers=header)
    

    return postss.json()

### Creating kit with checklists 

@api_view(['POST'])
def post_kit(request):
    url_kit = STR_URL + 'tools/v1/kit'
    header = {
        'Content-Type':'application/json',
        'Authorization':'Bearer {}'.format(token)
    }
    payloads = {
      "color": "BLUE",
      "description": "Kit de um programador lindo",
      "questions": [
        {
          "question": "Quais condições favorecem a abertura dos estômatos?"
        },
        {
          "question": "Como os estômatos influenciam na transpiração?"
        },
        {
          "question": "Cite uma estrutura deles e discuta sua importância."
        }      
      ],
      "references": [
        {
          "description": "Pesquisa pro google, não sou teu pai",
          "url": "https://google.com"
        }
      ],
      "title":request.hearder['title']
    }

    post = requests.post(url_kit, data = json.dumps(payloads), headers=header)
    

    return post.json()

### Posting first kit on map


# mapId = '61d35c00f04f183a377119b7'
# toolId = '61d35c206b39c9403a3cca00'
# url_kit_map = STR_URL + 'projects/v1/map/{}/divergence-point'.format(mapId)

# @api_view(['POST'])
# def post_kit_on_map(request):
#     header = {
#         'Content-Type':'application/json',
#         'Authorization':'Bearer {}'.format(token)
#     }
#     payloads = {
#       "position": {
#         "col": 0,
#         "row": 0
#       },
#       "tool_id": f"{toolId}"
#     }

#     post = requests.post(url_kit_map, data = json.dumps(payloads), headers=header)
    

#     return post.json()

