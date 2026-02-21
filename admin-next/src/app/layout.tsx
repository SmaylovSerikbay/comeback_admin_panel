import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ComeBack Admin",
  description: "Панель управления AR приложением ComeBack",
  viewport: { width: "device-width", initialScale: 1, maximumScale: 5 },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
