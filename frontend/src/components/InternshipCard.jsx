import React from 'react';
import { MapPin, Building, Calendar, ExternalLink, Zap, Globe } from 'lucide-react';

const InternshipCard = ({ internship }) => {
    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
        });
    };

    const getScoreTooltip = (score) => {
        if (score >= 8) return "High chance of sponsorship (Visa/CPT/OPT)";
        if (score >= 5) return "Sponsorship possible but not guaranteed";
        return "Sponsorship unlikely or US Citizen only";
    };

    return (
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 border border-slate-100 dark:border-slate-700 group h-full flex flex-col relative">
            <div className="p-6 flex-1 flex flex-col">
                <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                            {internship.logo_url ? (
                                <img
                                    src={internship.logo_url}
                                    alt={`${internship.company} logo`}
                                    className="w-10 h-10 rounded-lg object-contain bg-white border border-slate-100 p-0.5"
                                    onError={(e) => {
                                        e.target.onerror = null;
                                        e.target.src = "https://via.placeholder.com/40?text=" + internship.company.charAt(0);
                                    }}
                                />
                            ) : (
                                <div className="w-10 h-10 rounded-lg bg-blue-50 dark:bg-slate-700 flex items-center justify-center text-blue-600 dark:text-blue-400">
                                    <Building className="w-6 h-6" />
                                </div>
                            )}
                            <div>
                                <h3 className="text-lg font-semibold text-slate-900 dark:text-white leading-tight">
                                    <a
                                        href={internship.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                                    >
                                        {internship.role}
                                    </a>
                                </h3>
                                <div className="text-sm font-medium text-slate-500 dark:text-slate-400">
                                    {internship.company}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="flex gap-2">
                        {internship.international_score && (
                            <div className="relative group/tooltip">
                                <span className={`cursor-help text-xs px-2.5 py-1 rounded-full font-medium flex items-center gap-1 shadow-sm ${internship.international_score >= 8 ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' :
                                    internship.international_score >= 4 ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400' :
                                        'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                                    }`}>
                                    <Globe className="w-3 h-3" />
                                    {internship.international_score}
                                </span>
                                {/* Tooltip */}
                                <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 p-2 bg-slate-900 text-white text-xs rounded-lg opacity-0 group-hover/tooltip:opacity-100 transition-opacity pointer-events-none z-20 text-center shadow-lg">
                                    {getScoreTooltip(internship.international_score)}
                                    <div className="absolute top-full left-1/2 -translate-x-1/2 border-8 border-transparent border-t-slate-900"></div>
                                </div>
                            </div>
                        )}
                        {internship.ai_label && (
                            <span className="bg-gradient-to-r from-violet-500 to-fuchsia-500 text-white text-xs px-2.5 py-1 rounded-full font-medium flex items-center gap-1 shadow-sm">
                                <Zap className="w-3 h-3 fill-current" />
                                AI
                            </span>
                        )}
                    </div>
                </div>

                <div className="flex flex-wrap gap-4 text-sm text-slate-500 dark:text-slate-400 mb-4">
                    <div className="flex items-center gap-1.5 bg-slate-50 dark:bg-slate-700/50 px-2 py-1 rounded-md">
                        <MapPin className="w-4 h-4 text-slate-400 dark:text-slate-500" />
                        {internship.location}
                    </div>
                    <div className="flex items-center gap-1.5 bg-slate-50 dark:bg-slate-700/50 px-2 py-1 rounded-md">
                        <Calendar className="w-4 h-4 text-slate-400 dark:text-slate-500" />
                        {formatDate(internship.posted_date)}
                    </div>
                    {internship.salary && (
                        <div className="flex items-center gap-1.5 bg-green-50 dark:bg-green-900/20 px-2 py-1 rounded-md text-green-700 dark:text-green-400 font-medium">
                            <span>💰</span>
                            {internship.salary}
                        </div>
                    )}
                </div>

                <div className="flex items-center justify-between border-t border-slate-50 dark:border-slate-700 pt-4 mt-auto">
                    <span className="text-xs font-medium text-slate-400 dark:text-slate-500 uppercase tracking-wide">
                        {internship.industry}
                    </span>
                    <a
                        href={internship.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 hover:underline"
                    >
                        Apply Now
                        <ExternalLink className="w-4 h-4" />
                    </a>
                </div>
            </div>
        </div>
    );
};

export default InternshipCard;

