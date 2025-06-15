const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

app.use(express.json());

// Your credentials
const consumerKey = '8hYi846dzPSqBKAC3ZbEqkkJzOQFx95xnQLqIg6b2sL2thb0';
const consumerSecret = 'STITyxyFUIXAnCIVrRRueWnKV5wk3rZsfhxozk5wQzhoCwSAvBYLsPukttzvsPBh';
const shortCode = '5515738'; // Test Shortcode
const passkey = '3526578';

// Get access token
const getToken = async () => {
  const auth = Buffer.from(`${consumerKey}:${consumerSecret}`).toString('base64');
  const res = await axios.get('https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', {
    headers: {
      Authorization: `Basic ${auth}`
    }
  });
  return res.data.access_token;
};

app.post('/stkpush', async (req, res) => {
  const { phone, amount } = req.body;
  const token = await getToken();

  const timestamp = new Date().toISOString().replace(/[^0-9]/g, '').slice(0, 14);
  const password = Buffer.from(shortCode + passkey + timestamp).toString('base64');

  const payload = {
    BusinessShortCode: shortCode,
    Password: password,
    Timestamp: timestamp,
    TransactionType: 'CustomerPayBillOnline',
    Amount: amount,
    PartyA: phone,
    PartyB: shortCode,
    PhoneNumber: phone,
    CallBackURL: 'https://yourdomain.com/callback', // Replace with a live server endpoint
    AccountReference: 'ShopEase',
    TransactionDesc: 'Purchase on ShopEase'
  };

  try {
    const stkRes = await axios.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', payload, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    res.json({ success: true, message: 'STK Push Sent', response: stkRes.data });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Failed to push STK', error: error.response.data });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
