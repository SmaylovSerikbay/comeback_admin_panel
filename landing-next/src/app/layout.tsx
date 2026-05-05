import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ComeBack — древние города Узбекистана в AR",
  description:
    "ComeBack — мобильное приложение дополненной реальности, которое показывает, какими были Бухара, Самарканд, Хива и другие города Узбекистана в прошлом.",
  viewport: { width: "device-width", initialScale: 1, maximumScale: 5 },
  icons: {
    icon: "/favicon.svg",
    apple: "/favicon.svg",
  },
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
