'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Script from 'next/script';

interface Analysis {
  life_path_number: number;
  destiny_number: number;
  soul_urge_number: number;
  personality_number: number;
  birthday_number: number;
  maturity_number: number;
  personal_year: number;
  karmic_lessons: number[];
  analysis: string;
}

export default function Home() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    fullName: '',
    birthDate: ''
  });
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Convert date from YYYY-MM-DD to DD-MM-YYYY
      const [year, month, day] = formData.birthDate.split('-');
      const formattedDate = `${day}-${month}-${year}`;

      const response = await fetch('http://127.0.0.1:8080/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json'
        },
        mode: 'cors',
        body: JSON.stringify({
          full_name: formData.fullName,
          birth_date: formattedDate
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to get analysis');
      }

      const data = await response.json();
      setAnalysis(data);
      setStep(2);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An error occurred');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900">
      {/* Google AdSense Script */}
      <Script
        async
        src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR_CLIENT_ID"
        crossOrigin="anonymous"
      />

      <div className="container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-bold text-white mb-4">Discover Your True Self</h1>
          <p className="text-xl text-purple-200">
            Unlock the secrets of your personality through ancient numerology
          </p>
        </motion.div>

        {error && (
          <div className="max-w-md mx-auto mb-8 bg-red-500/10 border border-red-500/20 rounded-lg p-4 text-red-200">
            {error}
          </div>
        )}

        {step === 1 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="max-w-md mx-auto bg-white/10 backdrop-blur-lg rounded-xl p-8 shadow-2xl"
          >
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label
                  htmlFor="fullName"
                  className="block text-purple-200 text-sm font-medium mb-2"
                >
                  Full Name
                </label>
                <input
                  type="text"
                  id="fullName"
                  required
                  className="w-full px-4 py-2 rounded-lg bg-white/5 border border-purple-300/20 text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  value={formData.fullName}
                  onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                />
              </div>

              <div>
                <label
                  htmlFor="birthDate"
                  className="block text-purple-200 text-sm font-medium mb-2"
                >
                  Birth Date
                </label>
                <input
                  type="date"
                  id="birthDate"
                  required
                  className="w-full px-4 py-2 rounded-lg bg-white/5 border border-purple-300/20 text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  value={formData.birthDate}
                  onChange={(e) => setFormData({ ...formData, birthDate: e.target.value })}
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-6 rounded-lg bg-gradient-to-r from-purple-600 to-blue-600 text-white font-medium hover:from-purple-700 hover:to-blue-700 transition-colors duration-300 disabled:opacity-50"
              >
                {loading ? 'Analyzing...' : 'Reveal My Personality'}
              </button>
            </form>
          </motion.div>
        )}

        {step === 2 && analysis && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="max-w-4xl mx-auto bg-white/10 backdrop-blur-lg rounded-xl p-8 shadow-2xl text-white"
          >
            <h2 className="text-3xl font-bold mb-6">Your Numerological Profile</h2>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div className="bg-white/5 p-4 rounded-lg">
                <h3 className="text-lg font-semibold mb-1">Life Path Number</h3>
                <p className="text-3xl font-bold text-purple-300">{analysis.life_path_number}</p>
              </div>
              <div className="bg-white/5 p-4 rounded-lg">
                <h3 className="text-lg font-semibold mb-1">Destiny Number</h3>
                <p className="text-3xl font-bold text-purple-300">{analysis.destiny_number}</p>
              </div>
              <div className="bg-white/5 p-4 rounded-lg">
                <h3 className="text-lg font-semibold mb-1">Soul Urge Number</h3>
                <p className="text-3xl font-bold text-purple-300">{analysis.soul_urge_number}</p>
              </div>
              <div className="bg-white/5 p-4 rounded-lg">
                <h3 className="text-lg font-semibold mb-1">Personality Number</h3>
                <p className="text-3xl font-bold text-purple-300">{analysis.personality_number}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
              <div className="bg-white/5 p-4 rounded-lg">
                <h3 className="text-lg font-semibold mb-1">Birthday Number</h3>
                <p className="text-3xl font-bold text-purple-300">{analysis.birthday_number}</p>
              </div>
              <div className="bg-white/5 p-4 rounded-lg">
                <h3 className="text-lg font-semibold mb-1">Maturity Number</h3>
                <p className="text-3xl font-bold text-purple-300">{analysis.maturity_number}</p>
              </div>
              <div className="bg-white/5 p-4 rounded-lg">
                <h3 className="text-lg font-semibold mb-1">Personal Year</h3>
                <p className="text-3xl font-bold text-purple-300">{analysis.personal_year}</p>
              </div>
            </div>

            <div className="bg-white/5 p-4 rounded-lg mb-8">
              <h3 className="text-lg font-semibold mb-2">Karmic Lessons</h3>
              <div className="flex gap-2 flex-wrap">
                {analysis.karmic_lessons.map((lesson) => (
                  <span
                    key={lesson}
                    className="px-3 py-1 bg-purple-500/20 rounded-full text-purple-200"
                  >
                    {lesson}
                  </span>
                ))}
              </div>
            </div>

            <div className="prose prose-invert max-w-none">
              <div
                className="text-lg leading-relaxed"
                dangerouslySetInnerHTML={{ __html: analysis.analysis }}
              />
            </div>

            <button
              onClick={() => setStep(1)}
              className="mt-8 py-2 px-6 rounded-lg bg-purple-600 text-white hover:bg-purple-700 transition-colors duration-300"
            >
              Start New Analysis
            </button>
          </motion.div>
        )}

        {/* Ad Space */}
        <div className="mt-12 text-center">
          <ins
            className="adsbygoogle"
            style={{ display: 'block' }}
            data-ad-client="ca-pub-YOUR_CLIENT_ID"
            data-ad-slot="YOUR_AD_SLOT"
            data-ad-format="auto"
            data-full-width-responsive="true"
          ></ins>
        </div>
      </div>
    </main>
  );
}
