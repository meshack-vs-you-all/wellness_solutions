import { useState, useEffect } from 'react';
import { NavBar } from './Dashboard';
import api from '../../services/api';

interface Product {
  id: string | number;
  name: string;
  description: string;
  price: number;
  category: string;
  sessions?: number;
  inStock: boolean;
}

const categoryColors: Record<string, string> = { package: 'var(--brand-primary)', gear: '#3b82f6', apparel: '#8b5cf6', bundle: '#f59e0b', all: '#555' };
const categoryIcons: Record<string, string> = { package: '🧘', gear: '🏋️', apparel: '👕', bundle: '🎁', all: '🛍️' };

export default function Shop() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<string[]>(['all']);
  const [activeCategory, setActiveCategory] = useState('all');
  const [cart, setCart] = useState<{ [id: string]: number }>({});
  const [loading, setLoading] = useState(true);
  const [cartOpen, setCartOpen] = useState(false);
  const [checkoutStep, setCheckoutStep] = useState<'cart' | 'payment' | 'success'>('cart');
  const [mpesaCode, setMpesaCode] = useState('');

  useEffect(() => {
    api.get('/shop/products/').then(res => {
      setProducts(res.data.products || []);
      setCategories(res.data.categories || ['all']);
    }).catch(() => { }).finally(() => setLoading(false));
  }, []);

  const filtered = activeCategory === 'all' ? products : products.filter(p => p.category === activeCategory);
  const totalItems = Object.values(cart).reduce((a, b) => a + b, 0);
  const totalPrice = Object.entries(cart).reduce((total, [id, qty]) => {
    const p = products.find(p => String(p.id) === id);
    return total + (p ? p.price * qty : 0);
  }, 0);

  const addToCart = (product: Product) => {
    setCart(prev => ({ ...prev, [String(product.id)]: (prev[String(product.id)] || 0) + 1 }));
  };

  const handleCheckout = () => {
    if (!mpesaCode) return alert('Please enter M-Pesa transaction code');
    // Simulate API checkout
    setCheckoutStep('success');
    setTimeout(() => {
      setCart({});
      setCartOpen(false);
      setCheckoutStep('cart');
      setMpesaCode('');
    }, 4000);
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <NavBar />
      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '48px 20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 40, flexWrap: 'wrap', gap: 20 }}>
          <div>
            <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.5rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 8px' }}>JPF Shop</h1>
            <p style={{ color: '#888', margin: 0 }}>Gear, packages, and everything you need for your wellness journey.</p>
          </div>
          <button onClick={() => setCartOpen(!cartOpen)} style={{
            background: totalItems > 0 ? 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))' : 'var(--dark)',
            border: '1px solid #222', color: '#fff', padding: '12px 20px', borderRadius: 12,
            cursor: 'pointer', fontWeight: 700, display: 'flex', alignItems: 'center', gap: 10, position: 'relative',
          }}>
            🛒 Cart {totalItems > 0 && <span style={{ background: 'var(--red)', borderRadius: '50%', width: 20, height: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 800 }}>{totalItems}</span>}
          </button>
        </div>

        {/* Cart drawer */}
        {cartOpen && totalItems > 0 && (
          <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 20, padding: 24, marginBottom: 32 }}>
            <h3 style={{ marginBottom: 16, fontWeight: 700 }}>Your Cart</h3>
            {Object.entries(cart).filter(([, qty]) => qty > 0).map(([id, qty]) => {
              const p = products.find(p => String(p.id) === id);
              if (!p) return null;
              return (
                <div key={id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: 12, borderBottom: '1px solid #1a1a1a', marginBottom: 12, gap: 20, flexWrap: 'wrap' }}>
                  <div>
                    <div style={{ fontWeight: 600 }}>{p.name}</div>
                    <div style={{ color: '#888', fontSize: '0.85rem' }}>×{qty}</div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                    <span style={{ color: 'var(--brand-primary)', fontWeight: 700 }}>${(p.price * qty).toFixed(2)}</span>
                    <button onClick={() => setCart(prev => { const n = { ...prev }; if ((n[id] || 0) > 1) n[id]--; else delete n[id]; return n; })} style={{ background: 'transparent', border: '1px solid #222', color: 'var(--red)', padding: '4px 10px', borderRadius: 6, cursor: 'pointer', fontSize: '0.85rem' }}>−</button>
                  </div>
                </div>
              );
            })}
            {checkoutStep === 'cart' && (
              <>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 16 }}>
                  <div style={{ color: '#888' }}>Total: <span style={{ color: 'var(--brand-primary)', fontWeight: 800, fontSize: '1.2rem' }}>KES {totalPrice.toFixed(0)}</span></div>
                  <button onClick={() => setCheckoutStep('payment')} style={{ background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', padding: '12px 24px', border: 'none', borderRadius: 12, cursor: 'pointer', fontWeight: 700 }}>
                    Proceed to Pay →
                  </button>
                </div>
              </>
            )}

            {checkoutStep === 'payment' && (
              <div style={{ marginTop: 24, borderTop: '1px solid #222', paddingTop: 24 }}>
                <div style={{ background: 'rgba(18,18,18,0.5)', border: '1px solid #222', borderRadius: 16, padding: 20, textAlign: 'center', marginBottom: 20 }}>
                  <div style={{ display: 'inline-block', background: 'var(--brand-primary)', color: '#fff', padding: '4px 12px', borderRadius: 20, fontSize: '0.8rem', fontWeight: 800, letterSpacing: 1, marginBottom: 12 }}>LIPA NA M-PESA</div>
                  <h4 style={{ margin: '0 0 8px', fontSize: '1.2rem' }}>Paybill: <span style={{ color: 'var(--brand-primary)', fontWeight: 800, letterSpacing: 2 }}>123456</span></h4>
                  <p style={{ margin: '0 0 16px', color: '#888', fontSize: '0.9rem' }}>Account: <span style={{ color: '#fff', fontWeight: 600 }}>Shop-{Math.floor(Math.random() * 1000)}</span></p>
                  <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--brand-primary)' }}>KES {totalPrice.toFixed(0)}</div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                  <label style={{ fontSize: '0.9rem', color: '#888', fontWeight: 600 }}>Enter M-Pesa Transaction Code</label>
                  <input
                    placeholder="e.g. QWE123RTY4"
                    value={mpesaCode}
                    onChange={e => setMpesaCode(e.target.value.toUpperCase())}
                    style={{ background: 'var(--soft-dark)', border: '1px solid #222', color: '#fff', padding: '14px', borderRadius: 10, fontSize: '1rem', textTransform: 'uppercase', outline: 'none' }}
                  />
                  <div style={{ display: 'flex', gap: 12, marginTop: 8 }}>
                    <button onClick={() => setCheckoutStep('cart')} style={{ flex: 1, background: 'transparent', border: '1px solid #222', color: '#888', padding: '14px', borderRadius: 10, cursor: 'pointer', fontWeight: 600 }}>Back</button>
                    <button onClick={handleCheckout} style={{ flex: 2, background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', border: 'none', color: '#fff', padding: '14px', borderRadius: 10, cursor: 'pointer', fontWeight: 700 }}>Confirm Payment</button>
                  </div>
                </div>
              </div>
            )}

            {checkoutStep === 'success' && (
              <div style={{ textAlign: 'center', padding: '30px 0' }}>
                <div style={{ fontSize: '3rem', marginBottom: 16 }}>✅</div>
                <h3 style={{ margin: '0 0 8px', fontSize: '1.5rem', color: 'var(--brand-primary)' }}>Payment Verified!</h3>
                <p style={{ color: '#888', margin: '0 0 24px' }}>Your credits have been added to your clinical account.</p>
                <button
                  onClick={() => {
                    setCart({});
                    setCartOpen(false);
                    setCheckoutStep('cart');
                    window.location.href = '/booking';
                  }}
                  style={{ background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', border: 'none', padding: '12px 32px', borderRadius: 12, fontWeight: 700, cursor: 'pointer' }}
                >
                  Book Your Session Now →
                </button>
              </div>
            )}
          </div>
        )}

        {/* Category tabs */}
        <div style={{ display: 'flex', gap: 10, marginBottom: 32, flexWrap: 'wrap' }}>
          {categories.map(cat => (
            <button key={cat} onClick={() => setActiveCategory(cat)} style={{
              padding: '8px 20px', borderRadius: 99, border: '1px solid', fontSize: '0.9rem', fontWeight: 600, cursor: 'pointer', textTransform: 'capitalize',
              borderColor: activeCategory === cat ? (categoryColors[cat] || 'var(--brand-primary)') : '#222',
              background: activeCategory === cat ? `${categoryColors[cat] || 'var(--brand-primary)'}18` : 'transparent',
              color: activeCategory === cat ? (categoryColors[cat] || 'var(--brand-primary)') : '#888',
            }}>
              {categoryIcons[cat] || '📦'} {cat}
            </button>
          ))}
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', color: '#555', padding: '80px 0' }}>Loading products...</div>
        ) : filtered.length === 0 ? (
          <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 24, padding: '80px 40px', textAlign: 'center' }}>
            <div style={{ fontSize: '3.5rem', marginBottom: 20 }}>📦</div>
            <h3 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#fff', marginBottom: 12 }}>Wellness Essentials Restocking</h3>
            <p style={{ color: '#888', maxWidth: 400, margin: '0 auto', lineHeight: 1.6 }}>
              Our curated clinical recovery tools are currently being restocked. Check back in a few hours or contact your trainer for recommendations.
            </p>
            <button onClick={() => setActiveCategory('all')} style={{ marginTop: 24, background: 'transparent', border: '1px solid #222', color: 'var(--brand-primary)', padding: '10px 20px', borderRadius: 10, cursor: 'pointer', fontWeight: 600 }}>View All Categories</button>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 24 }}>
            {filtered.map(product => {
              const imagePath = (product as any).image;
              const fullImageUrl = imagePath && imagePath.startsWith('/static/')
                ? `${api.defaults.baseURL?.replace('/api', '')}${imagePath}`
                : imagePath;

              return (
                <div key={product.id} style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 20, overflow: 'hidden', display: 'flex', flexDirection: 'column', transition: 'all 0.2s' }}
                  onMouseOver={e => { e.currentTarget.style.transform = 'translateY(-4px)'; e.currentTarget.style.borderColor = '#333'; }}
                  onMouseOut={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.borderColor = '#222'; }}>
                  <div style={{
                    height: 180,
                    background: fullImageUrl ? `url(${fullImageUrl}) center/cover` : `linear-gradient(135deg, rgba(15,173,182,0.1), var(--soft-dark))`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '3.5rem'
                  }}>
                    {!fullImageUrl && (categoryIcons[product.category] || '📦')}
                  </div>
                  <div style={{ padding: 24, flex: 1, display: 'flex', flexDirection: 'column' }}>
                    <div style={{ display: 'flex', gap: 8, marginBottom: 12, flexWrap: 'wrap' }}>
                      <span style={{ background: `${categoryColors[product.category] || 'var(--brand-primary)'}18`, color: categoryColors[product.category] || 'var(--brand-primary)', padding: '3px 10px', borderRadius: 99, fontSize: '0.75rem', fontWeight: 600, textTransform: 'capitalize' }}>{product.category}</span>
                      {product.sessions && <span style={{ background: 'rgba(59,130,246,0.1)', color: '#3b82f6', padding: '3px 10px', borderRadius: 99, fontSize: '0.75rem', fontWeight: 600 }}>{product.sessions} sessions</span>}
                    </div>
                    <h3 style={{ fontWeight: 700, fontSize: '1.1rem', margin: '0 0 10px', letterSpacing: '-0.01em' }}>{product.name}</h3>
                    <p style={{ color: '#888', fontSize: '0.9rem', lineHeight: 1.6, flex: 1, margin: '0 0 20px' }}>{product.description}</p>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ color: 'var(--brand-primary)', fontWeight: 800, fontSize: '1.3rem' }}>${product.price.toFixed(2)}</span>
                      <button onClick={() => addToCart(product)} disabled={!product.inStock} style={{
                        background: product.inStock ? 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))' : '#222',
                        color: product.inStock ? '#fff' : '#555', padding: '10px 20px', border: 'none', borderRadius: 10, cursor: product.inStock ? 'pointer' : 'not-allowed',
                        fontWeight: 700, fontSize: '0.9rem', transition: 'opacity 0.2s',
                      }}>
                        {product.inStock ? '+ Add to Cart' : 'Out of Stock'}
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
