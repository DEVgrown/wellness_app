import { reactive, computed } from 'vue';

const state = reactive({
  currency: 'KES', // 'KES' or 'EUR'
  user: {
    name: 'Sarah',
    email: 'sarah@example.com',
    phone: '+254 712 345 678',
    avatar: 'https://lh3.googleusercontent.com/aida/AEtjO1UwxvO7_3GTbgWd4EMPt4rt_w381oAezID3bV9-NdwIdn55FZ_9EuUxkek0b1g_CCD7OREkS7yHj5Cgb747yd7hji3o7wMsF5yMWX7Y-9WXeuNJSV87pRW9T6yotkdPzul6-kYjIysNWHJ6rcSRnoCnngzil7rsid2c6iewLxqYX2u5vPcQFLY7r3ZEkPxwmhnE8RfShmfVHjQTEbYJSi9MwKlsQzRFBydQI4ftgATXc7O0xLaTmJmS44Z2gA8121FAes4FrKhN'
  },
  draftBooking: {
    serviceId: null,
    serviceTitle: '1:1 Pilates Reformer',
    date: '2024-10-26',
    dateDisplay: 'Saturday, 26 Oct 2024',
    timeSlot: '09:30 AM',
    locationName: 'Karen Studio, Nairobi',
    basePriceKes: 6500,
    basePriceEur: 75,
    isPackApplied: false,
    packPriceKes: 27600,
    packPriceEur: 190,
  },
  toastMessage: null,
  toastType: 'info'
});

export const useBookingStore = () => {
  const currency = computed(() => state.currency);
  const user = computed(() => state.user);
  const draft = computed(() => state.draftBooking);
  const toastMessage = computed(() => state.toastMessage);
  const toastType = computed(() => state.toastType);

  const currentPrice = computed(() => {
    if (state.draftBooking.isPackApplied) {
      return state.currency === 'KES' ? state.draftBooking.packPriceKes : state.draftBooking.packPriceEur;
    }
    return state.currency === 'KES' ? state.draftBooking.basePriceKes : state.draftBooking.basePriceEur;
  });

  const formattedPrice = computed(() => {
    const val = currentPrice.value;
    if (state.currency === 'KES') {
      return `KES ${val.toLocaleString()}`;
    }
    return `€${val}`;
  });

  function setCurrency(curr) {
    state.currency = curr;
  }

  function setDraftService(service) {
    state.draftBooking.serviceId = service.id;
    state.draftBooking.serviceTitle = service.title;
    state.draftBooking.basePriceKes = service.price_kes || 6500;
    state.draftBooking.basePriceEur = service.price_eur || 75;
    state.draftBooking.packPriceKes = Math.round((service.price_kes || 6500) * 5 * 0.85);
    state.draftBooking.packPriceEur = Math.round((service.price_eur || 75) * 5 * 0.85);
    state.draftBooking.isPackApplied = false;
    if (service.location_display) {
      state.draftBooking.locationName = service.location_display;
    }
  }

  function setDraftSchedule(date, dateDisplay, timeSlot) {
    state.draftBooking.date = date;
    state.draftBooking.dateDisplay = dateDisplay;
    state.draftBooking.timeSlot = timeSlot;
  }

  function togglePack() {
    state.draftBooking.isPackApplied = !state.draftBooking.isPackApplied;
  }

  function showToast(message, type = 'info', duration = 3000) {
    state.toastMessage = message;
    state.toastType = type;
    setTimeout(() => {
      if (state.toastMessage === message) {
        state.toastMessage = null;
      }
    }, duration);
  }

  return {
    state,
    currency,
    user,
    draft,
    currentPrice,
    formattedPrice,
    toastMessage,
    toastType,
    setCurrency,
    setDraftService,
    setDraftSchedule,
    togglePack,
    showToast
  };
};
