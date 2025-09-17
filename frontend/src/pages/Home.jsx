import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { ArrowRight, Bot, TrendingUp, Shield, Zap, BarChart3, Users } from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: Bot,
      title: 'Trading Automatizado',
      description: 'Bots inteligentes que operan 24/7 con estrategias optimizadas por IA'
    },
    {
      icon: TrendingUp,
      title: 'Máxima Rentabilidad',
      description: 'Algoritmos avanzados para maximizar ganancias en tiempo real'
    },
    {
      icon: Shield,
      title: 'Gestión de Riesgo',
      description: 'Perfiles de riesgo personalizables: Conservador, Moderado, Agresivo'
    },
    {
      icon: Zap,
      title: 'Ejecución Instantánea',
      description: 'Conexión directa con Zaffex para operaciones ultrarrápidas'
    }
  ];

  const stats = [
    { label: 'Usuarios Activos', value: '12,847', icon: Users },
    { label: 'Ganancias Generadas', value: '$2.8M', icon: TrendingUp },
    { label: 'Precisión Promedio', value: '87.3%', icon: BarChart3 },
    { label: 'Operaciones/Día', value: '45,692', icon: Zap }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Hero Section */}
      <section className="relative px-4 pt-20 pb-32">
        <div className="max-w-7xl mx-auto text-center">
          <Badge className="mb-6 bg-gradient-to-r from-blue-500 to-purple-600 text-white border-0">
            🚀 Nuevo: Integración avanzada con Zaffex
          </Badge>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-white via-blue-100 to-purple-100 bg-clip-text text-transparent">
            Trading Automatizado
            <br />
            <span className="text-blue-400">Inteligente</span>
          </h1>
          
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Conecta con Zaffex y deja que nuestros bots de IA hagan el trabajo por ti.
            Operaciones automatizadas con el mayor porcentaje de ganancias en tiempo real.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              asChild 
              size="lg" 
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-4 text-lg"
            >
              <Link to="/dashboard">
                Empezar Trading <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
            </Button>
            <Button 
              variant="outline" 
              size="lg" 
              className="border-gray-600 text-gray-300 hover:text-white hover:bg-gray-700 px-8 py-4 text-lg"
            >
              Ver Demo
            </Button>
          </div>
        </div>
        
        {/* Floating elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-blue-500/20 rounded-full blur-xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-32 h-32 bg-purple-500/20 rounded-full blur-xl animate-pulse delay-1000"></div>
      </section>

      {/* Stats Section */}
      <section className="px-4 py-16 bg-gray-800/50">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map(({ label, value, icon: Icon }) => (
              <div key={label} className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                </div>
                <div className="text-3xl font-bold text-white mb-2">{value}</div>
                <div className="text-sm text-gray-400">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-4 py-20">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Características Avanzadas
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Tecnología de vanguardia para maximizar tus ganancias en el mercado
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map(({ icon: Icon, title, description }) => (
              <Card key={title} className="bg-gray-800 border-gray-700 hover:border-blue-500/50 transition-colors group">
                <CardHeader>
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <CardTitle className="text-white">{title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-gray-400">
                    {description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-4 py-20 bg-gradient-to-r from-blue-900/50 to-purple-900/50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-4">
            ¿Listo para Automatizar tu Trading?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Únete a miles de traders que ya están generando ganancias pasivas con GPTading Pro
          </p>
          <Button 
            asChild 
            size="lg" 
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-12 py-6 text-lg"
          >
            <Link to="/dashboard">
              Comenzar Ahora <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Home;