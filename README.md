
<div align="center"> 
  <h3 align="center">Online Battleship ⚓</h3>
  <p>
    A real-time multiplayer mobile battleship game built with Python Flask-SocketIO backend and Kotlin frontend.
  </p>
</div>

## 📝 About The Project
This is an online mobile game that supports real-time multiplayer gameplay. Players can connect from their mobile devices and interact with each other in real-time through WebSocket connections.

Screenshot from game:

![image](https://github.com/user-attachments/assets/bd25cd52-ebc1-47f3-a9af-0bbd323850bc)
![image](https://github.com/user-attachments/assets/5cc188c3-db27-421c-a4d9-63912ef1e729)
![image](https://github.com/user-attachments/assets/2660062e-a2f5-445c-9e1c-d89d0d2d2193)
![image](https://github.com/user-attachments/assets/e083cbc1-7a48-42bc-9a2f-e1101ce44281)

### 🛠️ Tech Stack
- Backend: Python
- Frontend: Kotlin
- Web Framework: Flask
- Real-time Communication: Flask-SocketIO
- WebSocket: Socket.IO
  
### 🔌 WebSocket Events

[Event diagram](./event_map.pdf)


**Connection Events**

- `connect` - Player joins the server
- `disconnect` - Player leaves the server
- `check_room_to_join` - Join or create a game room

**Game Events**

- `ready_to_start` - Start multiplayer game
- `ready_to_start_bot` - Start game with AI opponent
- `place_ship` - Place ships on board
- `shoot` - Attack opponent (multiplayer)
- `shoot_bot` - Attack AI opponent

**Server Responses**

- `room_status` - Room join/status updates
- `placeShip` - Begin ship placement phase
- `start` - Game begins
- `turn` - Current player's turn
- `update_context` - Shot result and board updates
- `end_game` - Game over with win/loss status
### 📂 Project Structure
```
├── app.py                 # Main Flask-SocketIO server
├── entities/              # Game entities and logic
│   ├── __init__.py       # Package initialization
│   ├── ai_player.py      # AI player implementation
│   ├── battleship.py     # Main game logic
│   ├── board.py          # Game board management
│   ├── direction.py      # Ship direction enum
│   ├── game.py           # Base game class
│   ├── player.py         # Base player class
│   ├── player_user.py    # Human player wrapper
│   ├── room.py           # Game room management
│   ├── server.py         # Server state management
│   ├── ship.py           # Ship entity
│   └── user.py           # User entity
├── requirements.txt       # Python dependencies
└── .gitignore          
```
## 🚀 Getting Started
### Prerequisites

Before running this project, make sure you have:

- Python 3.8 or +
- pip
- Git

### Installation 
**Backend Setup**
1. Clone the repository
```bash
git clone https://github.com/nptchiko/Online-Battleship
cd Online-Battleship
```
2. Create virtual environment
```bash
python -m venv env

# On Linux:
source env/bin/activate

# On Windows:
env\Scripts\activate
```
3. Install dependencies
```python
pip install -r requirements.txt
```
5. Run the server
```python
python app.py `
```
The server will start on ```http://localhost:5000```

**Frontend setup**
...
<!-- USAGE EXAMPLES -->
## Usage



<!-- CONTACT -->
## 📞 Contact

Nguyen Phuoc Tien - [tiennguyenn04.dev@gmail.com](mailto:tiennguyenn04.dev@gmail.com)

Project Link: [https://github.com/nptchiko/Online-Battleship](https://github.com/nptchiko/Online-Battleship)
