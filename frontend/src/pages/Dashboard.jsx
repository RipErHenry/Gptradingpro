import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Progress } from '../components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  Bot, 
  Activity, 
  BarChart3,
  Play,
  Pause,
  Settings,
  RefreshCw
} from 'lucide-react';
import mockData from '../utils/mockData';

const Dashboard = () => {
  const [bots, setBots] = useState(mockData.bots);
  const [portfolio, setPortfolio] = useState(mockData.portfolio);
  const [trades, setTrades] = useState(mockData.recentTrades);

  const totalProfit = portfolio.balance - portfolio.initialBalance;
  const profitPercentage = ((totalProfit / portfolio.initialBalance) * 100).toFixed(2);

  const toggleBot = (botId) => {
    setBots(prev => prev.map(bot => 
      bot.id === botId ? { ...bot, isActive: !bot.isActive } : bot
    ));
  };

  return (
    <div className="min-h-screen bg-gray-900 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-white">Dashboard</h1>
            <p className="text-gray-400">Monitorea tus bots y ganancias en tiempo real</p>
          </div>
          <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
            <RefreshCw className="w-4 h-4 mr-2" />
            Actualizar
          </Button>
        </div>

        {/* Portfolio Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card className="bg-gray-800 border-gray-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-400">Balance Total</CardTitle>
              <DollarSign className="h-4 w-4 text-gray-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-white">${portfolio.balance.toLocaleString()}</div>
              <p className="text-xs text-gray-400">
                +${(portfolio.balance - portfolio.initialBalance).toLocaleString()} desde inicio
              </p>
            </CardContent>
          </Card>

          <Card className="bg-gray-800 border-gray-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-400">Ganancia Hoy</CardTitle>
              <TrendingUp className="h-4 w-4 text-green-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-400">+${portfolio.dailyProfit.toLocaleString()}</div>
              <p className="text-xs text-gray-400">
                +{portfolio.dailyProfitPercentage}% en las últimas 24h
              </p>
            </CardContent>
          </Card>

          <Card className="bg-gray-800 border-gray-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-400">Bots Activos</CardTitle>
              <Bot className="h-4 w-4 text-blue-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-white">
                {bots.filter(bot => bot.isActive).length}/{bots.length}
              </div>
              <p className="text-xs text-gray-400">
                {bots.filter(bot => bot.isActive).length} bots operando
              </p>
            </CardContent>
          </Card>

          <Card className="bg-gray-800 border-gray-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-400">Precisión</CardTitle>
              <Activity className="h-4 w-4 text-purple-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-white">{portfolio.accuracy}%</div>
              <p className="text-xs text-gray-400">
                Promedio de operaciones exitosas
              </p>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="bots" className="space-y-4">
          <TabsList className="grid w-full grid-cols-3 bg-gray-800">
            <TabsTrigger value="bots">Trading Bots</TabsTrigger>
            <TabsTrigger value="trades">Operaciones</TabsTrigger>
            <TabsTrigger value="analytics">Análisis</TabsTrigger>
          </TabsList>

          <TabsContent value="bots" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {bots.map((bot) => (
                <Card key={bot.id} className="bg-gray-800 border-gray-700">
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-white text-lg">{bot.name}</CardTitle>
                        <CardDescription className="text-gray-400">{bot.strategy}</CardDescription>
                      </div>
                      <Badge 
                        variant={bot.isActive ? "default" : "secondary"}
                        className={bot.isActive ? "bg-green-600" : "bg-gray-600"}
                      >
                        {bot.isActive ? 'Activo' : 'Inactivo'}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-400">Ganancia:</span>
                      <span className={`font-bold ${bot.profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {bot.profit >= 0 ? '+' : ''}${bot.profit.toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-400">ROI:</span>
                      <span className={`font-bold ${bot.roi >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {bot.roi >= 0 ? '+' : ''}{bot.roi}%
                      </span>
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-400">Precisión:</span>
                        <span className="text-white">{bot.accuracy}%</span>
                      </div>
                      <Progress value={bot.accuracy} className="h-2" />
                    </div>
                    <div className="flex gap-2">
                      <Button 
                        size="sm" 
                        onClick={() => toggleBot(bot.id)}
                        className={bot.isActive ? "bg-red-600 hover:bg-red-700" : "bg-green-600 hover:bg-green-700"}
                      >
                        {bot.isActive ? <Pause className="w-4 h-4 mr-1" /> : <Play className="w-4 h-4 mr-1" />}
                        {bot.isActive ? 'Pausar' : 'Iniciar'}
                      </Button>
                      <Button size="sm" variant="outline" className="border-gray-600">
                        <Settings className="w-4 h-4" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="trades" className="space-y-4">
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white">Operaciones Recientes</CardTitle>
                <CardDescription className="text-gray-400">
                  Historial de las últimas operaciones realizadas
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {trades.map((trade, index) => (
                    <div key={index} className="flex items-center justify-between p-4 rounded-lg bg-gray-700/50">
                      <div className="flex items-center space-x-4">
                        <div className={`w-3 h-3 rounded-full ${trade.type === 'BUY' ? 'bg-green-400' : 'bg-red-400'}`}></div>
                        <div>
                          <div className="text-white font-medium">{trade.pair}</div>
                          <div className="text-gray-400 text-sm">{trade.time}</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-white font-medium">{trade.amount} {trade.pair.split('/')[0]}</div>
                        <div className={`text-sm ${trade.profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {trade.profit >= 0 ? '+' : ''}${trade.profit}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-4">
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white">Análisis de Rendimiento</CardTitle>
                <CardDescription className="text-gray-400">
                  Métricas detalladas de tus estrategias de trading
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <h4 className="text-lg font-semibold text-white">Rendimiento por Estrategia</h4>
                    {['Conservador', 'Moderado', 'Agresivo'].map((strategy, index) => (
                      <div key={strategy} className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-400">{strategy}</span>
                          <span className="text-white">{[85, 78, 92][index]}%</span>
                        </div>
                        <Progress value={[85, 78, 92][index]} className="h-2" />
                      </div>
                    ))}
                  </div>
                  <div className="space-y-4">
                    <h4 className="text-lg font-semibold text-white">Distribución de Activos</h4>
                    <div className="space-y-3">
                      {[
                        { asset: 'BTC/USDT', percentage: 45, color: 'bg-orange-500' },
                        { asset: 'ETH/USDT', percentage: 30, color: 'bg-blue-500' },
                        { asset: 'ADA/USDT', percentage: 15, color: 'bg-green-500' },
                        { asset: 'DOT/USDT', percentage: 10, color: 'bg-purple-500' }
                      ].map(({ asset, percentage, color }) => (
                        <div key={asset} className="flex items-center space-x-3">
                          <div className={`w-3 h-3 rounded-full ${color}`}></div>
                          <span className="text-gray-400 flex-1">{asset}</span>
                          <span className="text-white">{percentage}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Dashboard;