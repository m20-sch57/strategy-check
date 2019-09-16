#print("s")
import sys
import importlib

sys.stderr.write("spam\n")

strategyPath, gameModule, GameStr, PlayerIdStr = input(), input(), input(), input()

#print("p")

game = importlib.import_module(gameModule)
strategy = importlib.import_module(strategyPath)
#print("i")

gameState = game.GameState()
gameState.fromString(GameStr)
#print("cg")

playerId = str(PlayerIdStr)
#print("ci")

turn = strategy.Strategy(game, gameState, int(playerId))
#if type(turn) != classes.Turn:
#    raise TypeError("Invalid Type")
#print("r")

try:
    ans = turn.toString()
except:
    sys.exit(57)
print(ans)
#print("e")

sys.stderr.write("finished\n")

