import { useState } from 'react'
import './App.css'

function App() {
  const [url, setUrl] = useState('')
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!url || !query) {
      setError('Please provide both URL and query')
      return
    }

    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      // This would call your Python backend
      const apiUrl = import.meta.env.PROD 
        ? '/api/analyze' 
        : 'http://localhost:5000/api/analyze';
        
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url, query }),
      })

      if (!response.ok) {
        throw new Error('Failed to analyze website')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleExample = (exampleUrl, exampleQuery) => {
    setUrl(exampleUrl)
    setQuery(exampleQuery)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-yellow-50 to-orange-100">
      {/* Floating bee decorations */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 text-4xl animate-bounce" style={{animationDelay: '0s'}}>🐝</div>
        <div className="absolute top-40 right-20 text-2xl animate-bounce" style={{animationDelay: '2s'}}>🌻</div>
        <div className="absolute bottom-40 left-20 text-3xl animate-bounce" style={{animationDelay: '4s'}}>🌼</div>
        <div className="absolute top-60 right-10 text-2xl animate-bounce" style={{animationDelay: '1s'}}>🐝</div>
        <div className="absolute bottom-20 right-40 text-3xl animate-bounce" style={{animationDelay: '3s'}}>🌺</div>
      </div>

      <div className="container mx-auto px-4 py-8 relative z-10">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <div className="relative">
              <div className="w-20 h-20 bg-gradient-to-br from-yellow-400 to-amber-500 rounded-full mr-4 flex items-center justify-center text-4xl shadow-lg transform hover:scale-110 transition-transform">
                🐝
              </div>
              <div className="absolute -top-2 -right-2 text-2xl animate-spin" style={{animationDuration: '3s'}}>✨</div>
            </div>
            <div>
              <h1 className="text-5xl font-bold bg-gradient-to-r from-amber-600 to-yellow-600 bg-clip-text text-transparent">
                Worker Bee
              </h1>
              <div className="text-lg text-amber-700 font-medium">🍯 Buzzing with AI Intelligence</div>
            </div>
          </div>
          
          <p className="text-xl text-gray-700 max-w-3xl mx-auto leading-relaxed mb-6">
            Like a busy bee collecting nectar from flowers, Worker Bee gathers information from any website. 
            Our AI-powered automation <span className="font-semibold text-amber-700">pollinates</span> the web with intelligent analysis.
          </p>
          
          <div className="flex items-center justify-center space-x-6 text-sm text-gray-600">
            <div className="flex items-center">
              <span className="mr-2 text-lg">🌸</span>
              <span>Powered by Pollinations AI</span>
            </div>
            <div className="flex items-center">
              <span className="mr-2 text-lg">🆓</span>
              <span>Free & Unlimited</span>
            </div>
            <div className="flex items-center">
              <span className="mr-2 text-lg">⚡</span>
              <span>Lightning Fast</span>
            </div>
          </div>
        </div>

        {/* Main Form */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-8 mb-8 border border-yellow-200">
            <div className="text-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-2">🌻 Let Worker Bee Gather Information</h2>
              <p className="text-gray-600">Enter any website URL and tell us what nectar of knowledge you seek!</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* URL Input */}
              <div>
                <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
                  🌐 Website URL (The Flower Garden)
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 transform -translate-y-1/2 text-amber-500 text-xl">🌸</span>
                  <input
                    type="url"
                    id="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://example.com"
                    className="w-full pl-14 pr-4 py-4 border-2 border-yellow-200 rounded-xl focus:ring-2 focus:ring-amber-400 focus:border-amber-400 transition-all bg-white/80 text-lg"
                    required
                  />
                </div>
              </div>

              {/* Query Input */}
              <div>
                <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
                  🔍 What Information Do You Need? (The Nectar You Seek)
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-4 text-amber-500 text-xl">🍯</span>
                  <textarea
                    id="query"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="What is the main topic of this website? Extract contact information. Find pricing details..."
                    rows={4}
                    className="w-full pl-14 pr-4 py-4 border-2 border-yellow-200 rounded-xl focus:ring-2 focus:ring-amber-400 focus:border-amber-400 transition-all resize-none bg-white/80 text-lg"
                    required
                  />
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-600 hover:to-yellow-600 disabled:from-amber-300 disabled:to-yellow-300 text-white font-bold py-4 px-8 rounded-xl transition-all transform hover:scale-105 disabled:scale-100 shadow-lg text-lg"
              >
                {isLoading ? (
                  <>
                    <div className="inline-flex items-center">
                      <div className="w-6 h-6 mr-3 border-3 border-white border-t-transparent rounded-full animate-spin"></div>
                      🐝 Worker Bee is Buzzing Around the Web...
                    </div>
                  </>
                ) : (
                  <>
                    <span className="mr-3">🐝</span>
                    Send Worker Bee to Collect Information
                    <span className="ml-3">🍯</span>
                  </>
                )}
              </button>
            </form>

            {/* Example Queries */}
            <div className="mt-8 pt-6 border-t border-yellow-200">
              <h3 className="text-lg font-semibold text-gray-700 mb-4 text-center">🌻 Try These Flower Gardens:</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button
                  onClick={() => handleExample('https://example.com', 'What is the title and main content of this page?')}
                  className="text-left p-4 bg-gradient-to-r from-yellow-50 to-amber-50 hover:from-yellow-100 hover:to-amber-100 rounded-xl transition-all border border-yellow-200 hover:border-amber-300 transform hover:scale-105"
                >
                  <div className="text-base font-semibold text-amber-700 mb-1">🌼 Basic Page Analysis</div>
                  <div className="text-sm text-gray-600">Extract title and content from example.com</div>
                </button>
                <button
                  onClick={() => handleExample('https://github.com/microsoft/playwright', 'What is this project about and what are its main features?')}
                  className="text-left p-4 bg-gradient-to-r from-yellow-50 to-amber-50 hover:from-yellow-100 hover:to-amber-100 rounded-xl transition-all border border-yellow-200 hover:border-amber-300 transform hover:scale-105"
                >
                  <div className="text-base font-semibold text-amber-700 mb-1">🌻 Project Information</div>
                  <div className="text-sm text-gray-600">Analyze GitHub repository details</div>
                </button>
              </div>
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6 mb-6 shadow-lg">
              <div className="flex items-center">
                <span className="text-red-500 mr-3 text-2xl">🚫</span>
                <span className="text-red-700 font-semibold text-lg">Oops! Worker Bee Hit a Snag</span>
              </div>
              <p className="text-red-600 mt-2 text-base">{error}</p>
            </div>
          )}

          {/* Results Display */}
          {result && (
            <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-8 border border-green-200">
              <div className="flex items-center mb-6">
                <span className="text-green-500 mr-3 text-3xl">🍯</span>
                <h2 className="text-3xl font-bold text-gray-800">Sweet Success! Nectar Collected</h2>
                <span className="ml-3 text-2xl animate-bounce">🐝</span>
              </div>

              {/* Operations Summary */}
              <div className="mb-6">
                <h3 className="text-xl font-semibold text-gray-700 mb-3 flex items-center">
                  <span className="mr-2">📋</span>
                  Worker Bee's Journey
                </h3>
                <p className="text-gray-700 bg-amber-50 p-4 rounded-xl border border-amber-200">{result.ops_summary}</p>
              </div>

              {/* Main Answer */}
              <div className="mb-6">
                <h3 className="text-xl font-semibold text-gray-700 mb-3 flex items-center">
                  <span className="mr-2">🍯</span>
                  The Sweet Nectar (Your Answer)
                </h3>
                <div className="prose max-w-none">
                  <p className="text-gray-800 leading-relaxed bg-yellow-50 p-4 rounded-xl border border-yellow-200 text-lg">{result.answer}</p>
                </div>
              </div>

              {/* Sources */}
              {result.sources && result.sources.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-xl font-semibold text-gray-700 mb-3 flex items-center">
                    <span className="mr-2">🌸</span>
                    Flowers Visited (Sources)
                  </h3>
                  <div className="space-y-3">
                    {result.sources.map((source, index) => (
                      <a
                        key={index}
                        href={source}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center text-amber-600 hover:text-amber-800 transition-colors bg-amber-50 p-3 rounded-lg border border-amber-200 hover:border-amber-300"
                      >
                        <span className="mr-3 text-lg">🔗</span>
                        <span className="flex-1">{source}</span>
                        <span className="ml-2">🌻</span>
                      </a>
                    ))}
                  </div>
                </div>
              )}

              {/* Quotes */}
              {result.quotes && result.quotes.length > 0 && (
                <div>
                  <h3 className="text-xl font-semibold text-gray-700 mb-3 flex items-center">
                    <span className="mr-2">💬</span>
                    Golden Quotes (Key Findings)
                  </h3>
                  <div className="space-y-4">
                    {result.quotes.map((quote, index) => (
                      <blockquote key={index} className="border-l-4 border-amber-400 pl-6 py-3 bg-gradient-to-r from-amber-50 to-yellow-50 rounded-r-xl">
                        <p className="text-gray-700 italic text-lg">"{quote}"</p>
                        <div className="text-right mt-2">
                          <span className="text-amber-500">🌼</span>
                        </div>
                      </blockquote>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="text-center mt-16 text-gray-600">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <span className="text-2xl">🐝</span>
            <p className="text-lg">Built with Worker Bee • Powered by Pollinations AI • Open Source</p>
            <span className="text-2xl">🍯</span>
          </div>
          <p className="text-sm">Buzzing around the web, collecting knowledge one site at a time</p>
        </footer>
      </div>
    </div>
  )
}

export default App