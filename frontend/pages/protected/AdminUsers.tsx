import { useState, useEffect } from 'react';
import { NavBar } from './Dashboard';
import api from '../../services/api';

interface User {
  id: number;
  name: string;
  email: string;
  isStaff: boolean;
  isActive: boolean;
  dateJoined: string;
  bookingCount: number;
}

interface AdminBooking {
  id: number;
  bookingNumber: string;
  client: { name: string; email: string };
  service: string;
  startTime: string;
  status: string;
  paymentStatus: string;
  price: number;
  location: string;
}

export default function AdminUsers() {
  const [users, setUsers] = useState<User[]>([]);
  const [bookings, setBookings] = useState<AdminBooking[]>([]);
  const [view, setView] = useState<'users' | 'bookings'>('users');
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    Promise.all([
      api.get('/admin/users/').catch(() => ({ data: { users: [], total: 0 } })),
      api.get('/admin/bookings/').catch(() => ({ data: { bookings: [], total: 0 } })),
    ]).then(([usersRes, bookingsRes]) => {
      setUsers(usersRes.data.users || []);
      setBookings(bookingsRes.data.bookings || []);
    }).finally(() => setLoading(false));
  }, []);

  const toggleUser = async (userId: number) => {
    try {
      const res = await api.patch(`/admin/users/${userId}/toggle/`);
      setUsers(prev => prev.map(u => u.id === userId ? { ...u, isActive: res.data.isActive } : u));
    } catch (e) { /* silent */ }
  };

  const filtered = view === 'users'
    ? users.filter(u => u.name.toLowerCase().includes(search.toLowerCase()) || u.email.toLowerCase().includes(search.toLowerCase()))
    : bookings.filter(b => b.client.name.toLowerCase().includes(search.toLowerCase()) || b.bookingNumber.toLowerCase().includes(search.toLowerCase()));

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <NavBar />
      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '48px 20px' }}>
        <div style={{ marginBottom: 40 }}>
          <div style={{ color: 'var(--brand-primary)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: 2, marginBottom: 8 }}>Admin Panel</div>
          <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.8rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 8px' }}>User Management</h1>
          <p style={{ color: '#888', margin: 0 }}>Manage all users, view bookings, and control access.</p>
        </div>

        {/* stats */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 16, marginBottom: 40 }}>
          {[
            { label: 'Total Users', value: users.length, color: '#3b82f6' },
            { label: 'Active Users', value: users.filter(u => u.isActive).length, color: 'var(--brand-primary)' },
            { label: 'Staff', value: users.filter(u => u.isStaff).length, color: '#8b5cf6' },
            { label: 'Total Bookings', value: bookings.length, color: '#f59e0b' },
          ].map(({ label, value, color }) => (
            <div key={label} style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 16, padding: '20px' }}>
              <div style={{ fontSize: '2rem', fontWeight: 800, color }}>{value}</div>
              <div style={{ color: '#888', fontSize: '0.8rem', marginTop: 4 }}>{label}</div>
            </div>
          ))}
        </div>

        {/* tabs + search */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24, flexWrap: 'wrap', gap: 16 }}>
          <div style={{ display: 'flex', gap: 4, background: 'var(--dark)', padding: 4, borderRadius: 12 }}>
            {(['users', 'bookings'] as const).map(v => (
              <button key={v} onClick={() => setView(v)} style={{
                padding: '8px 20px', borderRadius: 8, border: 'none', cursor: 'pointer', fontWeight: 600, fontSize: '0.9rem', textTransform: 'capitalize',
                background: view === v ? '#222' : 'transparent', color: view === v ? '#fff' : '#555'
              }}>{v}</button>
            ))}
          </div>
          <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search..." style={{
            background: 'var(--dark)', border: '1px solid #222', color: '#fff', padding: '10px 16px', borderRadius: 10, fontSize: '0.9rem', width: 220, outline: 'none',
          }} />
        </div>

        {loading ? <div style={{ color: '#555', padding: '60px 0' }}>Loading data...</div> : (
          <div style={{ overflowX: 'auto', background: 'var(--dark)', borderRadius: 16, border: '1px solid #222' }}>
            {view === 'users' ? (
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem', minWidth: 800 }}>
                <thead><tr style={{ borderBottom: '1px solid #222' }}>
                  {['Name', 'Email', 'Role', 'Bookings', 'Joined', 'Status', 'Action'].map(h => (
                    <th key={h} style={{ padding: '16px 20px', textAlign: 'left', color: '#555', fontWeight: 600, fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: 1 }}>{h}</th>
                  ))}
                </tr></thead>
                <tbody>
                  {(filtered as User[]).map(u => (
                    <tr key={u.id} style={{ borderBottom: '1px solid #222' }}>
                      <td style={{ padding: '16px 20px', fontWeight: 600 }}>{u.name}</td>
                      <td style={{ padding: '16px 20px', color: '#888' }}>{u.email}</td>
                      <td style={{ padding: '16px 20px' }}><span style={{ color: u.isStaff ? '#8b5cf6' : '#3b82f6', fontSize: '0.8rem', fontWeight: 600 }}>{u.isStaff ? 'Staff' : 'Member'}</span></td>
                      <td style={{ padding: '16px 20px', color: '#888' }}>{u.bookingCount}</td>
                      <td style={{ padding: '16px 20px', color: '#555', fontSize: '0.8rem' }}>{new Date(u.dateJoined).toLocaleDateString()}</td>
                      <td style={{ padding: '16px 20px' }}><span style={{ color: u.isActive ? 'var(--brand-primary)' : 'var(--red)', fontWeight: 600, fontSize: '0.8rem' }}>{u.isActive ? 'Active' : 'Blocked'}</span></td>
                      <td style={{ padding: '16px 20px' }}>
                        <button onClick={() => toggleUser(u.id)} style={{
                          background: 'transparent', border: `1px solid ${u.isActive ? 'var(--red)' : 'var(--brand-primary)'}`, color: u.isActive ? 'var(--red)' : 'var(--brand-primary)',
                          padding: '6px 16px', borderRadius: 8, cursor: 'pointer', fontSize: '0.8rem', fontWeight: 600,
                        }}>{u.isActive ? 'Block' : 'Activate'}</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem', minWidth: 900 }}>
                <thead><tr style={{ borderBottom: '1px solid #222' }}>
                  {['Booking #', 'Client', 'Service', 'Date', 'Location', 'Status', 'Payment', 'Price'].map(h => (
                    <th key={h} style={{ padding: '16px 20px', textAlign: 'left', color: '#555', fontWeight: 600, fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: 1 }}>{h}</th>
                  ))}
                </tr></thead>
                <tbody>
                  {(filtered as AdminBooking[]).map(b => (
                    <tr key={b.id} style={{ borderBottom: '1px solid #222' }}>
                      <td style={{ padding: '16px 20px', color: 'var(--brand-primary)', fontWeight: 600 }}>{b.bookingNumber}</td>
                      <td style={{ padding: '16px 20px' }}><div style={{ fontWeight: 600 }}>{b.client.name}</div><div style={{ color: '#555', fontSize: '0.8rem' }}>{b.client.email}</div></td>
                      <td style={{ padding: '16px 20px', color: '#888' }}>{b.service}</td>
                      <td style={{ padding: '16px 20px', color: '#888', fontSize: '0.85rem' }}>{new Date(b.startTime).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</td>
                      <td style={{ padding: '16px 20px', color: '#888' }}>{b.location}</td>
                      <td style={{ padding: '16px 20px' }}><span style={{ color: b.status === 'confirmed' ? 'var(--brand-primary)' : b.status === 'cancelled' ? 'var(--red)' : '#f59e0b', fontWeight: 600, fontSize: '0.8rem' }}>{b.status}</span></td>
                      <td style={{ padding: '16px 20px' }}><span style={{ color: b.paymentStatus === 'paid' ? 'var(--brand-primary)' : '#888', fontSize: '0.85rem' }}>{b.paymentStatus}</span></td>
                      <td style={{ padding: '16px 20px', color: 'var(--brand-primary)', fontWeight: 700 }}>${b.price.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            {filtered.length === 0 && <div style={{ color: '#555', textAlign: 'center', padding: '60px 0' }}>No results found.</div>}
          </div>
        )}
      </div>
    </div>
  );
}
