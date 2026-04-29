exports.handler = async function(event, context) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { messages } = JSON.parse(event.body);

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 200,
        system: `You are a helpful assistant for Coastal Cash Offer, a cash home buying company serving Southern California — Orange County, San Diego, and Los Angeles. We buy houses for cash throughout SoCal including Irvine, Mission Viejo, Newport Beach, Laguna Hills, Lake Forest, San Clemente, San Juan Capistrano, Aliso Viejo, Huntington Beach, Tustin, Fountain Valley, San Diego, Los Angeles and all surrounding cities. Phone: 949-280-5139. No repairs needed, no fees, no commissions. Cash offers within 24 hours, close in 7 days. Keep responses SHORT — 2-3 sentences max. Be warm, friendly, and California casual. Always guide sellers toward filling out the form or calling 949-280-5139.`,
        messages: messages
      })
    });

    const data = await response.json();

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({ reply: data.content[0].text })
    };

  } catch(err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message })
    };
  }
};
