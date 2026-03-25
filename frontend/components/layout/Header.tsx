import React, { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../common/Button';
import { LogOut, User as UserIcon, LayoutDashboard, CalendarCheck, Moon, Sun, Menu, X } from 'lucide-react';
import { useTheme } from '../../contexts/ThemeContext';

const Header: React.FC = () => {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const getLinkClass = ({ isActive }: { isActive: boolean }) =>
    `text-neutral-600 dark:text-neutral-300 hover:text-primary dark:hover:text-primary-light transition-colors ${isActive ? 'text-primary dark:text-primary-light font-semibold' : ''}`;

  const closeMobileMenu = () => setMobileMenuOpen(false);

  return (
    <header className="bg-white dark:bg-neutral-800 shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="text-xl sm:text-2xl font-bold text-primary dark:text-primary-light">
            Wellness Solutions
          </Link>
          
          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center space-x-6">
            <NavLink to="/" className={getLinkClass} end>Home</NavLink>
            <NavLink to="/schedule" className={getLinkClass}>Schedule</NavLink>
            <NavLink to="/services" className={getLinkClass}>Services</NavLink>
            <NavLink to="/pricing" className={getLinkClass}>Pricing</NavLink>
            <NavLink to="/about" className={getLinkClass}>About</NavLink>
            <NavLink to="/contact" className={getLinkClass}>Contact</NavLink>
          </nav>
          
          {/* Desktop User Menu */}
          <div className="hidden lg:flex items-center space-x-4">
            <Button onClick={toggleTheme} variant="ghost" size="sm" className="px-2">
              {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
            </Button>
            {user ? (
              <>
                <Link to="/dashboard" title="Dashboard" className="text-neutral-600 dark:text-neutral-300 hover:text-primary dark:hover:text-primary-light transition-colors">
                  <LayoutDashboard size={20} />
                </Link>
                <Link to="/bookings" title="My Bookings" className="text-neutral-600 dark:text-neutral-300 hover:text-primary dark:hover:text-primary-light transition-colors">
                  <CalendarCheck size={20} />
                </Link>
                <Link to="/profile" title="Profile" className="text-neutral-600 dark:text-neutral-300 hover:text-primary dark:hover:text-primary-light transition-colors">
                  <UserIcon size={20} />
                </Link>
                <Button onClick={logout} variant="outline" size="sm" className="hidden sm:flex">
                  <LogOut size={16} className="mr-2" />
                  Logout
                </Button>
                <Button onClick={logout} variant="outline" size="sm" className="sm:hidden p-2">
                  <LogOut size={16} />
                </Button>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="ghost">Login</Button>
                </Link>
                <Link to="/register">
                  <Button>Sign Up</Button>
                </Link>
              </>
            )}
          </div>
          
          {/* Mobile Menu Button */}
          <div className="flex lg:hidden items-center space-x-2">
            <Button onClick={toggleTheme} variant="ghost" size="sm" className="px-2">
              {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
            </Button>
            <Button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              variant="ghost"
              size="sm"
              className="px-2"
            >
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </Button>
          </div>
        </div>
        
        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="lg:hidden mt-4 pb-4 border-t border-gray-200 dark:border-gray-700">
            <nav className="flex flex-col space-y-2 mt-4">
              <NavLink to="/" className={getLinkClass} onClick={closeMobileMenu} end>
                Home
              </NavLink>
              <NavLink to="/schedule" className={getLinkClass} onClick={closeMobileMenu}>
                Schedule
              </NavLink>
              <NavLink to="/services" className={getLinkClass} onClick={closeMobileMenu}>
                Services
              </NavLink>
              <NavLink to="/pricing" className={getLinkClass} onClick={closeMobileMenu}>
                Pricing
              </NavLink>
              <NavLink to="/about" className={getLinkClass} onClick={closeMobileMenu}>
                About
              </NavLink>
              <NavLink to="/contact" className={getLinkClass} onClick={closeMobileMenu}>
                Contact
              </NavLink>
              
              {user ? (
                <>
                  <div className="border-t border-gray-200 dark:border-gray-700 pt-2 mt-2">
                    <NavLink to="/dashboard" className={getLinkClass} onClick={closeMobileMenu}>
                      <LayoutDashboard size={16} className="inline mr-2" />
                      Dashboard
                    </NavLink>
                    <NavLink to="/bookings" className={getLinkClass} onClick={closeMobileMenu}>
                      <CalendarCheck size={16} className="inline mr-2" />
                      My Bookings
                    </NavLink>
                    <NavLink to="/profile" className={getLinkClass} onClick={closeMobileMenu}>
                      <UserIcon size={16} className="inline mr-2" />
                      Profile
                    </NavLink>
                    <Button onClick={() => { logout(); closeMobileMenu(); }} variant="outline" className="w-full mt-2">
                      <LogOut size={16} className="mr-2" />
                      Logout
                    </Button>
                  </div>
                </>
              ) : (
                <div className="border-t border-gray-200 dark:border-gray-700 pt-2 mt-2 space-y-2">
                  <Link to="/login" onClick={closeMobileMenu} className="block">
                    <Button variant="ghost" className="w-full">Login</Button>
                  </Link>
                  <Link to="/register" onClick={closeMobileMenu} className="block">
                    <Button className="w-full">Sign Up</Button>
                  </Link>
                </div>
              )}
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;