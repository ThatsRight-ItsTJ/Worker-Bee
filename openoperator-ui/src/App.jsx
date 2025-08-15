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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <div className="w-12 h-12 bg-indigo-600 rounded-lg mr-3 flex items-center justify-center text-white font-bold text-xl">🤖</div>
            <h1 className="text-4xl font-bold text-gray-800">OpenOperator</h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            AI-powered web automation and information extraction. 
            Analyze any website with natural language queries.
          </p>
          <div className="flex items-center justify-center mt-4 text-sm text-gray-500">
            <span className="mr-1">🌐</span>
            <span>Powered by Pollinations AI • Free & Unlimited</span>
          </div>
        </div>

        {/* Main Form */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* URL Input */}
              <div>
                <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
                  Website URL
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">🌐</span>
                  <input
                    type="url"
                    id="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://example.com"
                    className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                    required
                  />
                </div>
              </div>

              {/* Query Input */}
              <div>
                <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
                  What would you like to know?
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-4 text-gray-400">🔍</span>
                  <textarea
                    id="query"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="What is the main topic of this website? Extract contact information. Find pricing details..."
                    rows={3}
                    className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none"
                    required
                  />
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white font-medium py-3 px-6 rounded-lg transition-colors flex items-center justify-center"
              >
                {isLoading ? (
                  <>
                    <div className="w-5 h-5 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Analyzing Website...
                  </>
                ) : (
                  <>
                    <span className="mr-2">🤖</span>
                    Analyze Website
                  </>
                )}
              </button>
            </form>

            {/* Example Queries */}
            <div className="mt-8 pt-6 border-t border-gray-200">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Try these examples:</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <button
                  onClick={() => handleExample('https://example.com', 'What is the title and main content of this page?')}
                  className="text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <div className="text-sm font-medium text-indigo-600">Basic Page Analysis</div>
                  <div className="text-xs text-gray-500">Extract title and content from example.com</div>
                </button>
                <button
                  onClick={() => handleExample('https://github.com/microsoft/playwright', 'What is this project about and what are its main features?')}
                  className="text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <div className="text-sm font-medium text-indigo-600">Project Information</div>
                  <div className="text-xs text-gray-500">Analyze GitHub repository details</div>
                </button>
              </div>
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <div className="flex items-center">
                <span className="text-red-500 mr-2">❌</span>
                <span className="text-red-700 font-medium">Error</span>
              </div>
              <p className="text-red-600 mt-1">{error}</p>
            </div>
          )}

          {/* Results Display */}
          {result && (
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <div className="flex items-center mb-6">
                <span className="text-green-500 mr-2 text-xl">✅</span>
                <h2 className="text-2xl font-bold text-gray-800">Analysis Complete</h2>
              </div>

              {/* Operations Summary */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-700 mb-2">Operations Summary</h3>
                <p className="text-gray-600 bg-gray-50 p-4 rounded-lg">{result.ops_summary}</p>
              </div>

              {/* Main Answer */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-700 mb-2">Answer</h3>
                <div className="prose max-w-none">
                  <p className="text-gray-800 leading-relaxed">{result.answer}</p>
                </div>
              </div>

              {/* Sources */}
              {result.sources && result.sources.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-700 mb-2">Sources</h3>
                  <div className="space-y-2">
                    {result.sources.map((source, index) => (
                      <a
                        key={index}
                        href={source}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center text-indigo-600 hover:text-indigo-800 transition-colors"
                      >
                        <span className="mr-2">🔗</span>
                        {source}
                      </a>
                    ))}
                  </div>
                </div>
              )}

              {/* Quotes */}
              {result.quotes && result.quotes.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-700 mb-2">Key Quotes</h3>
                  <div className="space-y-3">
                    {result.quotes.map((quote, index) => (
                      <blockquote key={index} className="border-l-4 border-indigo-200 pl-4 py-2 bg-indigo-50 rounded-r-lg">
                        <p className="text-gray-700 italic">"{quote}"</p>
                      </blockquote>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="text-center mt-16 text-gray-500">
          <p>Built with OpenOperator • Powered by Pollinations AI • Open Source</p>
        </footer>
      </div>
    </div>
  )
}

export default App