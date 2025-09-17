import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Progress } from '../components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Slider } from '../components/ui/slider';
import { 
  Bot, 
  Plus, 
  Play, 
  Pause, 
  Settings, 
  TrendingUp, 
  TrendingDown, 
  BarChart3,
  AlertTriangle
} from 'lucide-react';
import mockData from '../utils/mockData';

const Bots = () => {
  const [bots, setBots] = useState(mockData.bots);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [newBot, setNewBot] = useState({
    name: '',
    strategy: '',
    risk: 'Medio',
    investment: 1000
  });

  const toggleBot = (botId) => {
    setBots(prev => prev.map(bot => 
      bot.id === botId ? { ...bot, isActive: !bot.isActive } : bot
    ));
  };

  const createBot = () => {
    const bot = {
      id: Date.now(),
      name: newBot.name,
      strategy: newBot.strategy,
      isActive: false,
      profit: 0,
      roi: 0,
      accuracy: 0,
      risk: newBot.risk
    };
    setBots(prev => [...prev, bot]);
    setNewBot({ name: '', strategy: '', risk: 'Medio', investment: 1000 });
    setIsCreateDialogOpen(false);
  };

  const strategies = [
    { id: 'grid', name: 'Grid Trading', description: 'Operaciones automáticas en rangos definidos' },
    { id: 'dca', name: 'DCA + RSI', description: 'Promedio de costo con indicadores técnicos' },
    { id: 'momentum', name: 'Momentum Trading', description: 'Seguimiento de tendencias fuertes' },
    { id: 'scalping', name: 'High Frequency', description: 'Múltiples operaciones de corto plazo' },
    { id: 'arbitrage', name: 'Cross Exchange', description: 'Aprovecha diferencias de precio entre exchanges' },
    { id: 'ai', name: 'Machine Learning', description: 'Predicciones basadas en inteligencia artificial' }
  ];

  return (
    <div className="min-h-screen bg-gray-900 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-white">Trading Bots</h1>
            <p className="text-gray-400">Gestiona y configura tus bots de trading automatizado</p>
          </div>
          
          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                <Plus className="w-4 h-4 mr-2" />
                Crear Bot
              </Button>
            </DialogTrigger>
            <DialogContent className="bg-gray-800 border-gray-700">
              <DialogHeader>
                <DialogTitle className="text-white">Crear Nuevo Bot</DialogTitle>
                <DialogDescription className="text-gray-400">
                  Configura un nuevo bot de trading con tus preferencias
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-4 py-4">
                <div>
                  <Label htmlFor="name" className="text-gray-300">Nombre del Bot</Label>
                  <Input
                    id="name"
                    value={newBot.name}
                    onChange={(e) => setNewBot(prev => ({ ...prev, name: e.target.value }))}
                    placeholder="Mi Bot de Trading"
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                </div>
                
                <div>
                  <Label className="text-gray-300">Estrategia</Label>
                  <Select value={newBot.strategy} onValueChange={(value) => setNewBot(prev => ({ ...prev, strategy: value }))}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                      <SelectValue placeholder="Selecciona una estrategia" />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-700 border-gray-600">
                      {strategies.map((strategy) => (
                        <SelectItem key={strategy.id} value={strategy.name} className="text-white">
                          {strategy.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <Label className="text-gray-300">Nivel de Riesgo</Label>
                  <Select value={newBot.risk} onValueChange={(value) => setNewBot(prev => ({ ...prev, risk: value }))}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-700 border-gray-600">
                      <SelectItem value="Bajo" className="text-white">Bajo - Operaciones conservadoras</SelectItem>
                      <SelectItem value="Medio" className="text-white">Medio - Balance riesgo/ganancia</SelectItem>
                      <SelectItem value="Alto" className="text-white">Alto - Máxima rentabilidad</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <Label className="text-gray-300">Inversión Inicial: ${newBot.investment}</Label>
                  <Slider
                    value={[newBot.investment]}
                    onValueChange={([value]) => setNewBot(prev => ({ ...prev, investment: value }))}
                    max={10000}
                    min={100}
                    step={100}
                    className="mt-2"
                  />
                </div>
              </div>
              
              <div className="flex justify-end space-x-2">
                <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)} className="border-gray-600 text-gray-300">
                  Cancelar
                </Button>
                <Button 
                  onClick={createBot}
                  disabled={!newBot.name || !newBot.strategy}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                >
                  Crear Bot
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-6">
              <div className="flex items-center space-x-2">
                <Bot className="w-5 h-5 text-blue-400" />
                <span className="text-gray-400 text-sm">Total Bots</span>
              </div>
              <div className="text-2xl font-bold text-white mt-2">{bots.length}</div>
            </CardContent>
          </Card>
          
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-6">
              <div className="flex items-center space-x-2">
                <Play className="w-5 h-5 text-green-400" />
                <span className="text-gray-400 text-sm">Activos</span>
              </div>
              <div className="text-2xl font-bold text-white mt-2">
                {bots.filter(bot => bot.isActive).length}
              </div>
            </CardContent>
          </Card>
          
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-6">
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-5 h-5 text-green-400" />
                <span className="text-gray-400 text-sm">Ganancia Total</span>
              </div>
              <div className="text-2xl font-bold text-green-400 mt-2">
                +${bots.reduce((sum, bot) => sum + Math.max(0, bot.profit), 0).toLocaleString()}
              </div>
            </CardContent>
          </Card>
          
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-6">
              <div className="flex items-center space-x-2">
                <BarChart3 className="w-5 h-5 text-purple-400" />
                <span className="text-gray-400 text-sm">ROI Promedio</span>
              </div>
              <div className="text-2xl font-bold text-white mt-2">
                {(bots.reduce((sum, bot) => sum + bot.roi, 0) / bots.length).toFixed(1)}%
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Bots Grid */}
        <Tabs defaultValue="all" className="space-y-4">
          <TabsList className="grid w-full grid-cols-4 bg-gray-800">
            <TabsTrigger value="all">Todos ({bots.length})</TabsTrigger>
            <TabsTrigger value="active">Activos ({bots.filter(bot => bot.isActive).length})</TabsTrigger>
            <TabsTrigger value="profitable">Rentables ({bots.filter(bot => bot.profit > 0).length})</TabsTrigger>
            <TabsTrigger value="strategies">Estrategias</TabsTrigger>
          </TabsList>

          <TabsContent value="all" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {bots.map((bot) => (
                <Card key={bot.id} className="bg-gray-800 border-gray-700 hover:border-blue-500/50 transition-colors">
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-white text-lg flex items-center space-x-2">
                          <Bot className="w-5 h-5" />
                          <span>{bot.name}</span>
                        </CardTitle>
                        <CardDescription className="text-gray-400 mt-1">{bot.strategy}</CardDescription>
                      </div>
                      <Badge 
                        variant={bot.isActive ? "default" : "secondary"}
                        className={`${bot.isActive ? "bg-green-600" : "bg-gray-600"} ${
                          bot.risk === 'Alto' ? 'border-red-500/50' : 
                          bot.risk === 'Medio' ? 'border-yellow-500/50' : 
                          'border-green-500/50'
                        }`}
                      >
                        {bot.isActive ? 'Activo' : 'Inactivo'}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <div className="text-xs text-gray-400 mb-1">Ganancia</div>
                        <div className={`font-bold text-lg ${bot.profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {bot.profit >= 0 ? '+' : ''}${bot.profit.toLocaleString()}
                        </div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-400 mb-1">ROI</div>
                        <div className={`font-bold text-lg ${bot.roi >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {bot.roi >= 0 ? '+' : ''}{bot.roi}%
                        </div>
                      </div>
                    </div>
                    
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-gray-400">Precisión</span>
                        <span className="text-white">{bot.accuracy}%</span>
                      </div>
                      <Progress value={bot.accuracy} className="h-2" />
                    </div>
                    
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">Riesgo:</span>
                      <Badge 
                        variant="outline" 
                        className={`text-xs ${
                          bot.risk === 'Alto' ? 'border-red-500 text-red-400' :
                          bot.risk === 'Medio' ? 'border-yellow-500 text-yellow-400' :
                          'border-green-500 text-green-400'
                        }`}
                      >
                        {bot.risk}
                      </Badge>
                    </div>
                    
                    <div className="flex gap-2">
                      <Button 
                        size="sm" 
                        onClick={() => toggleBot(bot.id)}
                        className={`flex-1 ${bot.isActive ? "bg-red-600 hover:bg-red-700" : "bg-green-600 hover:bg-green-700"}`}
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

          <TabsContent value="active">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {bots.filter(bot => bot.isActive).map((bot) => (
                <Card key={bot.id} className="bg-gray-800 border-gray-700 border-green-500/30">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-white">{bot.name}</h3>
                      <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                    </div>
                    <p className="text-gray-400 text-sm mb-2">{bot.strategy}</p>
                    <div className="text-2xl font-bold text-green-400">
                      +${bot.profit.toLocaleString()}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="profitable">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {bots.filter(bot => bot.profit > 0).map((bot) => (
                <Card key={bot.id} className="bg-gray-800 border-gray-700 border-green-500/30">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-white">{bot.name}</h3>
                      <TrendingUp className="w-5 h-5 text-green-400" />
                    </div>
                    <p className="text-gray-400 text-sm mb-2">ROI: +{bot.roi}%</p>
                    <div className="text-2xl font-bold text-green-400">
                      +${bot.profit.toLocaleString()}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="strategies">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {strategies.map((strategy) => (
                <Card key={strategy.id} className="bg-gray-800 border-gray-700 hover:border-blue-500/50 transition-colors cursor-pointer">
                  <CardHeader>
                    <CardTitle className="text-white">{strategy.name}</CardTitle>
                    <CardDescription className="text-gray-400">{strategy.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400 text-sm">
                        {bots.filter(bot => bot.strategy === strategy.name).length} bots usando
                      </span>
                      <Button size="sm" variant="outline" className="border-gray-600 text-gray-300">
                        Usar Estrategia
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Bots;