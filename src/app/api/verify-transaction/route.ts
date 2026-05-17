import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { txHash, email, telegram, expectedAmount } = body;

    // Simulate blockchain verification delay (e.g., calling TronGrid API or similar)
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Basic validation
    if (!txHash || txHash.length < 10) {
      return NextResponse.json(
        { success: false, message: 'Недійсний хеш транзакції. Перевірте та спробуйте ще раз.' },
        { status: 400 }
      );
    }

    // --- In a real scenario, you would do this here: ---
    // 1. Fetch transaction details from blockchain API using `txHash`
    // 2. Verify receiver address matches your wallet
    // 3. Verify amount matches `expectedAmount`
    // 4. Verify the transaction hasn't been processed before (DB check)
    // 5. If valid, send an email/telegram message with the product archive to `email` and `telegram`

    // For this mock, we assume success if txHash is provided and looks vaguely like a hash
    console.log(`[MOCK BLOCKCHAIN] Verified tx ${txHash} for ${expectedAmount}. Sending product to ${email} / ${telegram}`);

    return NextResponse.json({
      success: true,
      message: 'Транзакція успішно підтверджена.'
    });

  } catch (error) {
    console.error('Error verifying transaction:', error);
    return NextResponse.json(
      { success: false, message: 'Внутрішня помилка сервера при перевірці.' },
      { status: 500 }
    );
  }
}
