import React, { useState } from 'react';
import { Search } from 'lucide-react';

const RECOMMENDATIONS = ['AI', 'Machine Learning', 'Software Engineer', 'Data Science', 'New York', 'Remote'];

const SearchBar = ({ onSearch }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSearch(query);
    };

    const handleTagClick = (tag) => {
        setQuery(tag);
        onSearch(tag);
    };

    return (
        <div className="w-full max-w-2xl mx-auto mb-10">
            <form onSubmit={handleSubmit} className="relative mb-4">
                <div className="relative group">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5 group-focus-within:text-blue-500 transition-colors" />
                    <input
                        type="text"
                        className="w-full pl-12 pr-4 py-4 rounded-2xl border border-slate-200 shadow-sm focus:ring-4 focus:ring-blue-50 focus:border-blue-500 transition-all outline-none text-slate-700 text-lg placeholder:text-slate-400"
                        placeholder="Search roles, companies, or keywords..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                </div>
            </form>

            <div className="flex flex-wrap items-center justify-center gap-2">
                <span className="text-sm text-slate-400 font-medium">Trending:</span>
                {RECOMMENDATIONS.map((tag) => (
                    <button
                        key={tag}
                        onClick={() => handleTagClick(tag)}
                        className="px-3 py-1 text-sm bg-white border border-slate-200 text-slate-600 rounded-full hover:border-blue-200 hover:text-blue-600 hover:bg-blue-50 transition-all"
                    >
                        {tag}
                    </button>
                ))}
            </div>
        </div>
    );
};

export default SearchBar;
