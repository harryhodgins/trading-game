import { useState, useEffect } from "react";

export function useGameEngine(player) {
  const [round, setRound] = useState(1);
  const [currentPrice, setCurrentPrice] = useState(100.0);
  const [signal, setSignal] = useState(null);
  const [timeLeft, setTimeLeft] = useState(10);
  const [phase, setPhase] = useState("trading"); // 'trading' or 'reveal'

  const startTimer = () => {
    const interval = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return interval;
  };

  const generateSignal = () => {
    const upChance = Math.floor(Math.random() * 99) + 1;
    const downChance = 100 - upChance;
    const upAmount = Math.floor(Math.random() * 11);
    const downAmount = Math.floor(Math.random() * 11);

    setSignal({
      upChance,
      downChance,
      upAmount,
      downAmount,
    });
  };

  const resolveRound = () => {
    if (!signal) return;

    const roll = Math.random() * 100;
    if (roll < signal.upChance) {
      setCurrentPrice(currentPrice + signal.upAmount);
    } else {
      setCurrentPrice(currentPrice - signal.downAmount);
    }
    setPhase("reveal");
  };

  useEffect(() => {
    if(!player) return
    generateSignal();
    startTimer();
  }, [player]);

  useEffect(() => {
    if (!player) return
    if (timeLeft === 0) {
      resolveRound();
    }
  }, [timeLeft]);

  useEffect(() => {
    if (!player) return
    if (phase === "reveal") {
      const timeout = setTimeout(() => {
        setTimeLeft(10);
        generateSignal();
        setRound((prev) => prev + 1);
        setPhase("trading");

        const interval = startTimer();
      }, 3000);

      return () => clearTimeout(timeout); // cleanup
    }
  }, [phase]);

  return {
    round,
    currentPrice,
    signal,
    timeLeft,
    phase,
    generateSignal,
    resolveRound,
  };
}
