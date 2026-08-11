/** @type {import('next').NextConfig} */
const apiUpstream = process.env.API_UPSTREAM || 'http://127.0.0.1:8000';

const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api-backend/:path*',
        destination: `${apiUpstream}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
