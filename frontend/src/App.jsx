import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './index.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
        <div className="flex space-x-8 mb-6">
          <a href="https://vite.dev" target="_blank" rel="noopener noreferrer">
            <img src={viteLogo} className="h-16 w-16" alt="Vite logo" />
          </a>
          <a href="https://react.dev" target="_blank" rel="noopener noreferrer">
            <img src={reactLogo} className="h-16 w-16" alt="React logo" />
          </a>
        </div>
        <h1 className="text-4xl font-bold text-blue-600 mb-4">Utilities Payment SaaS</h1>
        <div className="bg-white rounded-lg shadow p-6 w-full max-w-md flex flex-col items-center">
          <button className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded mb-4" onClick={() => setCount((count) => count + 1)}>
            Payment Link Demo (count: {count})
          </button>
          <p className="text-gray-700 mb-2">Send and manage utility payment links easily.</p>
          <p className="text-sm text-gray-400">Edit <code>src/App.jsx</code> and save to test HMR</p>
        </div>
        <p className="mt-6 text-gray-500 text-xs">Click on the Vite and React logos to learn more</p>
      </div>
    </>
  )
}

export default App
