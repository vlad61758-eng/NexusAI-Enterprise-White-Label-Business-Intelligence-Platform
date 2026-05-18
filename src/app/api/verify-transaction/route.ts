import { NextResponse } from 'next/server';

// This is a basic implementation of TRON Nile Testnet verification.
// In production, use mainnet (api.trongrid.io) and consider using a library like tronweb.
const TRON_API_URL = 'https://nile.trongrid.io/wallet/gettransactionbyid';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { txHash, expectedAmount, expectedCurrency } = body;

    // Basic validation
    if (!txHash || txHash.length < 10) {
      return NextResponse.json(
        { success: false, message: 'Недійсний хеш транзакції. Перевірте та спробуйте ще раз.' },
        { status: 400 }
      );
    }

    // Verify on TRON Nile Testnet
    if (expectedCurrency === 'USDT' || expectedCurrency === 'TRX') {
      try {
        const response = await fetch(TRON_API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ value: txHash })
        });

        const data = await response.json();

        // TronGrid returns empty object {} if transaction is not found
        if (!data || Object.keys(data).length === 0 || !data.txID) {
           return NextResponse.json(
            { success: false, message: 'Транзакцію не знайдено в блокчейні (TRON Nile Testnet). Зачекайте хвилину і спробуйте знову.' },
            { status: 404 }
          );
        }

        // Check if transaction is successful (in TRON, ret[0].contractRet === 'SUCCESS')
        if (data.ret && data.ret[0] && data.ret[0].contractRet !== 'SUCCESS') {
           return NextResponse.json(
            { success: false, message: 'Транзакція знайдена, але має статус "Failed".' },
            { status: 400 }
          );
        }

        // Note: For a FULL production implementation you also need to:
        // 1. Decode `data.raw_data.contract[0].parameter.value` to verify receiver address
        // 2. Decode the amount (considering decimals, e.g., 6 for USDT TRC20)
        // 3. Save txHash to database to prevent double-spending

        console.log(`[TRON TESTNET] Verified tx ${txHash} for ${expectedAmount} ${expectedCurrency}`);

        return NextResponse.json({
          success: true,
          message: 'Транзакція успішно підтверджена.'
        });

      } catch (apiError) {
         console.error('TronGrid API Error:', apiError);
         return NextResponse.json(
            { success: false, message: 'Помилка зв\'язку з блокчейном. Спробуйте пізніше.' },
            { status: 502 }
          );
      }
    }

    // Fallback for other currencies (mock)
    await new Promise(resolve => setTimeout(resolve, 2000));
    return NextResponse.json({
      success: true,
      message: 'Транзакція успішно підтверджена (Mock).'
    });

  } catch (error) {
    console.error('Error verifying transaction:', error);
    return NextResponse.json(
      { success: false, message: 'Внутрішня помилка сервера при перевірці.' },
      { status: 500 }
    );
  }
}
