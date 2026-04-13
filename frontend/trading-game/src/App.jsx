import { useState, useEffect } from "react";
import "./App.css";
import { useGameEngine } from "./useGameEngine";

function App() {
  const [player, setPlayer] = useState(null);
  const [playerId, setPlayerId] = useState("");
  const [quantity, setQuantity] = useState("");
  const [players, setPlayers] = useState([]);
  const [newPlayerName, setNewPlayerName] = useState("");
  const [newPlayerBalance, setNewPlayerBalance] = useState(10000);

  const { round, currentPrice, signal, timeLeft, phase } =
    useGameEngine(player);

  const fetchPlayer = async (player_id) => {
    const response = await fetch(`http://localhost:8000/players/${player_id}`);
    const data = await response.json();
    setPlayer(data);
  };

  const fetchAllPlayers = async () => {
    const response = await fetch(`http://localhost:8000/players`);
    if (response.ok) {
      const data = await response.json();
      setPlayers(data);
    }
  };

  const createPlayer = async () => {
    if (!newPlayerName) return;
    const response = await fetch(
      `http://localhost:8000/players?playerName=${newPlayerName}&balance=${newPlayerBalance}`,
      { method: "POST" },
    );
    if (response.ok) {
      const allPlayers = await fetch(`http://localhost:8000/players`);
      const data = await allPlayers.json();
      const created = data.find((p) => p.player_name === newPlayerName);
      if (created) fetchPlayer(created.player_id);
    }
  };

  const placeOrder = async (quantity, type) => {
    if (!player) return;
    const response = await fetch(
      `http://localhost:8000/orders?ticker=DUMMY_STOCK&quantity=${quantity}&type=${type}&player_id=${player.player_id}&price=${currentPrice}`,
      { method: "POST" },
    );
    const data = await response.json();
    fetchPlayer(player.player_id);
  };

  useEffect(() => {
    if (!player) fetchAllPlayers();
  }, [player]);

  return (
    <>
      <h1>Trading Game</h1>

      {player === null ? (
        <div className="login-screen">
          <div className="existing-players">
            <h2>Select Player</h2>
            {players.length === 0 && <p>No players yet</p>}
            {players.map((p) => (
              <div
                key={p.player_id}
                className="player-row"
                onClick={() => fetchPlayer(p.player_id)}
              >
                <span>{p.player_name}</span>
                <span className="bal">${Number(p.balance).toFixed(2)}</span>
              </div>
            ))}
          </div>

          <div className="create-player">
            <h2>Create New Player</h2>
            <input
              placeholder="Name"
              value={newPlayerName}
              onChange={(e) => setNewPlayerName(e.target.value)}
            />
            <input
              type="number"
              placeholder="Starting balance"
              value={newPlayerBalance}
              onChange={(e) => setNewPlayerBalance(e.target.value)}
            />
            <button className="btn-create" onClick={createPlayer}>Create & Play</button>
          </div>
        </div>
      ) : (
        <div>
          <p>Balance: ${player.balance}</p>
          <p>Round {round}</p>
          <p>Current Price: ${currentPrice}</p>
          {signal && (
            <p>
              Signal: {signal.upChance}% chance of +${signal.upAmount},{" "}
              {signal.downChance}% chance of -${signal.downAmount}
            </p>
          )}
          <p>Time Left: {timeLeft}</p>
          <input
            type="number"
            value={quantity || ""}
            onChange={(e) => setQuantity(e.target.value)}
          />
          <button onClick={() => placeOrder(quantity, "BUY")}>BUY</button>
          <button onClick={() => placeOrder(quantity, "SELL")}>SELL</button>
        </div>
      )}
    </>
  );
}

export default App;
