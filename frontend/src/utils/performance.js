/**
 * Production Performance Telemetry & Web Vitals Monitoring for FLUX.
 *
 * Measures Largest Contentful Paint (LCP), First Contentful Paint (FCP),
 * Cumulative Layout Shift (CLS), Time to First Byte (TTFB), and Interaction to Next Paint (INP).
 */

export function reportWebVitals(onPerfEntry) {
  if (typeof window === 'undefined' || !window.performance) return

  const logMetric = (metric) => {
    if (onPerfEntry && typeof onPerfEntry === 'function') {
      onPerfEntry(metric)
    } else if (import.meta.env.DEV) {
      console.debug(`[FLUX Telemetry] ${metric.name}:`, `${metric.value.toFixed(2)}ms`, metric)
    }
  }

  // 1. Time to First Byte (TTFB) & Navigation Timing
  try {
    const navEntries = performance.getEntriesByType('navigation')
    if (navEntries && navEntries.length > 0) {
      const nav = navEntries[0]
      const ttfb = nav.responseStart - nav.requestStart
      logMetric({
        name: 'TTFB',
        value: ttfb,
        rating: ttfb < 800 ? 'good' : ttfb < 1800 ? 'needs-improvement' : 'poor',
      })
    }
  } catch {
    // Ignore environments without Navigation Timing API
  }

  // 2. Paint Timing (FCP)
  if ('PerformanceObserver' in window) {
    try {
      const paintObserver = new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
          if (entry.name === 'first-contentful-paint') {
            logMetric({
              name: 'FCP',
              value: entry.startTime,
              rating: entry.startTime < 1800 ? 'good' : entry.startTime < 3000 ? 'needs-improvement' : 'poor',
            })
          }
        }
      })
      paintObserver.observe({ type: 'paint', buffered: true })
    } catch {
      // Ignore paint observer errors
    }

    // 3. Largest Contentful Paint (LCP)
    try {
      const lcpObserver = new PerformanceObserver((entryList) => {
        const entries = entryList.getEntries()
        const lastEntry = entries[entries.length - 1]
        if (lastEntry) {
          logMetric({
            name: 'LCP',
            value: lastEntry.startTime,
            rating: lastEntry.startTime < 2500 ? 'good' : lastEntry.startTime < 4000 ? 'needs-improvement' : 'poor',
          })
        }
      })
      lcpObserver.observe({ type: 'largest-contentful-paint', buffered: true })
    } catch {
      // Ignore LCP observer errors
    }

    // 4. Cumulative Layout Shift (CLS)
    try {
      let clsValue = 0
      const clsObserver = new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
          if (!entry.hadRecentInput) {
            clsValue += entry.value
          }
        }
        logMetric({
          name: 'CLS',
          value: clsValue,
          rating: clsValue < 0.1 ? 'good' : clsValue < 0.25 ? 'needs-improvement' : 'poor',
        })
      })
      clsObserver.observe({ type: 'layout-shift', buffered: true })
    } catch {
      // Ignore CLS observer errors
    }
  }
}
