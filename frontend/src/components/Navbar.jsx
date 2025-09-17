import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from './ui/button';
import { BarChart3, Settings, Wallet, Bot, TrendingUp } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();
  
  const navItems = [
    { href: '/', label: 'Inicio', icon: TrendingUp },
    { href: '/dashboard', label: 'Dashboard', icon: BarChart3 },
    { href: '/bots', label: 'Trading Bots', icon: Bot },
    { href: '/wallet', label: 'Billetera', icon: Wallet },
    { href: '/settings', label: 'Configuración', icon: Settings },
  ];

  return (
    <nav className="bg-gray-800 border-b border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">GPTading Pro</span>
            </Link>
          </div>
          
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map(({ href, label, icon: Icon }) => (
              <Link
                key={href}
                to={href}
                className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  location.pathname === href
                    ? 'text-blue-400 bg-gray-700'
                    : 'text-gray-300 hover:text-white hover:bg-gray-700'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{label}</span>
              </Link>
            ))}
          </div>
          
          <div className="flex items-center space-x-4">
            <Button variant="outline" size="sm" className="border-gray-600 text-gray-300 hover:text-white">
              Conectar Zaffex
            </Button>
            <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-blue-500 rounded-full flex items-center justify-center">
              <span className="text-xs font-bold">U</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;