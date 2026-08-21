export default {
  // Navigation & App Header
  appTitle: 'FLUX',
  appTagline: 'Everyday business ke liye smart AI assistant',
  navVendorDashboard: 'Vendor Dashboard',
  hackathonBadge: 'OOSC 4.0 · PS5',
  footerText: 'FLUX — AI for Public Good · Indian street vendors aur micro-entrepreneurs ke liye',

  // Language Selector
  language: 'Language',
  langEnglish: 'English',
  langHindi: 'हिंदी (Hindi)',
  langHinglish: 'Hinglish (हिंदी)',

  // Home Page
  homeHeroTitle: 'Welcome to',
  homeHeroDesc:
    'Indian street vendors aur dukandaro ke liye AI business assistant — demand forecast karein, stock plan karein aur sarkari schemes ka fayda uthayein.',
  homeOpenDashboard: 'Vendor Dashboard & Schemes Kholein →',
  homeFeatureDemandTitle: 'Demand Forecasting (ML)',
  homeFeatureDemandDesc: 'Mausam aur events ke hisaab se daily sales ka accurate prediction.',
  homeFeatureRecTitle: 'Smart Prep Recommendations',
  homeFeatureRecDesc: 'Kitna maal banana chahiye, expected kamai aur risk ki clear summary.',
  homeFeatureSchemeTitle: 'Scheme Assistant (RAG)',
  homeFeatureSchemeDesc: 'PM SVANidhi, MUDRA, Vishwakarma loans aur subsidies ki grounded jaankari.',
  homeFeatureVoiceTitle: 'Voice & Multilingual',
  homeFeatureVoiceDesc: 'Hindi ya Hinglish me bolkar poochein aur voice audio me jawab sunein.',
  homeExploreFeature: 'Feature dekhein →',
  statusLive: 'Live',

  // Health Card
  backendStatus: 'Backend Status',
  backendConnected: 'Connected (Sab theek hai)',
  backendDisconnected: 'Disconnected',
  dbConnected: 'Database successfully connected hai',
  dbDisconnected: 'Backend ya database se connection nahi ho pa raha hai',

  // Vendor Page Headers
  vendorPageTitle: 'Vendor Dashboard & Schemes',
  vendorPageSub:
    'Sales record karne, demand forecast dekhne aur matching schemes find karne ke liye profile banayein.',
  newVendorProfile: 'Naya Vendor Profile',
  yourVendors: 'Aapke Registered Vendors',
  loadingVendors: 'Vendors load ho rahe hain...',
  errorLoadingVendors: 'Vendors load nahi ho sake. Kya backend run ho raha hai?',
  noVendorsYet: 'Abhi tak koi vendor nahi bana hai. Start karne ke liye upar form bharein.',

  // Vendor Profile Form
  vendorNameLabel: 'Vendor ka Naam *',
  vendorNamePlaceholder: 'e.g. Ramesh Kumar',
  productLabel: 'Product / Item *',
  productPlaceholder: 'e.g. Samosa, Chaat, Chai',
  locationLabel: 'Location / Sheher *',
  locationPlaceholder: 'e.g. Prayagraj, Lucknow, Delhi',
  sellingPriceLabel: 'Bikri Price (₹) *',
  sellingPricePlaceholder: 'e.g. 10',
  currentInventoryLabel: 'Current Stock (units)',
  currentInventoryPlaceholder: 'e.g. 50',
  budgetLabel: 'Daily Budget (₹)',
  budgetPlaceholder: 'e.g. 2000',
  btnCreateVendor: 'Vendor Profile Banayein',
  btnCreatingVendor: 'Creating...',

  // Vendor List Card
  unitPrice: '₹{price}/unit',
  inStock: '{qty} stock me hai',
  budgetAmount: '₹{amount} budget',
  btnSelected: 'Selected',
  btnSelect: 'Select Karein',

  // Sales Records
  salesHistoryTitle: 'Sales History — {name}',
  salesHistorySub: 'Daily sales log karein. Is data se future demand prediction aur accurate hoga.',
  logSalesTitle: 'Daily Sales Log Karein',
  dateLabel: 'Date',
  unitsSoldLabel: 'Units Sold (Kitna bika)',
  revenueLabel: 'Total Kamai (₹)',
  notesLabel: 'Notes / Mausam observation (optional)',
  notesPlaceholder: 'e.g. Shaam ko baarish hui thi, bikri thodi kam rahi',
  btnAddRecord: 'Record Add Karein',
  btnAddBulk: 'Bulk Upload CSV / JSON',
  noSalesRecords: 'Abhi tak koi sales record nahi hai. Upar apna pehla record add karein.',
  thDate: 'Date',
  thUnitsSold: 'Units Sold',
  thRevenue: 'Kamai',
  thNotes: 'Notes',
  thAction: 'Action',
  btnDelete: 'Delete',

  // Demand Prediction Card
  demandPredictionTitle: 'Demand Prediction — {name}',
  demandPredictionSub: 'Mausam aur holidays ko calculate karke aane wale din ka sales estimate lein.',
  targetDateLabel: 'Target Date',
  holidayEventLabel: 'Festival / Local Event Day',
  weatherConditionLabel: 'Mausam Condition',
  weatherClear: 'Clear / Dhoop (Clear)',
  weatherCloudy: 'Baadal (Cloudy)',
  weatherRain: 'Baarish (Rain)',
  weatherExtremeHeat: 'Tez Garmi (>40°C)',
  btnPredict: 'Demand Predict Karein',
  btnPredicting: 'Calculating...',
  predictionResultTitle: 'Predicted Demand',
  expectedUnits: '{qty} units',
  predictionRange: 'Expected range: {low} – {high} units',
  confidenceScore: 'Confidence: {score}%',
  modelVersion: 'Model: {version}',

  // Recommendation Card
  recommendationTitle: 'Smart Preparation Advice — {name}',
  recommendationSub:
    'Kitna stock banana chahiye, expected kamai aur risk level — demand forecast, stock, budget aur mausam ke according.',
  autoWeatherCheckbox: 'Live mausam auto-fetch karein (OpenWeatherMap)',
  manualWeatherCheckbox: 'Mausam manually enter karein',
  tempCelsiusLabel: 'Temperature (°C)',
  btnGetRecommendation: 'Preparation Advice Lein',
  btnGettingRecommendation: 'Calculating advice...',
  prepQuantityTitle: 'Recommended Preparation',
  prepUnits: '{qty} units banayein',
  expectedRevenueTitle: 'Expected Kamai',
  estSurplusShortageTitle: 'Surplus / Shortage Estimate',
  riskRatingTitle: 'Risk Level',
  riskLow: 'Low Risk (Safe)',
  riskMedium: 'Medium Risk',
  riskHigh: 'High Risk (Savdhani)',
  weatherSourceAuto: 'Live Mausam ({temp}°C, {condition})',
  weatherSourceManual: 'Manual Mausam ({temp}°C, {condition})',
  weatherSourceUnavailable: 'Normal Mausam (27°C, Clear)',

  // Scheme Recommendations
  recommendedSchemesTitle: 'Aapke Business ke Liye Matching Sarkari Schemes — {name}',
  recommendedSchemesSub:
    '{location} me aapke {product} kaam ke liye tailored loan, subsidy aur welfare schemes.',
  matchReasonLabel: 'Ye scheme aapke liye kyu best hai:',
  recommendedActionLabel: 'Next Step:',
  btnViewSchemeDetails: 'Scheme Details & Apply Kaise Karein Dekhein →',

  // Scheme Assistant (RAG)
  schemeAssistantTitle: 'FLUX Sarkari Scheme Assistant',
  schemeAssistantSub:
    'Sarkari schemes (PM SVANidhi, MUDRA, Vishwakarma, e-Shram) ke baare me simple bhasha me poochein. Sabhi answers official documents se verified hain.',
  assistantInputPlaceholder: 'Scheme ke baare me kuch bhi poochein... ya 🎙️ press karke bolein',
  btnAsk: 'Poochein',
  btnAsking: 'Official documents search ho rahe hain...',
  suggestedQuestions: 'SUGGESTED QUESTIONS:',
  sourceCitationsTitle: 'Official Sources & References ({count})',
  suggestedFollowUpsTitle: 'Related Questions Jo Aap Pooch Sakte Hain:',
  officialPortal: 'Official Portal',

  // Scheme Detail Modal
  modalClose: 'Close',
  targetAudience: 'Kaun Apply Kar Sakta Hai',
  keyEligibility: 'Eligibility Criteria',
  schemeBenefits: 'Benefits & Subsidies',
  requiredDocs: 'Zaroori Documents',
  howToApply: 'Step-by-Step Apply Karne Ka Tarika',
  maxBenefit: 'Max Benefit',
  subsidy: 'Subsidy',
  collateral: 'Collateral / Guarantee',
  collateralNotRequired: 'Bina Kisi Guarantee Ke (No Collateral)',
  collateralRequired: 'Guarantee Required',
  openOfficialPortal: 'Official Website Kholein →',

  // Voice & Speech UI
  voiceListening: 'Sun rahe hain... Ab bolein',
  voiceSpeakNow: 'Bolne ke liye mic dabayein',
  voiceNotSupported: 'Is browser me voice speech recognition supported nahi hai.',
  btnReadAloud: 'Bolkar Sunein (Audio)',
  btnStopReading: 'Stop Karein',
  voiceQueryError: 'Aapki voice record nahi ho saki. Please dubara try karein.',
}
