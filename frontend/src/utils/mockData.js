const mockData = {
  bots: [
    {
      id: 1,
      name: "Bot Conservador",
      strategy: "Grid Trading",
      isActive: true,
      profit: 2450,
      roi: 12.3,
      accuracy: 87,
      risk: "Bajo"
    },
    {
      id: 2,
      name: "Bot Moderado",
      strategy: "DCA + RSI",
      isActive: true,
      profit: 3780,
      roi: 18.9,
      accuracy: 79,
      risk: "Medio"
    },
    {
      id: 3,
      name: "Bot Agresivo",
      strategy: "Momentum Trading",
      isActive: false,
      profit: -850,
      roi: -4.2,
      accuracy: 92,
      risk: "Alto"
    },
    {
      id: 4,
      name: "Scalping Bot",
      strategy: "High Frequency",
      isActive: true,
      profit: 1280,
      roi: 8.4,
      accuracy: 94,
      risk: "Medio"
    },
    {
      id: 5,
      name: "Arbitrage Bot",
      strategy: "Cross Exchange",
      isActive: true,
      profit: 567,
      roi: 3.2,
      accuracy: 96,
      risk: "Bajo"
    },
    {
      id: 6,
      name: "AI Predictor",
      strategy: "Machine Learning",
      isActive: false,
      profit: 4320,
      roi: 24.1,
      accuracy: 82,
      risk: "Alto"
    }
  ],
  
  portfolio: {
    balance: 47650,
    initialBalance: 40000,
    dailyProfit: 1235,
    dailyProfitPercentage: 2.68,
    accuracy: 86.7,
    totalTrades: 1247,
    successfulTrades: 1081
  },
  
  recentTrades: [
    {
      pair: "BTC/USDT",
      type: "BUY",
      amount: 0.025,
      price: 43250,
      profit: 125,
      time: "14:32:15"
    },
    {
      pair: "ETH/USDT", 
      type: "SELL",
      amount: 0.5,
      price: 2580,
      profit: 87,
      time: "14:28:42"
    },
    {
      pair: "ADA/USDT",
      type: "BUY", 
      amount: 1250,
      price: 0.485,
      profit: -12,
      time: "14:25:18"
    },
    {
      pair: "DOT/USDT",
      type: "SELL",
      amount: 45,
      price: 7.85,
      profit: 34,
      time: "14:21:09"
    },
    {
      pair: "BTC/USDT",
      type: "SELL",
      amount: 0.015,
      price: 43180,
      profit: 76,
      time: "14:18:55"
    },
    {
      pair: "ETH/USDT",
      type: "BUY",
      amount: 0.8,
      price: 2575,
      profit: 92,
      time: "14:15:23"
    }
  ],
  
  zaffexConnection: {
    isConnected: false,
    apiKey: "",
    lastSync: null,
    balance: 0,
    availableMarkets: []
  },
  
  tradingPairs: [
    { symbol: "BTC/USDT", price: 43250, change24h: 2.45, volume: "2.4B" },
    { symbol: "ETH/USDT", price: 2580, change24h: 1.89, volume: "1.8B" },
    { symbol: "ADA/USDT", price: 0.485, change24h: -0.87, volume: "456M" },
    { symbol: "DOT/USDT", price: 7.85, change24h: 3.21, volume: "234M" },
    { symbol: "MATIC/USDT", price: 0.92, change24h: -1.23, volume: "189M" },
    { symbol: "AVAX/USDT", price: 39.67, change24h: 4.56, volume: "178M" }
  ]
};

export default mockData;