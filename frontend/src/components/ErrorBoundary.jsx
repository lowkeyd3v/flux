import { Component } from 'react'

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('[FLUX Error Boundary]', error, errorInfo)
  }

  handleReload = () => {
    window.location.reload()
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-neutral-50 flex items-center justify-center p-6">
          <div className="max-w-md w-full bg-white rounded-2xl border border-neutral-200 shadow-xl p-8 text-center">
            <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-red-50 text-red-600 flex items-center justify-center text-2xl font-bold border border-red-200">
              ⚠️
            </div>
            <h1 className="text-xl font-bold text-neutral-900 mb-2">
              Something went wrong / कुछ गलत हो गया
            </h1>
            <p className="text-sm text-neutral-600 mb-6">
              An unexpected error occurred in the application. Please refresh the page to continue.
            </p>
            {this.state.error && (
              <pre className="bg-neutral-100 p-3 rounded-lg text-xs text-red-600 overflow-x-auto text-left mb-6 font-mono">
                {this.state.error.toString()}
              </pre>
            )}
            <button
              onClick={this.handleReload}
              className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2.5 px-4 rounded-xl transition cursor-pointer"
            >
              🔄 Refresh Page / पेज रीफ्रेश करें
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
