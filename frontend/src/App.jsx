import React, { useEffect, useState } from 'react';
import axios from 'axios';
import InternshipCard from './components/InternshipCard';
import SearchBar from './components/SearchBar';
import { LayoutGrid, Sparkles, AlertCircle } from 'lucide-react';

const API_URL = 'http://127.0.0.1:8000';

function App() {
  const [internships, setInternships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchInternships = async (search = '') => {
    setLoading(true);
    setError(null);
    try {
      const params = {};
      if (search) params.search = search;
      // Default API sort is by date already
      const response = await axios.get(`${API_URL}/internships`, { params });
      setInternships(response.data);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch internships. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInternships();
  }, []);

  const handleSearch = (query) => {
    fetchInternships(query);
  };

  return (
    <div className="min-h-screen bg-slate-50/50">
      {/* Header */}
      <header className="bg-white border-b border-slate-100 sticky top-0 z-10 backdrop-blur-md bg-white/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-blue-600 p-1.5 rounded-lg">
              <LayoutGrid className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-800 to-slate-600">
              Internship<span className="text-blue-600">Aggregator</span>
            </h1>
          </div>
          <div className="text-sm font-medium text-slate-500 flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-amber-400" />
            Summer 2026 Ready
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-extrabold text-slate-900 tracking-tight mb-4">
            Find Your Dream Internship
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Curated opportunities for students. Updated daily with the latest roles across Tech, Finance, and AI.
          </p>
        </div>

        <SearchBar onSearch={handleSearch} />

        {error ? (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="bg-red-50 p-3 rounded-full mb-4">
              <AlertCircle className="w-8 h-8 text-red-500" />
            </div>
            <h3 className="text-lg font-semibold text-slate-900">Connection Error</h3>
            <p className="text-slate-500 mt-1 max-w-md">{error}</p>
          </div>
        ) : loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="bg-white rounded-xl h-64 border border-slate-200"></div>
            ))}
          </div>
        ) : internships.length === 0 ? (
          <div className="text-center py-20">
            <h3 className="text-lg font-medium text-slate-900">No internships found</h3>
            <p className="text-slate-500">Try adjusting your search criteria</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {internships.map((internship) => (
              <InternshipCard key={internship.id} internship={internship} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
