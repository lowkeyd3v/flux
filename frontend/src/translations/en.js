export default {
  // Navigation & App Header
  appTitle: 'FLUX',
  appTagline: 'Adaptive intelligence for everyday commerce',
  navVendorDashboard: 'Vendor Dashboard',
  hackathonBadge: 'OOSC 4.0 · PS5',
  footerText: 'FLUX — AI for Public Good · Built for street vendors and micro-entrepreneurs',

  // Language Selector
  language: 'Language',
  langEnglish: 'English',
  langHindi: 'हिंदी (Hindi)',
  langHinglish: 'Hinglish',

  // Home Page
  homeHeroTitle: 'Welcome to',
  homeHeroDesc:
    'An AI-powered business intelligence assistant helping Indian street vendors and micro-entrepreneurs forecast demand, plan inventory, and access government schemes.',
  homeOpenDashboard: 'Open Vendor Dashboard & Schemes →',
  homeFeatureDemandTitle: 'Demand Forecasting',
  homeFeatureDemandDesc: 'ML-driven predictions for daily sales with uncertainty bounds.',
  homeFeatureRecTitle: 'Smart Recommendations',
  homeFeatureRecDesc: 'Actionable prep quantities, expected revenue, and weather awareness.',
  homeFeatureSchemeTitle: 'Scheme Assistant (RAG)',
  homeFeatureSchemeDesc: 'Grounded answers on PM SVANidhi, MUDRA, Vishwakarma, and subsidies.',
  homeFeatureVoiceTitle: 'Voice & Multilingual',
  homeFeatureVoiceDesc: 'Speak in Hindi or Hinglish with speech-to-text and audio readout.',
  homeExploreFeature: 'Explore feature →',
  statusLive: 'Live',

  // Health Card
  backendStatus: 'Backend Status',
  backendConnected: 'Connected',
  backendDisconnected: 'Disconnected',
  dbConnected: 'Database connected and operational',
  dbDisconnected: 'Cannot connect to backend or database',

  // Vendor Page Headers
  vendorPageTitle: 'Vendor Dashboard & Schemes',
  vendorPageSub:
    'Create a business profile to track sales, forecast demand, and discover grounded government support schemes.',
  newVendorProfile: 'New Vendor Profile',
  yourVendors: 'Your Vendors',
  loadingVendors: 'Loading vendors...',
  errorLoadingVendors: 'Could not load vendors. Is the backend running?',
  noVendorsYet: 'No vendors created yet. Fill out the form above to get started.',

  // Vendor Profile Form
  vendorNameLabel: 'Vendor Name *',
  vendorNamePlaceholder: 'e.g. Ramesh Kumar',
  productLabel: 'Product *',
  productPlaceholder: 'e.g. Samosa, Chaat, Tea',
  locationLabel: 'Location *',
  locationPlaceholder: 'e.g. Prayagraj, Lucknow, Delhi',
  sellingPriceLabel: 'Selling Price (₹) *',
  sellingPricePlaceholder: 'e.g. 10',
  currentInventoryLabel: 'Current Inventory (units)',
  currentInventoryPlaceholder: 'e.g. 50',
  budgetLabel: 'Daily Budget (₹)',
  budgetPlaceholder: 'e.g. 2000',
  btnCreateVendor: 'Create Vendor Profile',
  btnCreatingVendor: 'Creating...',

  // Vendor List Card
  unitPrice: '₹{price}/unit',
  inStock: '{qty} in stock',
  budgetAmount: '₹{amount} budget',
  btnSelected: 'Selected',
  btnSelect: 'Select Vendor',

  // Sales Records
  salesHistoryTitle: 'Sales History — {name}',
  salesHistorySub: 'Log historical daily sales. This data powers demand forecasting.',
  logSalesTitle: 'Log Daily Sales',
  dateLabel: 'Date',
  unitsSoldLabel: 'Units Sold',
  revenueLabel: 'Revenue (₹)',
  notesLabel: 'Notes / Weather observation (optional)',
  notesPlaceholder: 'e.g. Heavy rain in the evening, sales dipped',
  btnAddRecord: 'Add Record',
  btnAddBulk: 'Bulk Upload CSV / JSON',
  noSalesRecords: 'No sales records logged yet. Add your first record above.',
  thDate: 'Date',
  thUnitsSold: 'Units Sold',
  thRevenue: 'Revenue',
  thNotes: 'Notes',
  thAction: 'Action',
  btnDelete: 'Delete',

  // Demand Prediction Card
  demandPredictionTitle: 'Demand Prediction — {name}',
  demandPredictionSub: 'Get an ML-driven forecast for a specific day, adjusted for weather and holidays.',
  targetDateLabel: 'Target Date',
  holidayEventLabel: 'Festival / Local Event Day',
  weatherConditionLabel: 'Expected Weather Condition',
  weatherClear: 'Clear / Sunny',
  weatherCloudy: 'Cloudy',
  weatherRain: 'Rain / Wet',
  weatherExtremeHeat: 'Extreme Heat (>40°C)',
  btnPredict: 'Predict Demand',
  btnPredicting: 'Forecasting...',
  predictionResultTitle: 'Forecasted Demand',
  expectedUnits: '{qty} units',
  predictionRange: 'Likely range: {low} – {high} units',
  confidenceScore: 'Confidence: {score}%',
  modelVersion: 'Model: {version}',

  // Recommendation Card
  recommendationTitle: 'Smart Recommendation — {name}',
  recommendationSub:
    'How much to prepare, expected revenue, and risk — combining the demand forecast with your inventory, budget, and local weather.',
  autoWeatherCheckbox: 'Auto-fetch live weather (OpenWeatherMap)',
  manualWeatherCheckbox: 'Enter weather manually',
  tempCelsiusLabel: 'Temperature (°C)',
  btnGetRecommendation: 'Get Recommendation',
  btnGettingRecommendation: 'Calculating...',
  prepQuantityTitle: 'Recommended Preparation',
  prepUnits: '{qty} units to prepare',
  expectedRevenueTitle: 'Expected Revenue',
  estSurplusShortageTitle: 'Surplus / Shortage',
  riskRatingTitle: 'Risk Level',
  riskLow: 'Low Risk',
  riskMedium: 'Moderate Risk',
  riskHigh: 'High Risk',
  weatherSourceAuto: 'Live Forecast ({temp}°C, {condition})',
  weatherSourceManual: 'Manual Weather ({temp}°C, {condition})',
  weatherSourceUnavailable: 'Default Neutral Weather (27°C, Clear)',

  // Scheme Recommendations
  recommendedSchemesTitle: 'Recommended Government Schemes — {name}',
  recommendedSchemesSub:
    'Personalized subsidies, loans, and welfare benefits matched to your {product} business in {location}.',
  matchReasonLabel: 'Why this matches:',
  recommendedActionLabel: 'Action Step:',
  btnViewSchemeDetails: 'View Scheme Details & How to Apply →',

  // Scheme Assistant (RAG)
  schemeAssistantTitle: 'FLUX Scheme Assistant',
  schemeAssistantSub:
    'Ask natural-language questions about government schemes (PM SVANidhi, MUDRA, Vishwakarma, e-Shram). Answers are strictly grounded in official documents with source citations.',
  assistantInputPlaceholder: 'Ask a question in English, Hindi, or Hinglish... or click 🎙️ to speak',
  btnAsk: 'Ask Assistant',
  btnAsking: 'Searching scheme documents...',
  suggestedQuestions: 'SUGGESTED QUESTIONS:',
  sourceCitationsTitle: 'Source Citations ({count})',
  suggestedFollowUpsTitle: 'Suggested Follow-Up Questions:',
  officialPortal: 'Official Portal',

  // Scheme Detail Modal
  modalClose: 'Close',
  targetAudience: 'Target Beneficiaries',
  keyEligibility: 'Key Eligibility Criteria',
  schemeBenefits: 'Financial Benefits & Subsidies',
  requiredDocs: 'Documents Required for Application',
  howToApply: 'Step-by-Step Application Process',
  maxBenefit: 'Max Benefit',
  subsidy: 'Subsidy',
  collateral: 'Collateral',
  collateralNotRequired: 'No Collateral Required',
  collateralRequired: 'Collateral Required',
  openOfficialPortal: 'Visit Official Portal →',

  // Voice & Speech UI
  voiceListening: 'Listening... Please speak now',
  voiceSpeakNow: 'Click microphone to speak',
  voiceNotSupported: 'Speech recognition is not supported in this browser.',
  btnReadAloud: 'Read Aloud (TTS)',
  btnStopReading: 'Stop Reading',
  voiceQueryError: 'Could not capture speech. Please try again.',
}
