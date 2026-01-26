import React from 'react';
import { MapPin, Building, Calendar, ExternalLink, Zap, Globe } from 'lucide-react';

const InternshipCard = ({ internship }) => {
    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
        });
    };

    return (
        <div className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 border border-slate-100 overflow-hidden group h-full flex flex-col">
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
                                <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center text-blue-600">
                                    <Building className="w-6 h-6" />
                                </div>
                            )}
                            <div>
                                <h3 className="text-lg font-semibold text-slate-900 group-hover:text-blue-600 transition-colors leading-tight">
                                    {internship.role}
                                </h3>
                                <div className="text-sm font-medium text-slate-500">
                                    {internship.company}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="flex gap-2">
                        {internship.international_score && (
                            <span className={`text-xs px-2.5 py-1 rounded-full font-medium flex items-center gap-1 shadow-sm ${internship.international_score >= 8 ? 'bg-green-100 text-green-700' :
                                    internship.international_score >= 4 ? 'bg-amber-100 text-amber-700' :
                                        'bg-red-100 text-red-700'
                                }`}>
                                <Globe className="w-3 h-3" />
                                {internship.international_score}
                            </span>
                        )}
                        {internship.ai_label && (
                            <span className="bg-gradient-to-r from-violet-500 to-fuchsia-500 text-white text-xs px-2.5 py-1 rounded-full font-medium flex items-center gap-1 shadow-sm">
                                <Zap className="w-3 h-3 fill-current" />
                                AI
                            </span>
                        )}
                    </div>
                </div>

                <div className="flex flex-wrap gap-4 text-sm text-slate-500 mb-4">
                    <div className="flex items-center gap-1.5 bg-slate-50 px-2 py-1 rounded-md">
                        <MapPin className="w-4 h-4 text-slate-400" />
                        {internship.location}
                    </div>
                    <div className="flex items-center gap-1.5 bg-slate-50 px-2 py-1 rounded-md">
                        <Calendar className="w-4 h-4 text-slate-400" />
                        {formatDate(internship.posted_date)}
                    </div>
                    {internship.salary && (
                        <div className="flex items-center gap-1.5 bg-green-50 px-2 py-1 rounded-md text-green-700 font-medium">
                            <span>💰</span>
                            {internship.salary}
                        </div>
                    )}
                </div>

                <div className="flex items-center justify-between border-t border-slate-50 pt-4 mt-auto">
                    <span className="text-xs font-medium text-slate-400 uppercase tracking-wide">
                        {internship.industry}
                    </span>
                    <a
                        href={internship.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-600 hover:text-blue-700 hover:underline"
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
