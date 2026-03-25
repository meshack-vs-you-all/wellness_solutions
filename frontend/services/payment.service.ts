import api from './api';

export interface CheckoutSessionResponse {
  checkout_url: string;
  params?: any; // For Flutterwave Standard
}

export const paymentService = {
  createCheckoutSession: async (itemType: 'booking' | 'package', itemId: number, gateway: 'stripe' | 'flutterwave' = 'flutterwave'): Promise<CheckoutSessionResponse> => {
    const response = await api.post<CheckoutSessionResponse>('/payments/checkout-session/', {
      item_type: itemType,
      item_id: itemId,
      gateway: gateway,
    });
    return response.data;
  },
};
