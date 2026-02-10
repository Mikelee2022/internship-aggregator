import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import InternshipCard from './components/InternshipCard';
import SearchBar from './components/SearchBar';
import useDarkMode from './hooks/useDarkMode';
import { LayoutGrid, Sparkles, AlertCircle, Sun, Moon, ChevronLeft, ChevronRight } from 'lucide-react';

const API_URL = 'http://127.0.0.1:8000';
const ITEMS_PER_PAGE = 12;

function App() {
  const [internships, setInternships] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1); // 1-indexed for UI
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSource, setSelectedSource] = useState(null);
  const [sources, setSources] = useState([]);
  const [theme, toggleTheme] = useDarkMode();

  const fetchInternships = useCallback(async (query = '', pageNum = 1, sourceId = null) => {
    setLoading(true);
    setError(null);
    try {
      const params = {
        offset: (pageNum - 1) * ITEMS_PER_PAGE,
        limit: ITEMS_PER_PAGE,
      };
      if (query) params.search = query;
      if (sourceId) params.source = sourceId;

      const response = await axios.get(`${API_URL}/internships`, { params });
      // Expecting { items: [], total: number }
      const { items, total } = response.data;

      setInternships(items);
      setTotal(total);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch internships. Is the backend running?');
    } finally {
      setLoading(false);
    }
  }, []);

  // Effect to load data on page, search, or source change
  useEffect(() => {
    fetchInternships(searchQuery, page, selectedSource);
  }, [page, searchQuery, selectedSource, fetchInternships]);

  // Effect to load sources
  useEffect(() => {
    const fetchSources = async () => {
      try {
        const response = await axios.get(`${API_URL}/sources`);
        setSources(response.data.filter(s => s.enabled));
      } catch (err) {
        console.error("Failed to fetch sources", err);
      }
    };
    fetchSources();
  }, []);

  const handleSearch = (query) => {
    setSearchQuery(query);
    setPage(1); // Reset to first page
  };

  const handleSourceSelect = (sourceId) => {
    setSelectedSource(prev => prev === sourceId ? null : sourceId);
    setPage(1);
  };

  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= Math.ceil(total / ITEMS_PER_PAGE)) {
      setPage(newPage);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const totalPages = Math.ceil(total / ITEMS_PER_PAGE);

  return (
    <div className="min-h-screen bg-slate-50/50 dark:bg-slate-900 transition-colors duration-300">
      {/* Header */}
      <header className="bg-white border-b border-slate-100 sticky top-0 z-10 backdrop-blur-md bg-white/80 dark:bg-slate-800/80 dark:border-slate-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-blue-600 p-1.5 rounded-lg">
              <LayoutGrid className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-800 to-slate-600 dark:from-slate-100 dark:to-slate-300">
              Internship<span className="text-blue-600 dark:text-blue-400">Aggregator</span>
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors text-slate-500 dark:text-slate-400 cursor-pointer"
              aria-label="Toggle Dark Mode"
            >
              {theme === 'dark' ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5" />}
            </button>
            <div className="text-sm font-medium text-slate-500 dark:text-slate-400 flex items-center gap-1.5 hidden sm:flex">
              <Sparkles className="w-4 h-4 text-amber-400" />
              Summer 2026 Ready
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight mb-4">
            Find Your Dream Internship
          </h2>
          <p className="text-base sm:text-lg text-slate-600 dark:text-slate-400 max-w-3xl mx-auto whitespace-nowrap overflow-hidden text-ellipsis px-4">
            Curated opportunities for students • Updated daily across Tech, Finance & AI
          </p>
        </div>

        {/* Company Logos Row */}
        <div className="mb-10 overflow-x-auto pb-4 no-scrollbar">
          <div className="flex items-center justify-center gap-4 sm:gap-6 flex-wrap px-4">
            {sources.map(source => (
              <button
                key={source.id}
                onClick={() => handleSourceSelect(source.id)}
                className={`flex flex-col items-center gap-2 group transition-all duration-300 ${selectedSource === source.id ? 'opacity-100 scale-110' : 'opacity-60 hover:opacity-100'
                  }`}
              >
                <div className={`w-16 h-16 rounded-2xl bg-white dark:bg-slate-800 border-2 flex items-center justify-center p-3 shadow-sm transition-all ${selectedSource === source.id ? 'border-blue-500 shadow-blue-100 dark:shadow-blue-900/20' : 'border-transparent group-hover:border-slate-200 dark:group-hover:border-slate-700'
                  }`}>
                  <img
                    src={source.logo_url}
                    alt={source.name}
                    className="max-w-full max-h-full object-contain filter dark:brightness-90 transition-transform group-hover:scale-110"
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.src = "https://ui-avatars.com/api/?name=" + encodeURIComponent(source.name) + "&background=random";
                    }}
                  />
                </div>
                <span className={`text-xs font-semibold whitespace-nowrap transition-colors ${selectedSource === source.id ? 'text-blue-600 dark:text-blue-400' : 'text-slate-500 dark:text-slate-400'
                  }`}>
                  {source.name.split(' ')[0]}
                </span>
              </button>
            ))}
          </div>
        </div>

        <SearchBar onSearch={handleSearch} />

        {error ? (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="bg-red-50 dark:bg-red-900/20 p-3 rounded-full mb-4">
              <AlertCircle className="w-8 h-8 text-red-500" />
            </div>
            <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Connection Error</h3>
            <p className="text-slate-500 dark:text-slate-400 mt-1 max-w-md">{error}</p>
          </div>
        ) : (
          <>
            {loading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="bg-white dark:bg-slate-800 rounded-xl h-64 border border-slate-200 dark:border-slate-700"></div>
                ))}
              </div>
            ) : internships.length === 0 ? (
              <div className="text-center py-20">
                <h3 className="text-lg font-medium text-slate-900 dark:text-white">No internships found</h3>
                <p className="text-slate-500 dark:text-slate-400">Try adjusting your search criteria</p>
              </div>
            ) : (
              <>
                <div className="mb-4 text-sm text-slate-500 dark:text-slate-400">
                  Showing <span className="font-semibold text-slate-900 dark:text-white">{(page - 1) * ITEMS_PER_PAGE + 1}-{Math.min(page * ITEMS_PER_PAGE, total)}</span> of <span className="font-semibold text-slate-900 dark:text-white">{total}</span> results
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {internships.map((internship) => (
                    <InternshipCard key={internship.id} internship={internship} />
                  ))}
                </div>

                {/* Pagination Controls */}
                <div className="mt-12 flex items-center justify-center gap-4">
                  <button
                    onClick={() => handlePageChange(page - 1)}
                    disabled={page === 1}
                    className="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <ChevronLeft className="w-5 h-5" />
                  </button>

                  <span className="text-sm font-medium text-slate-600 dark:text-slate-400">
                    Page {page} of {totalPages}
                  </span>

                  <button
                    onClick={() => handlePageChange(page + 1)}
                    disabled={page >= totalPages}
                    className="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <ChevronRight className="w-5 h-5" />
                  </button>
                </div>
              </>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;

