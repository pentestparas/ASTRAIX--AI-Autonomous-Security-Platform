import { NextRequest, NextResponse } from 'next/server';
import http from 'http';
import https from 'https';

export async function POST(request: NextRequest) {
  const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:8000';
  const targetUrl = new URL('/api/v1/vapt/scan', backendUrl);

  try {
    const body = await request.json();
    const authHeader = request.headers.get('authorization');
    const bodyStr = JSON.stringify(body);

    const response = await new Promise<{ status: number; data: unknown }>((resolve, reject) => {
      const options = {
        hostname: targetUrl.hostname,
        port: targetUrl.port,
        path: targetUrl.pathname,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(bodyStr),
          ...(authHeader ? { Authorization: authHeader } : {}),
        },
        timeout: 600000,
      };

      const lib = targetUrl.protocol === 'https:' ? https : http;
      const req = lib.request(options, (res) => {
        let data = '';
        res.on('data', (chunk: string) => { data += chunk; });
        res.on('end', () => {
          try {
            resolve({ status: res.statusCode || 500, data: JSON.parse(data) });
          } catch {
            resolve({ status: res.statusCode || 500, data });
          }
        });
      });

      req.on('error', reject);
      req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
      req.write(bodyStr);
      req.end();
    });

    return NextResponse.json(response.data, { status: response.status });
  } catch (error) {
    console.error('VAPT scan proxy error:', error);
    return NextResponse.json(
      { success: false, error: error instanceof Error ? error.message : 'Scan failed' },
      { status: 500 },
    );
  }
}
