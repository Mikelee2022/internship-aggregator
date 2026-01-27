import React, { useEffect, useState, useRef, useCallback } from 'react';
import axios from 'axios';
import InternshipCard from './components/InternshipCard';
import SearchBar from './components/SearchBar';
import useDarkMode from './hooks/useDarkMode';
import { LayoutGrid, Sparkles, AlertCircle, Sun, Moon } from 'lucide-react';

const API_URL = 'http://127.0.0.1:8000';
const ITEMS_PER_PAGE = 18;

function App() {
  const [internships, setInternships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [theme, toggleTheme] = useDarkMode();

  // Observer for infinite scroll
  const observer = useRef();
  const lastInternshipElementRef = useCallback(node => {
    if (loading) return;
    if (observer.current) observer.current.disconnect();
    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && hasMore) {
        setPage(prevPage => prevPage + 1);
      }
    });
    if (node) observer.current.observe(node);
  }, [loading, hasMore]);


  // Deduplicate and append helper
  const mergeInternships = (existing, newItems) => {
    const existingIds = new Set(existing.map(i => i.id));
    const uniqueNew = newItems.filter(i => !existingIds.has(i.id));
    return [...existing, ...uniqueNew];
  };

  const fetchInternships = useCallback(async (query = '', pageNum = 0, reset = false) => {
    setLoading(true);
    setError(null);
    try {
      const params = {
        offset: pageNum * ITEMS_PER_PAGE,
        limit: ITEMS_PER_PAGE,
      };
      if (query) params.search = query;

      const response = await axios.get(`${API_URL}/internships`, { params });
      const newInternships = response.data;

      setInternships(prev => {
        if (reset) return newInternships;
        return mergeInternships(prev, newInternships);
      });

      // Stop if we fetched fewer items than requested (end of list)
      setHasMore(newInternships.length === ITEMS_PER_PAGE);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch internships. Is the backend running?');
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial load and search change
  useEffect(() => {
    setPage(0);
    fetchInternships(searchQuery, 0, true);
  }, [searchQuery, fetchInternships]);

  // Load more pages
  useEffect(() => {
    if (page > 0) {
      fetchInternships(searchQuery, page, false);
    }
  }, [page, searchQuery, fetchInternships]);

  const handleSearch = (query) => {
    setSearchQuery(query);
  };

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
              className="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors text-slate-500 dark:text-slate-400"
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
          <h2 className="text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight mb-4">
            Find Your Dream Internship
          </h2>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Curated opportunities for students. Updated daily with the latest roles across Tech, Finance, and AI.
          </p>
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
            {internships.length === 0 && !loading ? (
              <div className="text-center py-20">
                <h3 className="text-lg font-medium text-slate-900 dark:text-white">No internships found</h3>
                <p className="text-slate-500 dark:text-slate-400">Try adjusting your search criteria</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {internships.map((internship, index) => {
                  if (internships.length === index + 1) {
                    return (
                      <div ref={lastInternshipElementRef} key={internship.id}>
                        <InternshipCard internship={internship} />
                      </div>
                    );
                  } else {
                    return <InternshipCard key={internship.id} internship={internship} />;
                  }
                })}
              </div>
            )}
            {loading && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6 animate-pulse">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="bg-white dark:bg-slate-800 rounded-xl h-64 border border-slate-200 dark:border-slate-700"></div>
                ))}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;

