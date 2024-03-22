import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import time
from asgiref.sync import async_to_sync


class GameRoomManagerPong:

    rooms = {}  # Stores room_name: host_name

    @classmethod
    def create_room_pong(cls, host_name, room_settings):
        room_id = f"{host_name}_Game"
        cls.rooms[room_id] = {"host": host_name, "guest": None, "num_players": 2, "room_settings": room_settings}
        return room_id

    @classmethod
    def create_room_pong_tournament(cls, host_name, room_settings, round):
        room_id = f"{host_name}_Game_tournament"
        cls.rooms[room_id] = {"host": host_name, "guest": None, "num_players": 2, "room_settings": room_settings, "round": round}
        return room_id

    @classmethod
    def list_rooms_pong(cls):
        return [room_id for room_id, details in cls.rooms.items() if details["guest"] is None]

    @classmethod
    def list_rooms_pong_tournament(cls):
        return [room_id for room_id, details in cls.rooms.items() if details["guest"] is None and details["round"] > 0]

    @classmethod
    def join_room_pong(cls, room_id, guest_name):
        if room_id in cls.rooms and cls.rooms[room_id]["guest"] is None:
            cls.rooms[room_id]["guest"] = guest_name
            return True
        return False

    @classmethod
    def join_room_pong_tournament(cls, room_id, guest_name):
        if room_id in cls.rooms and cls.rooms[room_id]["guest"] is None and cls.rooms[room_id]["num_players"] < cls.rooms[room_id]["room_settings"]:
            cls.rooms[room_id]["num_players"] += 1
            return True
        elif room_id in cls.rooms and cls.rooms[room_id]["num_players"] == cls.rooms[room_id]["room_settings"]:
            cls.rooms[room_id]["num_players"] += 1
            cls.rooms[room_id]["guest"] = guest_name
            return True
        return False


class GameRoomManagerMemory:

    rooms = {}  # Stores room_name: host_name

    @classmethod
    def create_room_memory(cls, host_name, room_name):
        room_id = f"{host_name}_Game"
        cls.rooms[room_id] = {"host": host_name, "guest": None, "room_name": room_name}
        return room_id

    @classmethod
    def list_rooms_memory(cls):
        return [(room_id, details['room_name']) for room_id, details in cls.rooms.items() if details["guest"] is None]

    @classmethod
    def join_room_memory(cls, room_id, guest_name):
        if room_id in cls.rooms and cls.rooms[room_id]["guest"] is None:
            cls.rooms[room_id]["guest"] = guest_name
            return True
        return False


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'game_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_left',
                'channel_name': self.channel_name
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'create_room_pong_tournament':
            host_name = data.get('host_name')
            room_settings = data.get('room_settings')
            round = data.get('round')
            room_id = GameRoomManagerPong.create_room_pong_tournament(host_name, room_settings, round)
            await self.send(text_data=json.dumps({'action': 'room_created_pong', 'room_id': room_id}))

        elif action == 'create_room_pong':
            host_name = data.get('host_name')
            room_settings = data.get('room_settings')
            room_id = GameRoomManagerPong.create_room_pong(host_name, room_settings)
            await self.send(text_data=json.dumps({'action': 'room_created_pong', 'room_id': room_id}))

        elif action == 'create_room_memory':
            host_name = data.get('host_name')
            room_name = data.get('room_name')
            room_id = GameRoomManagerMemory.create_room_memory(host_name, room_name)
            await self.send(text_data=json.dumps({'action': 'room_created_memory', 'room_id': room_id}))

        elif action == 'list_rooms_pong':
            rooms = GameRoomManagerPong.list_rooms_pong()
            await self.send(text_data=json.dumps({'action': 'list_rooms_pong', 'rooms': rooms}))

        elif action == 'list_rooms_pong_tournament':
            rooms = GameRoomManagerPong.list_rooms_pong_tournament()
            await self.send(text_data=json.dumps({'action': 'list_rooms_pong_tournament', 'rooms': rooms}))

        elif action == 'list_rooms_memory':
            rooms = GameRoomManagerMemory.list_rooms_memory()
            await self.send(text_data=json.dumps({'action': 'list_rooms_memory', 'rooms': rooms}))

        elif action == 'join_room_pong':
            room_id = data.get('room_id')
            guest_name = data.get('guest_name')
            joined = GameRoomManagerPong.join_room_pong(room_id, guest_name)
            if joined:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'player_joined_pong',
                        'room_id': room_id,
                        'guest_name': guest_name,
                    }
                )
                await self.send(text_data=json.dumps({'action': 'joined_room_pong', 'room_id': room_id}))
            else:
                await self.send(text_data=json.dumps({'action': 'error', 'message': 'Room not found or full'}))

        elif action == 'join_room_pong_tournament':
            room_id = data.get('room_id')
            guest_name = data.get('guest_name')
            joined = GameRoomManagerPong.join_room_pong_tournament(room_id, guest_name)
            if joined:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'player_joined_pong_tournament',
                        'room_id': room_id,
                        'guest_name': guest_name,
                    }
                )
                await self.send(text_data=json.dumps({'action': 'joined_room_pong_tournament', 'room_id': room_id}))
            else:
                await self.send(text_data=json.dumps({'action': 'error', 'message': 'Room not found or full'}))

        elif action == 'join_room_memory':
            room_id = data.get('room_id')
            guest_name = data.get('guest_name')
            joined = GameRoomManagerMemory.join_room_memory(room_id, guest_name)
            if joined:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'player_joined_memory',
                        'room_id': room_id,
                        'guest_name': guest_name,
                    }
                )
                await self.send(text_data=json.dumps({'action': 'joined_room_memory', 'room_id': room_id}))
            else:
                await self.send(text_data=json.dumps({'action': 'error', 'message': 'Room not found or full'}))

        elif action == 'send_settings_memory':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_settings_memory',
                    'settings': data['settings']
                }
            )
        elif action == 'update_ball_position_pong':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ball_position',
                    'ball_x': data['ball_x'],
                    'ball_y': data['ball_y']
                }
            )
        elif action == 'update_player_scores_pong':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'player_scores_pong',
                    'player1': data['player1'],
                    'player2': data['player2']
                }
            )

        elif action == 'game_ended_pong':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_ended_pong',
                    'winner': data['winner']
                }
            )
        elif action == 'game_ended_pong_tournament':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_ended_pong_tournament',
                    'winner': data['winner']
                }
            )

        elif action == 'game_ended_pong':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_ended_pong',
                    'winner': data['winner']
                }
            )

        elif action == 'game_ended_memory':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_ended_memory',
                    'winner': data['winner']
                }
            )
        elif action == 'host_key_event':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'host_key_event',
                    'key': data['key']
                }
            )

        elif action == 'client_key_event':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'client_key_event',
                    'key': data['key']
                }
            )

        elif action == 'get_host_player':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'get_host_player',
                    'key': data['name']
                }
            )

        elif action == 'card_info':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_card_info',
                    'cards': data['cards'],
                    'settings': data['settings']
                }
            )

        elif action == 'player_turn_memory':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'player_turn_memory',
                    'player': data['player']
                }
            )

        elif action == 'card_clicked':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'card_clicked',
                    'card_id': data['card_id']
                }
            )

        elif action == 'card_returned':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'card_returned',
                    'card_id': data['card_id']
                }
            )

        elif action == 'update_score_memory':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_score_memory',
                    'score1': data['score1'],
                    'score2': data['score2']
                }
            )

        elif action == 'display_tournament_turn':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'display_tournament_turn',
                    'namePlayerTournament': data['namePlayerTournament'],
                    'score': data['score'],
                    'round': data['round']
                }
            )
            await self.send(text_data=json.dumps({'action': 'display_tournament_turn', 'namePlayerTournament': data['namePlayerTournament'], 'score': data['score'], 'round': data['round']}))

        elif action == 'launching_room':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'launching_room',
                    'nameAgainst': data['nameAgainst']
                }
            )

        elif action == 'all_room_launched':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'all_room_launched'
                }
            )

        elif action == 'change_tournament_round':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'change_tournament_round',
                    'round': data['round']
                }
            )

        elif action == 'adjust_second_round':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'adjust_second_round',
                    'mainHostLaunched': data['mainHostLaunched']
                }
            )

    async def adjust_second_round(self, event):
        await self.send(text_data=json.dumps({
            'action': 'adjust_second_round',
            'mainHostLaunched': event['mainHostLaunched']
        }))

    async def change_tournament_round(self, event):
        await self.send(text_data=json.dumps({
            'action': 'change_tournament_round',
            'round': event['round']
        }))

    async def all_room_launched(self, event):
        await self.send(text_data=json.dumps({
            'action': 'all_room_launched'
        }))

    async def launching_room(self, event):
        await self.send(text_data=json.dumps({
            'action': 'launching_room',
            'nameAgainst': event['nameAgainst']
        }))

    async def display_tournament_turn(self, event):
        await self.send(text_data=json.dumps({
            'action': 'display_tournament_turn',
            'namePlayerTournament': event['namePlayerTournament'],
            'score': event['score'],
            'round': event['round']
        }))

    async def game_ended_memory(self, event):
        await self.send(text_data=json.dumps({
            'action': 'game_ended_memory',
            'winner': event['winner']
        }))

    async def update_score_memory(self, event):
        await self.send(text_data=json.dumps({
            'action': 'update_score_memory',
            'score1': event['score1'],
            'score2': event['score2']
        }))

    async def card_returned(self, event):
        await self.send(text_data=json.dumps({
            'action': 'card_returned',
            'card_id': event['card_id']
        }))

    async def card_clicked(self, event):
        await self.send(text_data=json.dumps({
            'action': 'card_clicked',
            'card_id': event['card_id']
        }))

    async def player_turn_memory(self, event):
        await self.send(text_data=json.dumps({
            'action': 'player_turn_memory',
            'player': event['player']
        }))

    async def send_card_info(self, event):
        await self.send(text_data=json.dumps({
            'action': 'card_info',
            'cards': event['cards'],
            'settings': event['settings']
        }))

    async def get_host_player(self, event):
        await self.send(text_data=json.dumps({
            'action': 'get_host_player',
            'key': event['key']
        }))

    async def client_key_event(self, event):
        await self.send(text_data=json.dumps({
            'action': 'client_key_event',
            'key': event['key']
        }))

    async def host_key_event(self, event):
        await self.send(text_data=json.dumps({
            'action': 'host_key_event',
            'key': event['key']
        }))

    async def game_ended_pong(self, event):
        await self.send(text_data=json.dumps({
            'action': 'game_ended_pong',
            'winner': event['winner']
        }))

    async def game_ended_pong_tournament(self, event):
        await self.send(text_data=json.dumps({
            'action': 'game_ended_pong_tournament',
            'winner': event['winner']
        }))

    async def player_scores_pong(self, event):
        await self.send(text_data=json.dumps({
            'action': 'update_player_scores_pong',
            'player1': event['player1'],
            'player2': event['player2']
        }))

    async def ball_position(self, event):
        await self.send(text_data=json.dumps({
            'action': 'update_ball_position_pong',
            'ball_x': event['ball_x'],
            'ball_y': event['ball_y']
        }))

    async def player_joined_pong(self, event):
        await self.send(text_data=json.dumps({
            'action': 'player_joined_pong',
            'room_id': event['room_id'],
            'guest_name': event['guest_name'],
            'message': f"{event['guest_name']} has joined the game."
        }))
        if GameRoomManagerPong.rooms[event['room_id']]['guest'] is not None:
            for i in range(5, 0, -1):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'game_countdown_pong',
                        'message': str(i)
                    }
                )
                await asyncio.sleep(1)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'start_game_pong',
                    'message': 'start'
                }
            )

    async def player_joined_pong_tournament(self, event):
        await self.send(text_data=json.dumps({
            'action': 'player_joined_pong_tournament',
            'room_id': event['room_id'],
            'guest_name': event['guest_name'],
            'message': f"{event['guest_name']} has joined the game."
        }))

    async def player_joined_memory(self, event):
        await self.send(text_data=json.dumps({
            'action': 'player_joined_memory',
            'room_id': event['room_id'],
            'guest_name': event['guest_name'],
            'message': f"{event['guest_name']} has joined the game."
        }))
        if GameRoomManagerMemory.rooms[event['room_id']]['guest'] is not None:
            for i in range(5, 0, -1):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'game_countdown_memory',
                        'message': str(i)
                    }
                )
                await asyncio.sleep(1)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'start_game_memory',
                    'message': 'start'
                }
            )

    async def game_countdown_pong(self, event):
        await self.send(text_data=json.dumps({
            'action': 'countdown_pong',
            'message': event['message']
        }))

    async def start_game_pong(self, event):
        await self.send(text_data=json.dumps({
            'action': 'start_game_pong',
            'message': 'Game Starting!'
        }))

    async def game_countdown_memory(self, event):
        await self.send(text_data=json.dumps({
            'action': 'countdown_memory',
            'message': event['message']
        }))

    async def start_game_memory(self, event):
        await self.send(text_data=json.dumps({
            'action': 'start_game_memory',
            'message': 'Game Starting!'
        }))
