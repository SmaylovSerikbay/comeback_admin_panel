/** @type {import('next').NextConfig} */
const apiUpstream = process.env.API_UPSTREAM || "http://127.0.0.1:8000";

const nextConfig = {
  output: "standalone",
  reactStrictMode: true,
  // Без sharp в Alpine/Docker оптимизатор /_next/image даёт 400 — отдаём файлы из /public как есть
  images: {
    unoptimized: true,
  },
  async rewrites() {
    return [
      {
        source: "/api-backend/:path*",
        destination: `${apiUpstream}/api/:path*`,
      },
    ];
  },
  async redirects() {
    return [
      { source: "/favicon.ico", destination: "/favicon.svg", permanent: false },
    ];
  },
};

export default nextConfig;
