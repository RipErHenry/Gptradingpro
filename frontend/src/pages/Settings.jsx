import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Switch } from '../components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Badge } from '../components/ui/badge';
import { Alert, AlertDescription } from '../components/ui/alert';
import { 
  Link2, 
  Shield, 
  Bell, 
  User, 
  Zap, 
  AlertTriangle, 
  Check,
  Copy,
  Eye,
  EyeOff
} from 'lucide-react';
import { useToast } from '../hooks/use-toast';

const Settings = () => {
  const [zaffexConfig, setZaffexConfig] = useState({
    apiKey: '',
    apiSecret: '',
    isConnected: false,
    testMode: true
  });
  const [showSecrets, setShowSecrets] = useState(false);
  const [notifications, setNotifications] = useState({
    trades: true,
    profits: true,
    losses: true,
    botStatus: true,
    email: false,
    telegram: false
  });
  const { toast } = useToast();

  const connectZaffex = async () => {
    if (!zaffexConfig.apiKey || !zaffexConfig.apiSecret) {
      toast({
        title: "Error",
        description: "Por favor, ingresa tu API Key y Secret de Zaffex",
        variant: "destructive"
      });
      return;
    }

    // Simulamos conexión a Zaffex
    setTimeout(() => {
      setZaffexConfig(prev => ({ ...prev, isConnected: true }));
      toast({
        title: "¡Conexión exitosa!",
        description: "Tu cuenta de Zaffex ha sido conectada correctamente",
      });
    }, 2000);
  };

  const disconnectZaffex = () => {
    setZaffexConfig(prev => ({ 
      ...prev, 
      isConnected: false,
      apiKey: '',
      apiSecret: ''
    }));
    toast({
      title: "Desconectado",
      description: "Tu cuenta de Zaffex ha sido desconectada",
    });
  };

  const copyApiKey = () => {
    navigator.clipboard.writeText(zaffexConfig.apiKey);
    toast({
      title: "Copiado",
      description: "API Key copiada al portapapeles",
    });
  };

  return (
    <div className="min-h-screen bg-gray-900 p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-white">Configuración</h1>
          <p className="text-gray-400">Administra tu cuenta y configuraciones de trading</p>
        </div>

        <Tabs defaultValue="zaffex" className="space-y-4">
          <TabsList className="grid w-full grid-cols-4 bg-gray-800">
            <TabsTrigger value="zaffex">Zaffex API</TabsTrigger>
            <TabsTrigger value="notifications">Notificaciones</TabsTrigger>
            <TabsTrigger value="security">Seguridad</TabsTrigger>
            <TabsTrigger value="profile">Perfil</TabsTrigger>
          </TabsList>

          {/* Zaffex Configuration */}
          <TabsContent value="zaffex" className="space-y-4">
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <Link2 className="w-5 h-5 text-blue-400" />
                  <CardTitle className="text-white">Conexión con Zaffex</CardTitle>
                </div>
                <CardDescription className="text-gray-400">
                  Conecta tu cuenta de Zaffex para habilitar el trading automatizado
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {!zaffexConfig.isConnected ? (
                  <>
                    <Alert className="border-orange-500/50 bg-orange-500/10">
                      <AlertTriangle className="h-4 w-4 text-orange-400" />
                      <AlertDescription className="text-orange-300">
                        Necesitas crear tokens API en tu cuenta de Zaffex. Ve a: Configuración → API → Crear Nueva Clave
                      </AlertDescription>
                    </Alert>
                    
                    <div className="space-y-4">
                      <div>
                        <Label htmlFor="apiKey" className="text-gray-300">API Key</Label>
                        <Input
                          id="apiKey"
                          type={showSecrets ? "text" : "password"}
                          value={zaffexConfig.apiKey}
                          onChange={(e) => setZaffexConfig(prev => ({ ...prev, apiKey: e.target.value }))}
                          placeholder="Tu API Key de Zaffex"
                          className="bg-gray-700 border-gray-600 text-white mt-1"
                        />
                      </div>
                      
                      <div>
                        <Label htmlFor="apiSecret" className="text-gray-300">API Secret</Label>
                        <Input
                          id="apiSecret"
                          type={showSecrets ? "text" : "password"}
                          value={zaffexConfig.apiSecret}
                          onChange={(e) => setZaffexConfig(prev => ({ ...prev, apiSecret: e.target.value }))}
                          placeholder="Tu API Secret de Zaffex"
                          className="bg-gray-700 border-gray-600 text-white mt-1"
                        />
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <Switch
                          checked={showSecrets}
                          onCheckedChange={setShowSecrets}
                        />
                        <Label className="text-gray-300">Mostrar claves</Label>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <Switch
                          checked={zaffexConfig.testMode}
                          onCheckedChange={(checked) => setZaffexConfig(prev => ({ ...prev, testMode: checked }))}
                        />
                        <Label className="text-gray-300">Modo de prueba (recomendado)</Label>
                      </div>
                    </div>
                    
                    <Button 
                      onClick={connectZaffex}
                      className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                    >
                      <Link2 className="w-4 h-4 mr-2" />
                      Conectar con Zaffex
                    </Button>
                  </>
                ) : (
                  <div className="space-y-4">
                    <Alert className="border-green-500/50 bg-green-500/10">
                      <Check className="h-4 w-4 text-green-400" />
                      <AlertDescription className="text-green-300">
                        ¡Conexión exitosa! Tu cuenta de Zaffex está conectada y lista para el trading automatizado.
                      </AlertDescription>
                    </Alert>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label className="text-gray-300">Estado de la Conexión</Label>
                        <div className="flex items-center space-x-2">
                          <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                          <Badge className="bg-green-600">Conectado</Badge>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <Label className="text-gray-300">Modo</Label>
                        <Badge variant="outline" className="border-orange-500 text-orange-400">
                          {zaffexConfig.testMode ? 'Prueba' : 'Producción'}
                        </Badge>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Label className="text-gray-300">API Key (últimos 4 dígitos)</Label>
                      <div className="flex items-center space-x-2">
                        <Input 
                          value={`****-****-****-${zaffexConfig.apiKey.slice(-4)}`}
                          readOnly
                          className="bg-gray-700 border-gray-600 text-gray-400"
                        />
                        <Button size="sm" variant="outline" onClick={copyApiKey} className="border-gray-600">
                          <Copy className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                    
                    <Button 
                      variant="outline" 
                      onClick={disconnectZaffex}
                      className="border-red-500 text-red-400 hover:bg-red-500/10"
                    >
                      Desconectar Cuenta
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
            
            {/* Balance Information */}
            {zaffexConfig.isConnected && (
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white">Información de la Cuenta</CardTitle>
                  <CardDescription className="text-gray-400">
                    Datos de tu cuenta de Zaffex
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center p-4 bg-gray-700/50 rounded-lg">
                      <div className="text-2xl font-bold text-white">$12,450</div>
                      <div className="text-gray-400 text-sm">Balance Total</div>
                    </div>
                    <div className="text-center p-4 bg-gray-700/50 rounded-lg">
                      <div className="text-2xl font-bold text-green-400">$8,320</div>
                      <div className="text-gray-400 text-sm">Disponible</div>
                    </div>
                    <div className="text-center p-4 bg-gray-700/50 rounded-lg">
                      <div className="text-2xl font-bold text-orange-400">$4,130</div>
                      <div className="text-gray-400 text-sm">En Operaciones</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Notifications */}
          <TabsContent value="notifications" className="space-y-4">
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <Bell className="w-5 h-5 text-purple-400" />
                  <CardTitle className="text-white">Notificaciones</CardTitle>
                </div>
                <CardDescription className="text-gray-400">
                  Configura cómo quieres recibir alertas sobre tu trading
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-4">
                  <h4 className="text-lg font-semibold text-white">Alertas de Trading</h4>
                  
                  {[
                    { key: 'trades', label: 'Nuevas operaciones', desc: 'Te notificamos cuando se ejecute una operación' },
                    { key: 'profits', label: 'Ganancias', desc: 'Alertas cuando tus bots generen ganancias' },
                    { key: 'losses', label: 'Pérdidas', desc: 'Notificación de operaciones con pérdidas' },
                    { key: 'botStatus', label: 'Estado de bots', desc: 'Cuando un bot se active o desactive' }
                  ].map(({ key, label, desc }) => (
                    <div key={key} className="flex items-center justify-between p-4 bg-gray-700/30 rounded-lg">
                      <div>
                        <div className="text-white font-medium">{label}</div>
                        <div className="text-gray-400 text-sm">{desc}</div>
                      </div>
                      <Switch
                        checked={notifications[key]}
                        onCheckedChange={(checked) => 
                          setNotifications(prev => ({ ...prev, [key]: checked }))
                        }
                      />
                    </div>
                  ))}
                </div>
                
                <div className="space-y-4">
                  <h4 className="text-lg font-semibold text-white">Canales de Notificación</h4>
                  
                  <div className="flex items-center justify-between p-4 bg-gray-700/30 rounded-lg">
                    <div>
                      <div className="text-white font-medium">Notificaciones por Email</div>
                      <div className="text-gray-400 text-sm">Recibe resúmenes diarios por correo</div>
                    </div>
                    <Switch
                      checked={notifications.email}
                      onCheckedChange={(checked) => 
                        setNotifications(prev => ({ ...prev, email: checked }))
                      }
                    />
                  </div>
                  
                  <div className="flex items-center justify-between p-4 bg-gray-700/30 rounded-lg">
                    <div>
                      <div className="text-white font-medium">Telegram Bot</div>
                      <div className="text-gray-400 text-sm">Alertas instantáneas en Telegram</div>
                    </div>
                    <Switch
                      checked={notifications.telegram}
                      onCheckedChange={(checked) => 
                        setNotifications(prev => ({ ...prev, telegram: checked }))
                      }
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Security */}
          <TabsContent value="security" className="space-y-4">
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <Shield className="w-5 h-5 text-green-400" />
                  <CardTitle className="text-white">Seguridad</CardTitle>
                </div>
                <CardDescription className="text-gray-400">
                  Protege tu cuenta y configura medidas de seguridad
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-4">
                  <div className="p-4 bg-gray-700/30 rounded-lg">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-white font-medium">Autenticación de dos factores (2FA)</div>
                        <div className="text-gray-400 text-sm">Protección adicional para tu cuenta</div>
                      </div>
                      <Badge className="bg-red-600">Desactivado</Badge>
                    </div>
                    <Button className="mt-3 bg-green-600 hover:bg-green-700">
                      Activar 2FA
                    </Button>
                  </div>
                  
                  <div className="p-4 bg-gray-700/30 rounded-lg">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <div className="text-white font-medium">Límites de trading</div>
                        <div className="text-gray-400 text-sm">Establece límites máximos por operación</div>
                      </div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label className="text-gray-300">Límite por operación ($)</Label>
                        <Input 
                          type="number" 
                          defaultValue="1000"
                          className="bg-gray-700 border-gray-600 text-white mt-1"
                        />
                      </div>
                      <div>
                        <Label className="text-gray-300">Límite diario ($)</Label>
                        <Input 
                          type="number" 
                          defaultValue="10000"
                          className="bg-gray-700 border-gray-600 text-white mt-1"
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div className="p-4 bg-gray-700/30 rounded-lg">
                    <div className="text-white font-medium mb-2">Cambiar contraseña</div>
                    <div className="space-y-3">
                      <Input 
                        type="password" 
                        placeholder="Contraseña actual"
                        className="bg-gray-700 border-gray-600 text-white"
                      />
                      <Input 
                        type="password" 
                        placeholder="Nueva contraseña"
                        className="bg-gray-700 border-gray-600 text-white"
                      />
                      <Input 
                        type="password" 
                        placeholder="Confirmar nueva contraseña"
                        className="bg-gray-700 border-gray-600 text-white"
                      />
                      <Button className="bg-blue-600 hover:bg-blue-700">
                        Actualizar Contraseña
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Profile */}
          <TabsContent value="profile" className="space-y-4">
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <User className="w-5 h-5 text-blue-400" />
                  <CardTitle className="text-white">Perfil de Usuario</CardTitle>
                </div>
                <CardDescription className="text-gray-400">
                  Administra tu información personal
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex items-center space-x-4">
                  <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                    <span className="text-2xl font-bold text-white">U</span>
                  </div>
                  <div>
                    <Button variant="outline" className="border-gray-600">
                      Cambiar Avatar
                    </Button>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label className="text-gray-300">Nombre</Label>
                    <Input 
                      defaultValue="Usuario"
                      className="bg-gray-700 border-gray-600 text-white mt-1"
                    />
                  </div>
                  <div>
                    <Label className="text-gray-300">Email</Label>
                    <Input 
                      type="email"
                      defaultValue="usuario@ejemplo.com"
                      className="bg-gray-700 border-gray-600 text-white mt-1"
                    />
                  </div>
                </div>
                
                <div>
                  <Label className="text-gray-300">Zona horaria</Label>
                  <select className="w-full mt-1 p-2 bg-gray-700 border border-gray-600 text-white rounded-md">
                    <option>UTC-5 (América/Bogotá)</option>
                    <option>UTC-6 (América/México)</option>
                    <option>UTC-3 (América/Argentina)</option>
                  </select>
                </div>
                
                <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  Guardar Cambios
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Settings;