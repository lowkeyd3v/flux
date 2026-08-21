import { useHealthCheck } from '../hooks/useHealthCheck'
import { useLanguage } from '../context/LanguageContext'

const STATUS_STYLES = {
  loading: 'bg-neutral-100 text-neutral-600 border-neutral-300',
  ok: 'bg-green-50 text-green-700 border-green-300',
  error: 'bg-red-50 text-red-700 border-red-300',
}

export default function HealthStatusCard() {
  const { status, data, error, refetch } = useHealthCheck()
  const { t } = useLanguage()

  return (
    <div className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-semibold text-neutral-800">{t('backendStatus')}</h2>
        <button
          onClick={refetch}
          className="text-xs px-2.5 py-1 rounded-md border border-neutral-300 hover:bg-neutral-50 transition cursor-pointer"
        >
          🔄 Refresh
        </button>
      </div>

      <div
        className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-sm font-medium ${STATUS_STYLES[status]}`}
      >
        <span
          className={`h-2 w-2 rounded-full ${
            status === 'ok'
              ? 'bg-green-500'
              : status === 'error'
              ? 'bg-red-500'
              : 'bg-neutral-400 animate-pulse'
          }`}
        />
        {status === 'loading' && 'Checking backend...'}
        {status === 'ok' && t('backendConnected')}
        {status === 'error' && t('backendDisconnected')}
      </div>

      {status === 'ok' && (
        <p className="mt-2 text-xs text-green-700">{t('dbConnected')}</p>
      )}

      {status === 'ok' && data && (
        <pre className="mt-3 text-xs bg-neutral-50 rounded-md p-3 overflow-x-auto text-neutral-600">
          {JSON.stringify(data, null, 2)}
        </pre>
      )}

      {status === 'error' && (
        <p className="mt-3 text-xs text-red-600">
          {error?.message || t('dbDisconnected')}
        </p>
      )}
    </div>
  )
}
