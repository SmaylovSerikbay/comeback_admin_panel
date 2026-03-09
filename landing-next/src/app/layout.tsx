import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ComeBack — AR-платформа для бизнеса",
  description:
    "ComeBack — платформа дополненной реальности для маркетинга, продаж и вовлечения клиентов.",
  viewport: { width: "device-width", initialScale: 1, maximumScale: 5 },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru">
      <body>
        <main>{children}</main>
      </body>
    </html>
  );
}
